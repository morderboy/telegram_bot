import json

def get_BotToken():
    with open("config.json") as file:
        token_str = json.load(file)
        return token_str["BOT_TOKEN"]
    
def get_OpenAIToken():
    with open("config.json") as file:
        token_str = json.load(file)
        return token_str["OpenAI_TOKEN"]
    
def get_ConnString() -> dict:
    with open("config.json") as file:
        con_str = json.load(file)
        c_str = con_str["conn_string"]
        c_list = c_str.split('@')
        result_dict = {
            "user": c_list[0],
            "password": c_list[1],
            "database": c_list[2],
            "host": c_list[3]
        }
        return result_dict