from datetime import datetime, timedelta
from globals import config
import jwt
import models
import sqlalchemy as sa
from flask import Flask
import click
import logging


def create_engine():
	return sa.create_engine(config.DATABASE_URL)


def register_commands(app: Flask):

	@app.cli.command('create_tables')
	def create_tables():
		models.Base.metadata.create_all(create_engine())
		logging.info('Tables Created')

	@app.cli.command('drop_tables')
	def drop_tables():
		models.Base.metadata.drop_all(create_engine())
		logging.info('Tables Drop')

	@app.cli.command('truncate_tables')
	def truncate_tables():
		drop_tables()
		create_tables()
		logging.info('Tables Truncated')

	@app.cli.command('generate_admin_jwt')
	@click.argument('username')
	def generate_admin_jwt(username):
		token = None
		payload = {
			'username': username,
			'admin': True,
			'id': username,
			'iat': datetime.utcnow(),  # Issued at to know time JWT was issued
			'exp': datetime.utcnow() + timedelta(weeks=52),
			'nbf': datetime.utcnow(),  # Not before time
		}
		try:
			token = jwt.encode(payload, config.SECRET, algorithm='HS256')
		except Exception as e:
			print(e)
		logging.info('JWT Created it')
		click.echo(str(token.decode('utf-8')))
		return token.decode('utf-8')





