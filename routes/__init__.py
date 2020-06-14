#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from views.comics import comics
from views.docs import docs
from globals import spec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.yaml_utils import load_operations_from_docstring


def initialize_routes(api):
    api.register_blueprint(comics, url_prefix='/comics')
    api.register_blueprint(docs)

    with api.test_request_context():
        for r in api.url_map.iter_rules():
            view = api.view_functions.get(r.endpoint)
            operations = load_operations_from_docstring(view.__doc__)
            path = FlaskPlugin.flaskpath2openapi(r.rule)
            if not operations:
                continue
            # De-reference the schemas referenced in the docstring.
            for verb in operations:
                resp = operations.get(verb).get('responses')
                for status in resp:
                    val = resp.get(status)
                    content = resp.get(status).get('schema')
                    if content:
                        pass
            # Add paths to the spec
            spec.path(view=view, path=path, operations=operations)
