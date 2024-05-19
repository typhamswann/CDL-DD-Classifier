import openai
import os

class APIClient():
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY") #Set API Key how??
        self.default_model = "gpt-4o"
        self.temperature = 0
        self.max_tokens = 1500
    
    def get_response(self, instructions, prompt, model=None, temperature=None, max_tokens=None):
        if not model:
            model = self.default_model
        if not temperature:
            temperature = temperature
        if not max_tokens:
            max_tokens = self.max_tokens
            
        messages = instructions + [{'role': 'user', 'content': prompt}]
        
        response_object = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            n=1,
        )
        
        response = response_object.choices[0].message.content

        return response