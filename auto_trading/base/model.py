import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split


class Model:
    def __init__(self, datamart):
        self._datamart = datamart

    def fit(self):
        self.clf = lgb.LGBMClassifier()
        self.df = pd.DataFrame(self._datamart)
        self.X = self.df[
            [
                "close_N-0",
                "close_N-1",
                "close_N-2",
                "close_N-3",
                "close_N-4",
                "close_N-5",
            ]
        ]
        self.y = self.df["target"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.3, random_state=0
        )
        self.clf.fit(self.X_train, self.y_train)

    def predict(self):
        self.fit()
        self.y_pred = self.clf.predict(self.X_test)
        return self.y_pred
