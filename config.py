import json

def get_by_string(token: str):
    with open("config.json") as file:
        json_file = json.load(file)
        return json_file[token]

def get_BotToken():
    with open("config.json") as file:
        token_str = json.load(file)
        return token_str["BOT_TOKEN"]
    
def get_OpenAIToken():
    with open("config.json") as file:
        token_str = json.load(file)
        return token_str["OpenAI_TOKEN"]
    
def get_NgrokToken():
    with open("config.json") as file:
        token_str = json.load(file)
        return token_str["NGROK_TOKEN"]
    
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

def get_yoomoney_tokens() -> dict:
    with open("config.json") as file:
        con_str = json.load(file)
        client_id_str = con_str["client_id"]
        redirect_uri_str = con_str["redirect_uri"]
        client_secret = con_str["client_secret"]
        result_dict = {
            "client_id": client_id_str,
            "redirect_uri": redirect_uri_str,
            "client_secret": client_secret
        }
        return result_dict
    
def get_yoomoney_access_token():
    with open("config.json") as file:
        con_str = json.load(file)
        return con_str["yoomoney_access_token"]

def get_yoomoney_account_number():
    with open("config.json") as file:
        con_str = json.load(file)
        return con_str["yoomoney_account_number"]
    
def get_free_tokens_state():
    with open("config.json") as file:
        con_str = json.load(file)
        return con_str["free_tokens"]
    
def get_free_tokens_amount():
    with open("config.json") as file:
        con_str = json.load(file)
        return con_str["free_tokens_amount"]
    
def get_img_gen_price():
    with open("config.json") as file:
        con_str = json.load(file)
        return con_str["img_gen_price"]
    
def get_admin_ids():
    with open("config.json") as file:
        con_str = json.load(file)
        return con_str["admins"]