from api import APIClient
import pandas as pd

class Classifier:
    def __init__(self):
        self.client = APIClient()
        
    def classify(self, claim):
        response, subclaim_list, valid_subclaims = self.client.run_pipeline(claim)
        return response, subclaim_list, valid_subclaims
        
classifier = Classifier()

# Classify congress Test set
validation_set = pd.read_csv("data_labeled/formatted_test_50_samples.csv")

#clean
validation_set["label"] = validation_set["label"].apply(lambda x: int(x))
validation_set["text"] = validation_set["text"].apply(lambda x: x.replace("\n"," "))

# Classify a sample.
# validation_set = validation_set.sample(5)

validation_set_labeled = pd.DataFrame(columns=["text", "human_label", "llm_label", "subclaim_list", "valid_subclaims"])

for counter, (_, row) in enumerate(validation_set.iterrows()):
    try:
        text = row["text"]
        human_label = row["label"]
        llm_label, subclaim_list, valid_subclaims = classifier.classify(text)
    
    except Exception as e:
        print("ERROR: ", e)
        llm_label = 999
        subclaim_list = []
        valid_subclaims = []
    
    new_row_df = pd.DataFrame([{
        "text": text, 
        "human_label": human_label, 
        "llm_label": llm_label, 
        "subclaim_list": subclaim_list, 
        "valid_subclaims": valid_subclaims
    }])
    validation_set_labeled = pd.concat([validation_set_labeled, new_row_df], ignore_index=True)
        
    if counter % 5 == 0:
        print("Classified", counter, "/", len(validation_set), "paragraphs")

validation_set_labeled.to_csv("selected_few_shot_pipeline/results.csv", mode='a', index=False)
