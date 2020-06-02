#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
# Extend base table with "object" class to inject some defaults
class Base(object):

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()

	# extend_existing: When True, indicates that if this Table is already present in the given MetaData,
	#                  apply further arguments within the constructor to the existing Table.
	__table_args__ = {'extend_existing': True}
	id = Column(Integer, primary_key=True)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=func.now(), onupdate=datetime.now)
