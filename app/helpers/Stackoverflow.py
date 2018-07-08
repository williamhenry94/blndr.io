import requests
from flask import current_app

def authenticate():
    payload = {
        "client_id":current_app.config['STACKOVERFLOW_CLIENT_ID'],
        "scope":current_app.config['STACKOVERFLOW_SCOPE'], 
        "redirect_uri":current_app.config['STACKOVERFLOW_REDIRECT_URI']}
    return payload

    


   
    