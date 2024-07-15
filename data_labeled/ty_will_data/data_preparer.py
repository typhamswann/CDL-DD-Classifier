import pandas as pd
import re
import ast
from sklearn.metrics import cohen_kappa_score


class DataPrepper:
    def __init__(self):
        pass
    
    def remove_label_text(self, text):
        #Removes the text from labels. ['0 No claim'] -> ['0']
        match = re.match(r"^\d+(\.\d+)*", text)
        if match:
            return match.group(0)
        return None
        
    
    def map_label(self, label:str):
        #Maps the CARDS taxonomy to the denial (2), delay(1) no claim (0) categories
        
        if label.startswith("1") or label.startswith("2") or label.startswith("3"):
            return 2
        elif label.startswith("4"):
            return 1
        elif label.startswith("5"):
            if label == "5.3.1":
                return 1
            else:
                return 2
        else: #Category 0. No claim.
            return 0
        
    def aggregate_by_id(self, df):
        # Aggregating by 'id' and creating new columns for user and categories
        df_agg = df.groupby('id').agg({
            'user': lambda x: list(x)[:2],
            'categories': lambda x: list(x)[:2],
            "text":"first",
        }).reset_index()

        # Expanding the lists into separate columns
        df_agg['user_1'] = df_agg['user'].apply(lambda x: x[0] if len(x) > 0 else None)
        df_agg['user_2'] = df_agg['user'].apply(lambda x: x[1] if len(x) > 1 else None)
        df_agg['category_1'] = df_agg['categories'].apply(lambda x: x[0] if len(x) > 0 else None)
        df_agg['category_2'] = df_agg['categories'].apply(lambda x: x[1] if len(x) > 1 else None)

        # Dropping the original lists columns
        df_agg = df_agg.drop(columns=['user', 'categories'])

        return df_agg
    
    def intercoder_reliability(self, labels1:list, labels2:list):
        kappa = cohen_kappa_score(labels1, labels2)
        return kappa

#Load data    
data_preparer = DataPrepper()
df = pd.read_csv("data_labeled/ty_will_data/denial_delay_labels.csv")

#Remove label text. 
df["categories"] = df["categories"].apply(lambda x: ast.literal_eval(x))
df["categories"] = df["categories"].apply(lambda x: [data_preparer.remove_label_text(str(item)) for item in x]) 

#Map to denial/delay
df["categories"] = df["categories"].apply(lambda x: [data_preparer.map_label(str(item)) for item in x]) 
df["categories"] = df["categories"].apply(lambda x: max(x)) 

grouped_df = data_preparer.aggregate_by_id(df)
grouped_df = grouped_df.dropna(subset=["category_1","category_2"])
grouped_df["category_1"] = grouped_df["category_1"].astype(int)
grouped_df["category_2"] = grouped_df["category_2"].astype(int)

print("Intercoder reliability:", data_preparer.intercoder_reliability(grouped_df["category_1"], grouped_df["category_2"]))

#Output
grouped_df.to_csv("data_labeled/ty_will_data/denial_delay_labels_formatted.csv",index=False)    
        


   
