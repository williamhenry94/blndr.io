import json, requests
from flask import Blueprint, current_app
from flask import render_template, url_for, request, jsonify,session, redirect
from app.models.User import User
from uuid import uuid4
from github import Github

import requests
import redis as red
from datetime import datetime, timedelta

from flask_dance.contrib.github import github

githubBlueprint = Blueprint('githubBlueprint', __name__)

r = red.StrictRedis(host=current_app.config['REDIS_HOST'], port=current_app.config['REDIS_HOST'])

@githubBlueprint.route("/")
def index():
    if not github.authorized:
        return redirect("/auth")
    resp = github.get("/user")
    assert resp.ok

    githubData = resp.json()
    u = User.where('github_id',  githubData["id"]).first()
    
    if u == None:
        print ("none")
        user = User()
        user.name = githubData["name"]
        user.username = githubData["login"]
        user.email = githubData["email"]
        user.github_id = githubData["id"]
        user.avatar_url = githubData["avatar_url"]
        user.github_api_url = githubData["url"]
        user.access_token   = session["github_oauth_token"]["access_token"]
        user.github_html_url = githubData["html_url"]
        user.save()
        u=user


    session["user"] = u.to_json()
    return render_template("search.html", user = u)

def checkSession():
    
    try:
        user = session["user"]
        user = json.loads(user)
        return user
    except Exception:
        return None
    

@githubBlueprint.route("/repos")
def getRepos():

    if not github.authorized:
        return redirect("/auth")
    
    user= checkSession()
    if user == None:
        return jsonify({"message": "Forbidden"}), 403
    
    query = "React"
    repos= []
    if r.get(query) == None:
       
        payload = {"q":query,"sort":"stars", "order":"desc", 'access_token': user["access_token"]}
        rq = requests.get('https://api.github.com/search/repositories', params = payload)
        queries = json.loads(rq.text)["items"]
        
        for i in queries:
        
            repos.append({
                "id":i["id"],
                "name":i["name"], 
                "full_name":i["full_name"], 
                "description": i['description'],
                'issues':i['open_issues_count'], 
                'has_issues':i['has_issues'],
                'language': i['language'],
                # 'topic': i['topic'],
                'forks_count': i["forks_count"],
                'license': i['license'],
                'watchers_count': i['watchers_count'],
                'stargazers_count': i['stargazers_count'],
                'size': i['size'],
                'owner': i['owner'],
                'url': i['url'],
                'score':i['score'],
                'created_at':i['created_at'],
                'updated_at': i ['updated_at'],
                'pushed_at': i['pushed_at'],
                'default_branch': i['default_branch']
            })

        repoJSON = json.dumps(repos)

        r.set(query, repoJSON)
        r.expire(query, 3600)

    else:
        repos = json.loads(r.get(query))

    return jsonify(repos)

@githubBlueprint.route("/auth")
def auth():
    return "Auth required"


def getReadme(accessToken, repo_user, repo_name):
    payload = {'access_token': accessToken}
    rq = requests.get('https://api.github.com/repos/'+repo_user+"/"+repo_name+"/readme", params = payload)
    readme = json.loads(rq.text)

    rq = requests.get(readme['download_url'], params = payload)
    readme = rq.text

    return readme

@githubBlueprint.route("/repo/<repo_user>/<repo_name>")
def showRepo(repo_user, repo_name):
    if not github.authorized:
        return redirect("/auth")
    
    user= checkSession()
    if user == None:
        return jsonify({"message": "Forbidden"}), 403
    

    if r.get(repo_user+"/"+repo_name) == None:
        payload = {'access_token': user["access_token"]}
        rq = requests.get('https://api.github.com/repos/'+repo_user+"/"+repo_name, params = payload)
        repo = json.loads(rq.text)
        r.set(repo_user+"/"+repo_name, json.dumps(repo))
        r.expire(repo_user+"/"+repo_name, 900)
    else:
        
        repo = json.loads(r.get(repo_user+"/"+repo_name))
    
    readme = getReadme(user['access_token'], repo_user, repo_name)
    return render_template("repo.html", user=user, repo = repo, readme=readme)


@githubBlueprint.route("/readme/<repo_user>/<repo_name>")
def showReadme(repo_user, repo_name):

    if not github.authorized:
        return redirect("/auth")
    
    user= checkSession()
    if user == None:
        return jsonify({"message": "Forbidden"}), 403
    

    readme = getReadme(user['access_token'], repo_user, repo_name)
    return render_template("readme.html", user=user, readme=readme)
