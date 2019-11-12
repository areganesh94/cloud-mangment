import logging
from flask_restful import Resource
from api.models import user as UserDBM
from werkzeug.exceptions import BadRequest
from flask import request

logger = logging.getLogger(__name__)


class AddProfileUser(Resource):

	def post(self):
		# req: { "name": "foo"}
		try:
			data = request.get_json()
			response, code = UserDBM.create_user(data['name'])
			return response, code
		except BadRequest:
			logger.error('AddProfileUser.post got bad request for args=%s' % request.data)
			return "POST Params cannot be identified", 400
		except KeyError:
			logger.error('AddProfileUser.post got bad request since key not present for args=%s' % request.data)
			return "POST Params name key missing.", 400
