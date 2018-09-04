from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import uuid

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


# enable CORS
CORS(app)

# 画面に表示させる例

POSTS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'body': 'Jack Kerouac',
        'author_id': '1234',
        'updated': datetime.now()
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'body': 'J. K. Rowling',
        'author_id': '1234',
        'updated': datetime.now()
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'body': 'Dr. Seuss',
        'author_id': '1234',
        'updated': datetime.now()
    }
]

@app.route('/posts', methods=['GET', 'POST'])
def all_posts():
    response_object = { 'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        POSTS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'body': post_data.get('body'),
            'author_id': post_data.get('author_id'),
            'updated': datetime.now()
        })
        response_object['message']  = 'post added!'
    else:
        response_object['posts'] = POSTS

    return jsonify(response_object)


@app.route('/posts/<post_id>', methods=['PUT', 'DELETE'])
def single_post(post_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        indexnum = ""
        post_data = request.get_json()
        # indexの検索
        for i, dic in enumerate(POSTS):
            if dic["id"] == post_id:
                index_num = i

        # POSTSに修正
        POSTS[index_num]["title"] = post_data.get('title')
        POSTS[index_num]["body"] = post_data.get('body')

        response_object['message'] = 'post updated!'

    if request.method == 'DELETE':
        remove_post(post_id)
        response_object['message'] = 'post removed!'

    return jsonify(response_object)


def remove_post(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return True
    return false

if __name__ == '__main__':
    app.run()
