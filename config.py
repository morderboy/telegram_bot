import json

def get_BotToken():
    with open("config.json") as file:
        token_str = json.load(file)
        return token_str["BOT_TOKEN"]
    
def get_OpenAIToken():
    with open("config.json") as file:
        token_str = json.load(file)
        return token_str["OpenAI_TOKEN"]