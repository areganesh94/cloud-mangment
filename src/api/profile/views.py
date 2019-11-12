import logging
from flask_restful import Resource
from api.models import user as UserDBM
from werkzeug.exceptions import BadRequest
from flask import request

logger = logging.getLogger(__name__)


class AddProfileUser(Resource):

	def post(self):
		try:
			data = request.get_json()
			is_created = UserDBM.create_user(data['name'])
			response = ('User Created Successfully', 201) if is_created else ('User Not Created Successfully', 503)
			return response
		except BadRequest:
			logger.error('AddProfileUser.post got bad request for args=%s' % request.data)
			return "POST Params cannot be identified", 400
