from Data_cleaning import DataCleaning
import pandas as pd

# data .csv file
data = pd.read_csv("Wilson-disease-to-predict-neurological-symptoms.csv")
cleaner = DataCleaning(data=data)

to_drop = [
    # affects males and females equally
    "Gender",
    # non-informative
    "Qther brain regions damage(es/No)",
    # Not Specific
      "Cerebral cortex damage(es/No)",
      "Cerebral peduncle damage(es/No)",
    # Do the same as Cerebral ventricular system dilation
    "Deepening of the sulci and fissures of the brain(es/No)",
    # General health
    "WBC", "RBC", "Hb", "PLT",
    # Secondary
    "BUN", "Cr"]

cleaner.drop_columns(to_drop)
cleaner.transform_label()