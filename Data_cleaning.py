from dataclasses import dataclass, field
import pandas as pd
from sklearn.linear_model import LogisticRegression

@dataclass
class DataCleaning:
    data: pd.DataFrame = field(default_factory=pd.DataFrame)
    
    def drop_columns(self, to_drop):
        """Drop columns and save the cleaned data"""
        self.data.drop(columns=to_drop, inplace=True)
        self.data.to_csv("cleaned_data.csv", index=False)

    def transform_label(self):  
        """transforming label column from 0/1 to XX.XX%"""
        x = self.data.drop(columns=["label"])
        y = self.data["label"]

        model = LogisticRegression(max_iter=10000)
        model.fit(X=x, y=y)

        probs = model.predict_proba(X=x)[:, 1]

        self.data["label"] = (probs * 100).round(2)

        self.data.to_csv("cleaned_data.csv", index=False)

        return self.data