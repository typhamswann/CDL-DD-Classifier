from api import APIClient
from prompts import PromptTuner
import pandas as pd

class Classifier:
    def __init__(self):
        self.client = APIClient()
        self.prompt_tuner = PromptTuner()
        
    def classify(self, prompt):
        response = self.client.get_response(self.prompt_tuner.zero_shot_inststructions, prompt)
        return response
        
classifier = Classifier()

# Classify congress Validate set
congress_validate = pd.read_csv("data_labeled/congress/validation.csv")

#clean
congress_validate["label"] = congress_validate["label"].apply(lambda x: int(x))
congress_validate["text"] = congress_validate["text"].apply(lambda x: x.replace("\n"," "))

#Classify a sample.
congress_validate = congress_validate.sample(20)

congress_validate_labeled = pd.DataFrame(columns=["text", "human_label" "llm_label"])

for counter, (_, row) in enumerate(congress_validate.iterrows()):
    try:
        text = row["text"]
        human_label = row["label"]
        llm_label = int(classifier.classify(text))
    
    except Exception as e:
        print("ERROR: ", e)
        llm_label = 999
    
    new_row_df = pd.DataFrame([{"text": text, "human_label": human_label, "llm_label": llm_label}])
    congress_validate_labeled = pd.concat([congress_validate_labeled, new_row_df], ignore_index=True)
        
    if counter % 5== 0:
        print("Classified", counter, "/", len(congress_validate), "paragraphs")

congress_validate_labeled.to_csv("LLM_classifier/LLM_results/congress.csv", mode='a', index=False)

    