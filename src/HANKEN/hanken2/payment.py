import payjp
import os
from dotenv import load_dotenv

class payment:
    apikey = ""
    def __init__(self):
        load_dotenv()
        self.apikey = os.environ['PAYJP_TOKEN']
    def sendpay(self,amount,toaken):
        payjp.api_key = self.apikey
        charge = payjp.Charge.create(
            amount=amount,
            card=toaken,
            currency='jpy',
        )
        return charge
