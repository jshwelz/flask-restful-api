from flask import Blueprint, jsonify
from flask import request
from globals import db
from models.Comics import ComicsModel
from permissions import token_verification
from schemas.comics import comic_schema


comics = Blueprint('comics', __name__)


@comics.route('/', methods=['GET'])
@token_verification
def get_comics():
	"""Comic list view.
	---
	get:
		summary: 'List all Comics'
		description: 'Returns all the comics'
		operationId: 'ListComics'
		responses:
			401:
				description: 'UnAuthorized'
			500:
				description: 'Server error'
			'200':
				content:
					application/json:
						schema: 'Comic'
				description: 'Comic Created'
				schema:
					$ref: '#/components/schemas/Comic'
	"""
	items = db.session.query(ComicsModel).all()
	comics_list = comic_schema.dump(items, many=True)
	return jsonify(comics_list), 200


@comics.route('/', methods=['POST'])
@token_verification
def create_comic():
	"""Comic view.
	---
	post:
		summary: 'Add a new comic to the store'
		description: ''
		operationId: 'AddComic'
		parameters:
		- in: 'body'
		  name: 'body'
		  description: ''
		  required: true
		  schema:
			$ref: '#/components/schemas/Comic'
		responses:
			500:
				description: 'Server Error'
			401:
				description: 'UnAuthorized'
			201:
				description: 'Comic Created'
				schema:
					$ref: '#/components/schemas/Comic'
	"""
	try:
		content = request.json
		data = comic_schema.load(content)
		db.session.add(data)
		db.session.flush()
	except Exception as e:
		db.session.rollback()
		return jsonify({'error message': str(e)}), 500
	return jsonify(comic_schema.dump(data)), 201


@comics.route('/<id>', methods=['PUT'])
@token_verification
def update_comic(id):
	"""Comic view.
	---
	put:
		summary: 'Update Existing Comic'
		description: ''
		operationId: 'UpdateComic'
		parameters:
		- in: 'body'
		  name: 'body'
		  description: ''
		  required: true
		  schema:
			$ref: '#/components/schemas/Comic'
		responses:
			500:
				description: 'Server Error'
			404:
				description: 'Comic could not be found'
			401:
				description: 'UnAuthorized'
			201:
				description: 'Comic Updated'
				schema:
					$ref: '#/components/schemas/Comic'
	"""
	item = db.session.query(ComicsModel).filter(ComicsModel.id == id).first()
	if not item:
		return jsonify({'error message': 'comic could not be found'}), 404
	data = request.json
	fields = comic_schema.dump(data)
	for (key, value) in fields.items():
		if value is not None:
			setattr(item, key, value)
	db.session.flush()
	return jsonify(fields), 200


@comics.route('/<id>', methods=['DELETE'])
@token_verification
def delete_comic(id):
	"""Comic detail view.
	---
	delete:
		summary: 'delete comic by ID'
		description: 'comic delete it'
		operationId: 'getComicByID'
		parameters:
		- name: 'id'
		  in: 'path'
		  description: 'ID of comic to delete'
		  required: true
		  type: 'integer'
		responses:
			401:
				description: 'UnAuthorized'
			404:
				description: 'Comic not found'
			'200':
				content:
					application/json:
						schema: 'Comic'
				description: 'Comic delete it'
	"""
	item = db.session.query(ComicsModel).filter(ComicsModel.id == id).first()
	if not item:
		return jsonify({'error message': 'comic could not be found'}), 404
	db.session.delete(item)
	db.session.flush()
	return jsonify('True'), 200


@comics.route('/<id>', methods=['GET'])
@token_verification
def get_comic_by_id(id):
	"""Comic detail view.
	---
	get:
		summary: 'Find comic by ID'
		description: 'Returns a single comic'
		operationId: "getComicByID"
		parameters:
		- name: 'id'
		  in: 'path'
		  description: 'ID of comic to return'
		  required: true
		  type: 'integer'
		responses:
			401:
				description: 'UnAuthorized'
			404:
				description: 'Comic not found'
			'200':
				content:
					application/json:
						schema: 'Comic'
				description: 'Comic Created'
				schema:
					$ref: '#/components/schemas/Comic'
	"""
	item = db.session.query(ComicsModel).filter(ComicsModel.id == id).first()
	if not item:
		return jsonify({'error message': 'comic could not be found'}), 404
	return jsonify(comic_schema.dump(item)), 200
