This repository contains the codes used in the paper Predicting the Canadian Yield Curve Using Machine Learning Techniques by Rayeni and Naderi (2024). 
The repository contains the following:

1- STAT_CANADA.py: this file contains a function that receives a list of vector ids from Statistics Canada and the start date and returns the data from the start date onwards for the said vectors

2- Yield Curve Pricing_data_Shared.ipynb: this code script retrieves the data set using (1) and also cleans the data and prepare it for regressions
3- model_regression.ipynb: this code script runs the regressions using data from (2) and fine tunes the hyperparameters and returns the best fits based on the said algorithms
