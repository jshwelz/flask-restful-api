#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__version__ = '1.0.0'
__license__ = 'MIT'
__author__ = 'Josh Welchez'
__email__ = 'josh.welchez@gmail.com'


from flask import Flask, jsonify
from globals import db, config
from commands import register_commands
import routes


def init_app():
    app = Flask(__name__)
    db.connect()
    app.config['SECRET_KEY'] = config.SECRET

    @app.route('/')
    def hello_world():
        return 'Comics Api'

    routes.initialize_routes(app)
    register_commands(app)
    return app


app = init_app()

if __name__ == '__main__':
    app.run()
