[![Github commit](https://img.shields.io/github/last-commit/fdjutant/combining-alpha-factors-using-random-forests/main)](https://github.com/fdjutant/combining-alpha-factors-using-random-forests)

# Combining alpha factors using random forests
## Project overview
With multiple alpha factors, one might wonder what the best way is to combine them. Certainly, some alpha factors must contribute more significantly than others, and thus, they should contribute more strongly to the portfolio weight distribution. But how can this information be revealed? In this project, a random forest algorithm was employed to determine these relative effects and optimize the construction of an alpha factor.

Throughout this project, actual stock price data were used and implemented using the Zipline API. A total of 500 indices spanning over 5 years were used for factor modelin

## Project description
### Constructing alpha factors
Three alpha factors are considered here: (1) 1-year momentum factor, (2) 5-day mean-reversion sector-neutral smoothed factor, and (3) overnight sentiment smoothed factor.

#### Features and targets/labels
Features are more general than alpha factors in that they do not have to directly contribute to returns; instead, they can be used as conditional factors. Three types of features are considered here: (1) universal quant features, (2) regime features, and (3) additional features. Quant features include 20-day and 120-day stock volatility and stock dollar volume. Regime features consist of 20-day and 120-day market dispersion and volatility. Market dispersion indicates how a stock behaves over a period, while market volatility denotes how each stock behaves relative to others. Some additional features are dates and sectors. Dates allow the identification of window dressing and calendar effects, while sectors allow the splitting of alpha factors and other features since not all factors work in all sectors.

The labels for the features are the forward returns. Applying constant thresholds to bucket returns would break the market-neutral assumption. To mitigate this issue, a workaround is to quantize market returns. Here, the 5-day returns are used for training the model. By computing the rolling autocorrelation, it can be shown that shifting the days ensures that the targets are independent and identically distributed (IID).

![Alt text](./images/rolling-autocorrelation.png?raw=true "Rolling autocorrelation for targets/labels")

### Training the model
To properly train and evaluate the model, the input samples and targets must be split into training datasets, validation datasets, and testing datasets.

A simple decision tree classifier can be constructed and visualized as shown below. The tree indicates that 20-day market dispersion appears three times, i.e., splitting the data more than other features. This is why this feature has the highest importance value, as indicated by the table below, by more than a factor of 2 compared to the 120-day market volatility.

![Alt text](./images/decision-tree.png?raw=true "Decision tree for 1-year momentum factor")
![Alt text](./images/feature-importance.png?raw=true "Feature importance")

By training multiple trees, one can track the accuracy of the random forest, as shown below. The accuracy seems to plateau once the number of trees reaches around 250. However, the most important information here is that the model is indeed overfitting because the training accuracy is much higher than the validation accuracy. This is caused by overlapping samples. To mitigate this issue, the overlapping samples can be removed by the following: dropping the overlapping samples, using BaggingClassifier's `max_samples`, and building an ensemble of non-overlapping trees.
![Alt text](./images/random-forest-accuracy.png?raw=true "Random forest accuracy")

### Deploying the model into production
To deploy the model into production, one needs to re-train it up to the current day before testing. To evaluate the model, Sharpe ratio and factor rank autocorrelation were computed and shown below.

![Alt text](./images/sharpe-ratio.png?raw=true "Sharpe ratio")

![Alt text](./images/factor-rank-autocorrelation.png?raw=true "Factor rank autocorrelation")

## Credits
The project was built as part of a practical course in systematic trading from Udacity: [AI for trading](https://www.udacity.com/course/ai-for-trading--nd880)