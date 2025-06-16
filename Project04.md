[GitHub Link](https://github.com/HanchengLyu/Project_4_AAE718_Hans/settings)
# 1 Introduction

This project explores the relationship between biogas generation and various influencing factors in livestock-based anaerobic digestion systems. The dataset used for this analysis is sourced from [Kaggle](https://www.kaggle.com/datasets/mehmetisik/livestock-anaerobic-digester-database), specifically the *Livestock Anaerobic Digester Database*, which compiles information on digester projects implemented across the United States.

The dataset contains detailed project-level data, including variables such as digester type, operational year, funding status, livestock type, and estimated biogas production. The primary variable of interest in this study is the *Biogas Generation Estimate (cu-ft/day)*, which serves as the dependent variable in the regression models.

The main objective of this analysis is to investigate how biogas generation correlates with several key factors present in the dataset, namely:

- Dairy livestock population (Dairy)
- Total Emission Reductions (MTCO2e/yr)
- Year of Operational Start
- Whether the project received USDA funding
- Whether the digester system includes co-digestion of additional substrates

By applying both linear and log-log regression models, this study aims to uncover patterns and relationships between biogas generation and these factors, and to assess which variables most strongly influence the performance of anaerobic digestion systems.

# 2 Regression Model

In this section, I ran three successive regression specifications to identify the functional form that best captures how project-level factors affect *Biogas Generation Estimate (cu-ft/day)*.

---

### 2.1  Linear Model  

The initial specification is an ordinary least squares (OLS) model in levels:

- **Predictors:** Dairy, Total Emissions, Year Operational, USDA Funding, Co-Digestion Flag  
- **R² = 0.735**

Among these, **Awarded USDA Funding** (p = 0.621) and **Total Emissions** (p = 0.279) are not significant, hinting that a simple linear form may be inadequate.

![Predicted vs. Actual – linear view](D:/tasks/2025%20Spring/AAE%20718/Project04/ols_predicted_vs_actual.png)

---

### 2.2  Level-Log Model  

To accommodate potential curvature, I next log-transformed key predictors (ln Dairy, ln Total Emissions) while keeping the dependent variable in levels. The fitted–actual plot clearly traces a logarithmic-shaped cloud:

![Predicted vs. Actual – level-log view](D:/tasks/2025%20Spring/AAE%20718/Project04/ols_log_predicted_vs_actual.png)

Although the overall fit drops (R² = 0.437), the scatter pattern suggests the response itself may also require a log transformation.

---

### 2.3  Log-Log Model  

Finally, I applied a full log-log specification—log-transforming both the dependent variable and the main continuous predictors. This model achieves the best statistical fit (R² = 0.779) and yields highly significant elasticities for **ln Dairy** (p < 0.001) and **Co-Digestion Flag** (p < 0.001). Unsurprisingly, **ln Total Emissions**, **ln Year Operational**, and **USDA Funding** remain insignificant, but the residual pattern is markedly tighter.

![Predicted vs. Actual – log-log view](D:/tasks/2025%20Spring/AAE%20718/Project04/log_log.png)

---

### 2.4  Model Choice Rationale  

- The linear model over-predicts high-volume projects and under-predicts low-volume ones, reflecting multiplicative rather than additive noise.  
- The level-log model reduces heteroscedasticity but still leaves curvature unexplained.  
- The log-log model aligns predicted and actual values along the 45-degree line in log space, confirming a proportional (elasticity-type) relationship.

For these reasons, the log-log specification is selected as the preferred model for subsequent interpretation.
# 3 Conclusion

**Key Relationships.**  
The log–log model shows that dairy herd size and the presence of co-digestion dominate biogas performance. A 1 % increase in herd size raises daily gas output by about 0.85 %. Systems accepting additional organic substrates (co-digestion) produce nearly 90 % more gas than manure-only units. In contrast, total-emission credits, project age, and USDA funding display weak or statistically insignificant effects once scale and feedstock diversity are controlled for.

**Implications.**  
These results underline two practical levers: enlarge manure supply and integrate high-energy co-substrates. Policymakers could therefore focus incentives on feedstock aggregation and scale-up rather than flat capital grants. Investors should prioritise herd size and feedstock contracts when screening projects, while reported emission-reduction figures alone are a poor proxy for real output.

**Limitations.**  
The analysis relies on a cross-section of self-reported project data, omits detailed engineering variables (e.g., digester volume, retention time), and still exhibits mild heteroskedasticity despite log transformation. A high condition number hints at multicollinearity among scale-related variables, which may inflate standard errors.

**Future Improvements.**  
Panel data tracking year-over-year performance, richer technical covariates, and robust or machine-learning models could sharpen causal insight. Incorporating spatial factors such as energy prices and climate, plus out-of-sample validation, would further strengthen the model’s predictive power and policy relevance.
