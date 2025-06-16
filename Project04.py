import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = r"D:\tasks\2025 Spring\AAE 718\Project04\agstar-livestock-ad-database.xlsx"
save_path = r"D:\tasks\2025 Spring\AAE 718\Project04"
df = pd.read_excel(file_path)
#clean data
df_cleaned = df.dropna(subset=['Dairy']).copy()

# Awarded USDA Funding? → 0/1
df_cleaned['Awarded_USDA_Funding'] = (
    df_cleaned['Awarded USDA Funding?']
       .astype(str).str.strip().str.lower().eq('yes').astype(int)
)

# Co-Digestion → 0/1
df_cleaned['Co_Digestion_Flag'] = (~df_cleaned['Co-Digestion'].isna()).astype(int)
df_cleaned['Dairy'] = pd.to_numeric(df_cleaned['Dairy'], errors='coerce')
df_cleaned['Total_Emissions'] = pd.to_numeric(
    df_cleaned['Total Emission Reductions (MTCO2e/yr)'], errors='coerce'
)
df_cleaned['Year_Operational'] = pd.to_numeric(
    df_cleaned['Year Operational'], errors='coerce'
)

# drop na
df_reg = df_cleaned.dropna(subset=[
    'Biogas Generation Estimate (cu-ft/day)',
    'Dairy', 'Awarded_USDA_Funding', 'Co_Digestion_Flag',
    'Total_Emissions', 'Year_Operational'
])

# OLS regression 
model = smf.ols(
    formula='Q("Biogas Generation Estimate (cu-ft/day)") '
            '~ Dairy + Awarded_USDA_Funding + Co_Digestion_Flag '
            '+ Total_Emissions + Year_Operational',
    data=df_reg
).fit()

print(model.summary())

df_cleaned['ln_Biogas']          = np.log1p(df_cleaned['Biogas Generation Estimate (cu-ft/day)'])
df_cleaned['ln_Dairy']           = np.log1p(df_cleaned['Dairy'])
df_cleaned['ln_Total_Emissions'] = np.log1p(df_cleaned['Total_Emissions'])
df_cleaned['ln_Year_Operational'] = np.log1p(df_cleaned['Year_Operational'])

# ---------- 4. 准备回归数据 ----------
df_reg = df_cleaned.dropna(subset=[
    'Biogas Generation Estimate (cu-ft/day)', 'ln_Dairy', 'ln_Total_Emissions', 'Year_Operational',
    'Awarded_USDA_Funding', 'Co_Digestion_Flag'
])

# ---------- 5. OLS 回归 ----------
model = smf.ols(
    formula='Q("Biogas Generation Estimate (cu-ft/day)") ~ ln_Dairy + ln_Total_Emissions + Year_Operational '
            '+ Awarded_USDA_Funding + Co_Digestion_Flag',
    data=df_reg
).fit()

print(model.summary())

y_true = df_reg['Biogas Generation Estimate (cu-ft/day)']
y_pred = model.fittedvalues            # 与 df_reg 顺序一致

# ① 散点图
plt.figure(figsize=(8, 6))
plt.scatter(y_true, y_pred, alpha=0.6)

# ② 45° 参考线
lims = [y_true.min(), y_true.max()]
plt.plot(lims, lims)                   # 不指定颜色，matplotlib 会用默认颜色

# ③ 标注
plt.xlabel('Actual Biogas Generation (cu-ft/day)')
plt.ylabel('Predicted Biogas Generation (cu-ft/day)')
plt.title('Predicted vs. Actual – OLS Model')
plt.tight_layout()
plt.savefig(os.path.join(save_path, 'ols_predicted_vs_actual.png'), dpi=300)

plt.figure(figsize=(8, 6))
plt.scatter(y_true, y_pred, alpha=0.6)
plt.plot(lims, lims)      # 45° 线

plt.xscale('log')
plt.yscale('log')

plt.xlabel('Actual (log-scale) Biogas Generation')
plt.ylabel('Predicted (log-scale) Biogas Generation')
plt.title('Predicted vs. Actual – log–log view')
plt.tight_layout()
plt.savefig(os.path.join(save_path, 'ols_log_predicted_vs_actual.png'), dpi=300)


# --- ① 读数据 + 原来的清洗 ----
file_path = r"D:\tasks\2025 Spring\AAE 718\Project04\agstar-livestock-ad-database.xlsx"
df = pd.read_excel(file_path).dropna(subset=['Dairy']).copy()

df['Awarded_USDA_Funding'] = (df['Awarded USDA Funding?']
                              .astype(str).str.strip().str.lower().eq('yes').astype(int))
df['Co_Digestion_Flag'] = (~df['Co-Digestion'].isna()).astype(int)

df['Dairy'] = pd.to_numeric(df['Dairy'], errors='coerce')
df['Total_Emissions'] = pd.to_numeric(df['Total Emission Reductions (MTCO2e/yr)'], errors='coerce')
df['Year_Operational'] = pd.to_numeric(df['Year Operational'], errors='coerce')

# --- ② 取对数（log1p 避免 0 值崩溃） ----
df['ln_Biogas']          = np.log1p(df['Biogas Generation Estimate (cu-ft/day)'])
df['ln_Dairy']           = np.log1p(df['Dairy'])
df['ln_Total_Emissions'] = np.log1p(df['Total_Emissions'])
df['ln_Year_Operational'] = np.log1p(df['Year_Operational'])    # 如年份基本 >0 也可直接 ln

# --- ③ 组回归数据 ----
df_reg = df.dropna(subset=[
    'ln_Biogas', 'ln_Dairy', 'ln_Total_Emissions', 'ln_Year_Operational',
    'Awarded_USDA_Funding', 'Co_Digestion_Flag'
])

# --- ④ 估计 (Log-Log + 两个虚拟变量) ----
log_model = smf.ols(
    'ln_Biogas ~ ln_Dairy + ln_Total_Emissions + ln_Year_Operational '
    '+ Awarded_USDA_Funding + Co_Digestion_Flag',
    data=df_reg
).fit()

print(log_model.summary())
import matplotlib.pyplot as plt



y_true = np.expm1(df_reg['ln_Biogas'])          # 如果用 ln_Biogas 回归
y_pred = np.expm1(log_model.fittedvalues)

# ① 统一散点颜色
plt.figure(figsize=(8, 6))
plt.scatter(y_true, y_pred, alpha=0.7, s=45, color='steelblue')

# ② 计算整体轴限
all_vals = np.concatenate([y_true, y_pred])
low  = all_vals.min() * 0.9    # 略放大一点边界
high = all_vals.max() * 1.1

# ③ 画贯穿全域的 45° 线
plt.plot([low, high], [low, high],
         linestyle='--', linewidth=2)

# ④ 设置对数坐标 & 轴限
plt.xscale('log'); plt.yscale('log')
plt.xlim(low, high); plt.ylim(low, high)

# ⑤ 美化标签
plt.xlabel('Actual Biogas (cu-ft/day)')
plt.ylabel('Predicted Biogas (cu-ft/day)')
plt.title('Predicted vs. Actual – log–log view')
plt.tight_layout()
plt.savefig(os.path.join(save_path,'log_log'),dpi = 300)

