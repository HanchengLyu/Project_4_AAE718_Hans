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
