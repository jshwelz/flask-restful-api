#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import json
from app import init_app
from globals import config
from sqlalchemy_utils import database_exists, drop_database

runner = init_app().test_cli_runner()
admin_token = runner.invoke(args=['generate_admin_jwt', 'josh']).output

# scope: Run once per test function. The setup portion is run before each test using the fixture.
# autouse: Invoke fixture automatically without declaring a function argument explicitly.
@pytest.fixture(scope='function', autouse=True)
def setup_api(request):
	# Init HTTP web server
	app = init_app()
	# Create and delete database
	if not database_exists(config.DATABASE_URL):
		runner.invoke(args=['create_tables'])

	def tear_down():
		drop_database(config.DATABASE_URL)

	request.addfinalizer(tear_down)
	testing_client = app.test_client()
	return testing_client


def test_create_comic(setup_api):
	comic = {
		'publisher': 'DC Comics',
		'title': 'Batman Year One',
		'number': '1',
		'type': 'Comic',
		'vol': '1',
		'year': '1984'}

	headers = {'Authorization': 'Bearer ' + admin_token.rstrip()}
	response = setup_api.post('/comics', data=json.dumps(comic), follow_redirects=True,
								content_type='application/json', headers=headers)
	response_message = json.loads(response.data.decode('utf-8'))
	assert response.status_code == 201
	assert response_message['publisher'] == 'DC Comics'
	assert response_message['title'] == 'Batman Year One'


def test_list_comics(setup_api):
	comic = {
		'publisher': 'DC Comics',
		'title': 'Batman Year One',
		'number': '1',
		'type': 'Comic',
		'vol': '1',
		'year': '1984'}

	headers = {'Authorization': 'Bearer ' + admin_token.rstrip()}
	response = setup_api.post('/comics', data=json.dumps(comic), follow_redirects=True,
								content_type='application/json', headers=headers)
	assert response.status_code == 201

	comic = {
		'publisher': 'Marvel',
		'title': 'Adventures of Cyclops and Phoenix',
		'number': '1',
		'type': 'Comic',
		'vol': '1',
		'year': '1999'}

	response = setup_api.post('/comics', data=json.dumps(comic), follow_redirects=True,
								content_type='application/json', headers=headers)
	assert response.status_code == 201

	response = setup_api.get('/comics', follow_redirects=True,
								content_type='application/json', headers=headers)
	assert response.status_code == 200
	response_message = json.loads(response.data.decode('utf-8'))

	assert response_message == [
		{
			'box': None,
			'id': 1,
			'condition': None,
			'copies': None,
			'publication': None,
			'publisher': 'DC Comics',
			'title': 'Batman Year One',
			'number': 1,
			'type': 'Comic',
			'vol': 1,
			'year': 1984
		},
		{
			'box': None,
			'id': 2,
			'condition': None,
			'copies': None,
			'publication': None,
			'publisher': 'Marvel',
			'title': 'Adventures of Cyclops and Phoenix',
			'number': 1,
			'type': 'Comic',
			'vol': 1,
			'year': 1999
		}
	]


def test_get_comic_by_id(setup_api):
	comic = {
		'publisher': 'DC Comics',
		'title': 'Batman Year One',
		'number': '1',
		'type': 'Comic',
		'vol': '1',
		'year': '1984'}

	headers = {'Authorization': 'Bearer ' + admin_token.rstrip()}
	response = setup_api.post('/comics', data=json.dumps(comic), follow_redirects=True,
								content_type='application/json', headers=headers)
	response_message = json.loads(response.data.decode('utf-8'))
	id = response_message['id']

	response = setup_api.get('/comics/' + str(id), follow_redirects=True,
								content_type='application/json', headers=headers)
	response_message = json.loads(response.data.decode('utf-8'))
	assert response.status_code == 200
	assert response_message['publisher'] == 'DC Comics'
	assert response_message['title'] == 'Batman Year One'


def test_update_comic(setup_api):
	comic = {
		'publisher': 'DC Comics',
		'title': 'Batman Year One',
		'number': '1',
		'type': 'Comic',
		'vol': '1',
		'year': '1984'}

	headers = {'Authorization': 'Bearer ' + admin_token.rstrip()}
	response = setup_api.post('/comics', data=json.dumps(comic), follow_redirects=True,
								content_type='application/json', headers=headers)
	assert response.status_code == 201

	comic = {
		'publisher': 'DC Comics',
		'title': 'Batman Dark Knight Returns',
		'number': '1',
		'type': 'Comic',
		'vol': '1',
		'year': '1982'}

	response = setup_api.put('/comics/1', data=json.dumps(comic), follow_redirects=True,
								content_type='application/json', headers=headers)
	assert response.status_code == 200
	response_message = json.loads(response.data.decode('utf-8'))
	assert response_message['publisher'] == 'DC Comics'
	assert response_message['title'] == 'Batman Dark Knight Returns'


def test_delete_comic(setup_api):
	comic = {
		'publisher': 'DC Comics',
		'title': 'Batman Year One',
		'number': '1',
		'type': 'Comic',
		'vol': '1',
		'year': '1984'}

	headers = {'Authorization': 'Bearer ' + admin_token.rstrip()}
	response = setup_api.post('/comics', data=json.dumps(comic), follow_redirects=True,
								content_type='application/json', headers=headers)
	assert response.status_code == 201

	response = setup_api.delete('/comics/1', data=json.dumps(comic), follow_redirects=True,
								content_type='application/json', headers=headers)
	assert response.status_code == 200
