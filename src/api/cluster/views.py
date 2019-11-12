import logging
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request
from flask import abort
from api.models import cluster as ClusterDBM

logger = logging.getLogger(__name__)


class ClusterManageView(Resource):

    def post(self, user_id):
        try:
            # req = {'cluster_name':'cluster_name', 'cluster_region':'cluster_region'}
            post_data = request.get_json()
            msg, resp_code = ClusterDBM.create_cluster(user_id, post_data['cluster_name'], post_data['cluster_region'])
            return msg, resp_code
        except BadRequest:
            logger.error('CreateCluster.post got bad request for args=%s' % request.data)
            return "POST Params cannot be identified", 400
        except KeyError:
            logger.error('CreateCluster.post got bad request since key not present for args=%s' % request.data)
            return "POST Params name key missing.", 400

    def put(self, **kwargs):
        try:
            # req = {'cluster_name':'cluster_name', 'cluster_region':'cluster_region'}
            # http://localhost:5000/api/cluster/update/cfce2d3d-db86-4b49-81fa-4dae30b61285
            cluster_id = kwargs.get('cluster_id')
            if not cluster_id:
                abort(404)
            else:
                data = request.get_json()
                msg, resp_code = ClusterDBM.update_cluster_info(cluster_id, data['cluster_name'], data['cluster_region'])
                return msg, resp_code
        except BadRequest:
            logger.error('CreateCluster.put got bad request for args=%s' % request.data)
            return "PUT Params cannot be identified", 400
        except KeyError:
            logger.error('CreateCluster.put got bad request since key not present for args=%s' % request.data)
            return "POST Params name key missing.", 400

    def delete(self, **kwargs):
        cluster_id = kwargs.get('cluster_id')
        data, resp_code = ClusterDBM.delete_cluster(cluster_id)
        return data, resp_code

    def get(self, user_id):
        data = ClusterDBM.get_cluster_from_user(user_id)
        resp = data if data else 'No Cluster created by the user'
        return resp, 200
