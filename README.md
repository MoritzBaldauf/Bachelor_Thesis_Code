
# The Impact of Weather Changes on U.S. Amazon Marketplace Purchasing Behavior

This repository contains the code and analysis for the Bachelor's thesis "The Impact of weather changes on the purchasing behavior of the U.S. Amazon Marketplace" by Moritz Baldauf (Vienna University of Economics and Business, 2025).

## Abstract

This study investigates how weather variables (temperature and precipitation) influence online purchasing behavior on Amazon across 48 U.S. states from 2017-2023. Using Granger causality tests and linear regression analysis, we find that **temperature significantly affects weather-sensitive fashion purchases** (+1.5% per °C for hot-weather items, -1.0% per °C for cold-weather items), while precipitation effects are limited. The research contributes to understanding climate-driven e-commerce behavior across different geographic regions.

## Research Questions

1. **Does Climate have an impact on e-commerce sales?**
2. **What are the magnitude and direction of weather effects on specific product categories?**
3. **Do these effects vary across different geographic regions and climate zones?**

## Key Findings

- **Temperature has significant predictive power** for fashion purchases in multiple U.S. states
- **Hot-weather fashion items** show positive temperature sensitivity (mean +1.5% per °C)
- **Cold-weather fashion items** show negative temperature sensitivity (mean -1.0% per °C)
- **Grocery purchases** show minimal weather sensitivity compared to fashion
- **Regional climate zones** exhibit different weather-purchase relationship patterns
- **Precipitation effects** are generally weak and inconsistent across categories

## Data Sources

### 1. Amazon Purchase Dataset
- **Source**: [Berke et al. (2023)](https://doi.org/10.7910/DVN/YGLYDY) - Crowdsourced Amazon purchase histories
- **Coverage**: 5,027 Amazon customers, 1.8M transactions (2018-2023)
- **Geographic Scope**: 48 U.S. states
- **Categories**: 1,870 subcategories, aggregated into Fashion and Groceries

### 2. Weather Dataset  
- **Source**: [PRISM Climate Data](https://prism.oregonstate.edu/) via API
- **Variables**: Daily temperature and precipitation by state
- **Coverage**: 2017-2024 (extended beyond purchase data for year-over-year comparisons)
- **Resolution**: State-level aggregation

## Repository Structure

```
├── data/
│   └── amazon-purchases.csv       # Amazon Transactions dataset
│   └── survey.csv                 # Demographic Variables of Amazon Customers
│   └── weather_data.csv           # Weather data collected from 
├── Weather_API_call.R             # Main R script for weather data download
├── 0_Data_Processing.ipynb        # Combining of data and pre-processing
├── 1_Stationarity_test.ipynb      # Performs basic Stationarity testing 
├── 2_Granger_test.ipynb           # Performs a Granger causality test
├── 3_Linear_regression.ipynb      # Linear regression for Groceries and Fashion Subcategories
├── 4_Climate_Clustering.ipynb     # Applies Köppen climate clusters and performs linear regression
└── README.md                  # Documentation
```

## Code Overview

### `Weather_API_call.R`

This is the main R script that handles:

1. **Package Management**: Loads required libraries for data processing and visualization
2. **Weather Data Download**: Custom `download_prism()` function to fetch PRISM climate data
3. **Data Processing**: Aggregates daily weather data across multiple years and states
4. **Export**: Saves processed data as CSV for further analysis

### `0_Data_Processing.ipynb`

Script for processing the data into two data frames: fashion products and groceries. 

1. **Formatting state names**: Changing the naming of locations to match across data frames is important for joining the data.
2. **Combining weather and demographic data**: joining weather and demographic columns to the transaction information
3. **Formatting for single entry per date and state**: For each data frame, we processed the data to only contain an aggregated entry for a state on a single day
4. **Exporting results**: Results were saved as two separate CSV files

### `1_Stationarity_test.ipynb `

Script for testing the stationarity of both data frames Time series

1. **Visual comparison of aggregated sales data**: Visualization of Revenue and SMA7 and SMA30 for Fashion and Groceries data frame
2. **Visual comparison of climate data**: single plot visualization of temperature and precipitation in all 48 states
3. **Visual comparison of single state sales data**: Visualization of SMA7 Revenue of California
4. **Calculation of p-values using Augmented-Dickey Fuller (ADF) Test**: Performing ADF test for time series stationary

### `2_Granger_test.ipynb`

Script for implementing and visualizing a Granger Causality Test

1. **Implementation of Granger Causation Matrix**: Implementation of a Function for Granger Testing, allowing testing of Granger Causality between the variables
2. **Map Visualization of Granger Test Results**: Creation of a US-Map visualizing the Granger causality of a single state
3. **Implementation of Benjamini-Hochberg Multiple Error Adjustment**: Adjustment of the p-values for multiple testing via the Benjamini-Hochberg Method
4. **Visualization of adjusted and unadjusted p-values via Beeplot**: Creation of a Beeplot for p-values (adjusted and unadjusted) for both product categories

### `3_Linear_regression.ipynb`

Script to perform a linear regression for weather-sensitive product categories

1. **Creation of Linear Regression Function**: Creating a linear regression function for the data frame and input variables 
2. **Visualization of coefficient results of all states**: Visualizing regression results of all 48 states via Beeplot
3. **Visualization of p-values via an empirical cumulative distribution plot**: Creating a visualization for the distribution of p-values of our regressions

### `4_Climate_Clustering.ipynb`

Script to cluster states into Köppen Climate Clusters and perform climate regression on a cluster level

1. **Creation of climate clusters**: Assign the cluster to each state and visualize the results on a map
2. **Calculate the correlation matrix for each cluster**: Calculate and visualize the correlation matrix for each cluster; the minimum value in each cluster needs to be >= 0.75
3. **Perform linear regression** calculate the coefficients and p-values for the climate impacts for each cluster

## Requirements

### R Packages
```r
# Data processing
tidyverse, data.table, purrr

# Visualization  
sf, tigris, pals
```

### Installation
```r
if (!require("pacman")) install.packages("pacman")
pacman::p_load(tidyverse, data.table, purrr, sf, tigris, pals)
```

### Python Packages
```python
# Data processing
pandas, numpy

# Statistical analysis and time series
statsmodels, scipy

# Data visualization
matplotlib, seaborn

# Geospatial analysis
geopandas

# Machine learning utilities
ISLP

# Additional utilities
holidays, os, random
```

### Installation
```python
pip install pandas numpy statsmodels scipy matplotlib seaborn geopandas ISLP holidays
```