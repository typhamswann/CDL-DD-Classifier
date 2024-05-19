from api import APIClient
from prompts import PromptTuner

class Classifier:
    def __init__(self):
        self.client = APIClient()
        self.prompt_tuner = PromptTuner()
        
    def classify(self, prompt):
        response = self.client.get_response(self.prompt_tuner.zero_shot_inststructions, prompt)
        return response
        
classifier = Classifier()

print(classifier.classify(prompt="""Climate Sciencists are biased."""))