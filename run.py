#!/usr/bin/env python3

from flask import Flask, Response
import json

from users.blueprint import users_routes
from groups.blueprint import groups_routes
from messages.blueprint import messages_routes

app = Flask(__name__)
app.register_blueprint(users_routes)
app.register_blueprint(groups_routes)
app.register_blueprint(messages_routes)

@app.route('/')
def index():
    return Response(
        json.dumps({
            'app': 'Message System',
            'version': 0.1
        }),
        200,
        content_type = 'application/json'
    )

if __name__ == '__main__':
    app.run(debug = True)