import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split


class Model:
    """Model class predicts future price, up or down.
    Use LightGBM as a predictor model.
    Args:
        datamart: the stock datamart you want to predict
        feature: explanatory variables
    """    
    def __init__(self, datamart, feature):
        self._datamart = datamart
        self._feature = feature

    def fit(self):
        self.clf = lgb.LGBMClassifier()
        self.df = pd.concat([self._datamart, self._feature], axis=1)
        self.X = self.df.iloc[:,1:]
        self.y = self.df["target"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.3, random_state=0
        )
        self.clf.fit(self.X_train, self.y_train)

    def predict(self):
        self.fit()
        self.y_pred = self.clf.predict(self.X_test)
        return self.y_pred
