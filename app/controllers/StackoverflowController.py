from app.helpers.Stackoverflow import authenticate

import json, requests
from flask import Blueprint, current_app
from flask import render_template, url_for, request, jsonify,session, redirect
import redis as red
import json

stackoverflowBlueprint = Blueprint('stackoverflow', __name__)
r = red.StrictRedis(host=current_app.config['REDIS_HOST'], port=current_app.config['REDIS_PORT'])

@stackoverflowBlueprint.route("/auth/stackoverflow/callback")
def stackoverflowCallback():
    code = request.args.get('code')
    
    return getAccessToken(code)

@stackoverflowBlueprint.route('/auth/stackoverflow')
def getStackoverflowCode():
    payload = authenticate()
    return redirect("https://stackoverflow.com/oauth?scope="+payload["scope"]+"&client_id="+payload['client_id']+"&redirect_uri="+payload['redirect_uri'])



def getAccessToken(code):
    
    if r.get('stackoverflow_access_token') == None:
        
        profile = authenticate()
        payload = {"client_id":profile['client_id'],"client_secret":current_app.config['STACKOVERFLOW_CLIENT_SECRET'], "code":code, 'redirect_uri': profile["redirect_uri"]}
        rq = requests.post('https://stackoverflow.com/oauth/access_token/json', data = payload)
        response = json.loads(rq.text)
        if "access_token" in response:
            r.set('stackoverflow_access_token', response["access_token"])
            return response["access_token"]
        else:
            return jsonify(response), 401
    else:
        access_token = json.loads(r.get('stackoverflow_access_token'))
        return access_token
    


@stackoverflowBlueprint.route("/api/stackoverflow")
def searchIssues():
    query = 'React'

    if r.get('stack_'+query) == None:
        access_token = str(r.get('stackoverflow_access_token'))
        headers = {
            "access_token": "Bearer "+ access_token,
            "key": current_app.config['STACKOVERFLOW_KEY']
        }
        payloads={
            "q":"React",
            "sort":'relevance',
            'order':'desc',
            'site':'stackoverflow',
            'answers': 5
        }
        rq = requests.get('https://api.stackexchange.com/2.2/search/advanced', params=payloads, headers=headers)
        res = json.loads(rq.text)
        r.set('stack_'+query, json.dumps(res) )
        r.expire('stack_'+query, 1800)
    else:
        res = json.loads(r.get('stack_'+query))

    return jsonify(res)
    