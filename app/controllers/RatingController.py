import json, requests
from flask import Blueprint, current_app
from flask import render_template, url_for, request, jsonify,session, redirect
import redis as red
import json
from pymongo import MongoClient, ASCENDING

from datetime import datetime, timedelta
import hashlib
from app.forms.Ratings import Ratings
from marshmallow import ValidationError

ratingBlueprint = Blueprint('rating', __name__)
r = red.StrictRedis(host=current_app.config['REDIS_HOST'], port=current_app.config['REDIS_PORT'])

client =  MongoClient(current_app.config['MONGODB_HOST'],current_app.config['MONGODB_PORT'])
db = client.Blndr
comments = db.comments

@ratingBlueprint.route("/api/rating/<repo_user>/<repo_name>", methods=["POST"])
def storeRating(repo_user, repo_name):

    req = request.get_json()

    if req == None:
        return jsonify ({"message":"Invalid Request"}) ,400
    schema = Ratings()
    try:
        validation = schema.load(req)
        
        repo_full_name = repo_user+'/'+repo_name

        pre_id = str(13) + '_'+ req['application_name']+ '_' + str(req['repo_id'])
        hashed =  hashlib.sha256( pre_id.encode('utf-8')).hexdigest()
        website = None

        if 'website' in req:
            website = req['website']

        
        if comments.find_one({"id": hashed}) == None:

            comment = {
                'application_name':req['application_name'],
                'rating':req['rating'],
                'repo_id': req['repo_id'],
                'repo_full_name': repo_full_name,
                'website': website,
                'user_id': 13,
                'comments': req['comment'],
                'platform': req['platform'],
                'id': hashed,
                'abusive': False,
                'deleted_at': None,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),

            }
            comments.insert_one(comment)

            return jsonify({"message": "Comment Added"})
        else:

            return jsonify({"message": "Comment has been added before"}) , 403
    except ValidationError as err:
        return jsonify (err.messages), 400


@ratingBlueprint.route("/api/rating/<repo_id>", methods=["GET"])
def getRatings(repo_id):
      
    comment = comments.find({"repo_id": repo_id, "deleted_at":None},{'_id': False})

    return jsonify(list(comment))
  