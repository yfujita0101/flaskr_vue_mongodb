from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from db import get_db
from bson.objectid import ObjectId

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


# enable CORS
CORS(app)


@app.route('/posts', methods=['GET', 'POST'])
def all_posts():
    response_object = { 'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        db = get_db()
        post_id = db.post.insert({'title': post_data["title"], 'body': post_data["body"], 'updated': datetime.utcnow()})
        response_object['message']  = 'post added!'
    else:
        response_object['posts'] = get_all_posts()

    return jsonify(response_object)


def get_all_posts():
    db = get_db()
    posts = db.post.find()

    results = []

    # objectIDをstrにキャスト
    for post in posts:
        results.append({"id": str(post["_id"]), "title": post["title"], "body": post["body"],  "updated": post["updated"]})

    return results

@app.route('/posts/<post_id>', methods=['PUT', 'DELETE'])
def single_post(post_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        # payloadの値を取得
        post_data = request.get_json()
        title = post_data['title']
        body = post_data['body']

        # post_id指定でupdate
        db = get_db()
        result = db.post.update_one({"_id": ObjectId(post_id)}, {'$set': {'title': title, 'body': body, 'updated': datetime.utcnow()}})

        response_object['message'] = 'post updated!'

    if request.method == 'DELETE':
        result = remove_post(post_id)
        if result:
            response_object['message'] = 'post removed!'
        else:
            resuponse_object['message'] = 'post not removed!'

    return jsonify(response_object)


def remove_post(post_id):
    db = get_db()
    result = db
    result = db.post.delete_one(({"_id": ObjectId(post_id)}))

    return result

if __name__ == '__main__':
    app.run()
