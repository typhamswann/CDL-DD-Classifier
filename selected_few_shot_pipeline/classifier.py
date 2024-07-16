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
validation_set = pd.read_csv("data_labeled/ty_will_data/denial_delay_labels_formatted_150.csv")

#clean
validation_set["text"] = validation_set["text"].apply(lambda x: x.replace("\n"," "))

# Classify a sample.
# validation_set = validation_set.sample(5)

validation_set_labeled = pd.DataFrame(columns=["id","text","user_1","user_2","category_1","category_2", "llm_label", "intermediary_response", "valid_subclaims"])

for counter, (_, row) in enumerate(validation_set.iterrows()):
    try:
        id = row["id"]
        text = row["text"]
        user_1 = row["user_1"]
        user_2 = row["user_2"]
        category_1 = row["category_1"]
        category_2 = row["category_2"]
        llm_label, intermediary_response, valid_subclaims = classifier.classify(text)
        
    except Exception as e:
        print("ERROR: ", e)
        llm_label = 999
        subclaim_list = []
        valid_subclaims = []
    
    new_row_df = pd.DataFrame([{
        "id": id,
        "text": text, 
        "user_1":user_1,
        "user_2":user_2,
        "category_1":category_1,
        "category_2":category_2,
        "llm_label": llm_label, 
        "intermediary_response": intermediary_response, 
        "valid_subclaims": valid_subclaims
    }])
    validation_set_labeled = pd.concat([validation_set_labeled, new_row_df], ignore_index=True)
        
    if counter % 5 == 0:
        print("Classified", counter, "/", len(validation_set), "paragraphs")
    
    if counter % 25 == 0:
        print("---Exporting---")
        validation_set_labeled.to_csv("selected_few_shot_pipeline/results_split_150.csv", index=False)


validation_set_labeled.to_csv("selected_few_shot_pipeline/results_split_150.csv", index=False)
