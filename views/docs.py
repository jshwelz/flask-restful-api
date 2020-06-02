from flask import Blueprint, jsonify
from flask import request
from globals import db, spec, config
import json
from permissions import token_verification

docs = Blueprint('docs', __name__)


@docs.route('/docs', methods=['GET'])
def get_documentation():
	title = 'Firefly Api'
	swagger_url = str(config.URL) + '/docs/swagger.json'
	return """<! doctype html><html><head>
		<link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css">
		<title>""" + title + """</title></head><body><div id="swagger-ui"></div><script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
		<!-- `SwaggerUIBundle` is now available on the page -->
		<script>const ui = SwaggerUIBundle({url: '""" + swagger_url + """',dom_id: '#swagger-ui',presets: [
		SwaggerUIBundle.presets.apis,
		SwaggerUIBundle.SwaggerUIStandalonePreset],
		layout: "BaseLayout"})</script></body></html>"""


@docs.route('/docs/swagger.json', methods=['GET'])
def get_swagger():
	return jsonify(spec.to_dict()), 200
