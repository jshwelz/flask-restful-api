#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jwt
from flask import request, jsonify
from functools import wraps
from globals import config


def token_verification(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		token = None
		if 'Authorization' in request.headers:
			token = request.headers['Authorization']
			scheme, token = token.split()
		if not token:
			return jsonify({'message': 'a valid token is missing'}), 401
		try:
			data = jwt.decode(token, config.SECRET)
		except Exception as e:
			return jsonify({'message': 'token is invalid'}), 401
		return f(*args, **kwargs)
	return decorator


def get_user_from_token(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		token = None
		if 'Authorization' in request.headers:
			token = request.headers['Authorization']
			scheme, token = token.split()
		if not token:
			return jsonify({'message': 'a valid token is missing'})
		try:
			data = jwt.decode(token, config.SECRET)
		except Exception as e:
			return jsonify({'message': 'token is invalid'}), 401
		return f(data, *args,  **kwargs)
	return decorator
