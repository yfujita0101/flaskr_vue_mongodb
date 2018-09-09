from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from db import get_db
import os
import shutil


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# file saved path
FILE_ROOT_PATH = os.getcwd() + "/images/"


@app.route('/images/<post_id>/<file_name>', methods=['GET'])
def image(post_id, file_name):
    print(post_id)
    # 画像保存パス
    file_path = FILE_ROOT_PATH + post_id

    file_path = os.path.join(file_path, file_name)


    # file拡張子取得
    ext = str(file_path).split(".")[-1]
    type = "image/" + ext

    # return target image
    f = open(file_path, 'rb')
    image = f.read()
    return Response(response=image, content_type=type)


@app.route('/posts', methods=['GET', 'POST'])
def all_posts():
    response_object = { 'status': 'success'}
    if request.method == 'POST':
        post_data = request.form
        db = get_db()
        post_id = db.post.insert({'title': post_data["title"], 'body': post_data["body"], 'updated': datetime.utcnow()})

        # file save
        file_url = ''
        filename = ''
        if 'file' in request.files:
            # make file save dir (use mongodb _id)
            file_dir_path = os.path.join(FILE_ROOT_PATH, str(post_id))
            os.makedirs(file_dir_path)

            # file save
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(file_dir_path, filename))

            # file url情報をmongodbに保存
            file_url = "http://localhost:5000/images/" + str(post_id) + "/" + str(filename)

        result = db.post.update_one({"_id": ObjectId(post_id)}, {'$set': {'file_url': file_url}})

        response_object['message']  = 'post added!'
    else:
        response_object['posts'] = get_all_posts()

    return jsonify(response_object)


def get_all_posts():
    db = get_db()
    posts = db.post.find()

    results = []

    #
    if posts:
        for post in posts:
            results.append({"id": str(post["_id"]), "title": post["title"], "body": post["body"],  "updated": post["updated"], "file_url": post["file_url"]})


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
        # mongodbから削除
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

    # 画像削除
    file_dir = FILE_ROOT_PATH + post_id
    shutil.rmtree(file_dir)

    return result

if __name__ == '__main__':
    app.run()
