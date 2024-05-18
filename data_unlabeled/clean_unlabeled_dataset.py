"""
Purpose: cleaning up the unlabeled congress paragraphs. Some of the rows in this dataset had been 
labeled since the creation of the document, so we are removing those. 

Returns: final, unlabeled congress dataset.
"""
import pandas as pd

df = pd.read_csv("data_unlabeled/final_paragraphs_meta.csv")
df_labels = pd.read_csv("data_labeled/brown_congress_labels_mapped.csv") #Labeled examples

common_paragraph_ids = df[df['paragraph_id'].isin(df_labels['id'])]

# Remove the rows which id also appear in labeled paragr
df = df[~df['paragraph_id'].isin(common_paragraph_ids['paragraph_id'])].reset_index()

df.to_csv("data_unlabeled/unlabeled_congress.csv",index=False)