#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class Config:
	APP_NAME = os.environ.get('APP_NAME', str('Comics Api'))
	BRANCH_NAME = os.environ.get('BRANCH_NAME', str('develop'))
	DATABASE_URL = os.environ.get('DATABASE_URL', str('sqlite:///test.db'))
	ENVIRONMENT = os.environ.get('ENVIRONMENT', str('local'))
	SECRET = os.environ.get('SECRET', str('foobar'))
	DEBUG = os.environ.get('DEBUG', bool(
		True))  # IMPORTANT: this must be set 'False' for production security of GET /token !!!
	URL = os.environ.get('URL', str('http://127.0.0.1:5000/'))
