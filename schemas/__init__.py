#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from schemas.comics import Comic
from globals import spec

spec.components.schema("Comic", schema=Comic)
