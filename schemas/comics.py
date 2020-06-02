#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from marshmallow import fields, post_load
from marshmallow.schema import Schema
from models.Comics import ComicsModel


class Comic(Schema):
	id = fields.Int(dump_only=True)
	publication = fields.Integer()
	publisher = fields.String(required=True)
	title = fields.String(required=True)
	number = fields.Integer(required=True)
	vol = fields.Integer()
	year = fields.Integer()
	type = fields.String()
	condition = fields.String()
	box = fields.Integer()
	copies = fields.Integer()
	# @post_load: Register a method to invoke after deserializing an object.
	#             The method receives the deserialized data and returns the processed data.

	@post_load
	def make_comic(self, data,  **kwargs):
		return ComicsModel(**data)


comic_schema = Comic()
