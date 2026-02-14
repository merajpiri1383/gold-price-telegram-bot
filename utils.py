import os
import requests
import messages

API_URL = os.getenv("API_URL")
# Buttons 
buttons = [
    {
        "name" : "گرم طلای 18 عیار",
        "slug" : "18ayar"
    },{
        "name" : "سکه بهار آزادی",
        "slug" : "bahar"
    },{
        "name" : "انس طلا",
        "slug" : "usd_xau"
    },{
        "name" : "سکه گرمی",
        "slug" : "sek"
    }
]

async def get_gold_price (slug : str) : 

    response = requests.get(API_URL,timeout=5)

    if response.status_code == 200 : 
        content = response.json()
        try : 
            data = content[slug]
            return messages.format_gold_message(data=data)
        except : 
            return messages.API_ERROR_MESSAGE
    else : 
        return messages.API_ERROR_MESSAGE