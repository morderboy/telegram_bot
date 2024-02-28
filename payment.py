import config
from yoomoney import Client
import asyncio

token = config.get_yoomoney_access_token()
client = Client(token)

async def payment_check(label: str):
    while True:
        print("waiting: {}".format(label))
        history = client.operation_history(label=label)
        oper = None
        for operation in history.operations:
            oper = operation
        if oper != None and oper.status == "success":
            print("Well done 47")
            return True
        else:
            await asyncio.sleep(30)

    
