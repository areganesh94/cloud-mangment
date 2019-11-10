import logging
import pkgutil
from importlib import import_module
from flask.blueprints import Blueprint
from flask_restful import Api

logger = logging.getLogger(__name__)

class RegisterApp:

    def __init__(self, sub_apps):
        self.app_list = sub_apps
        self._auto_discover_blueprints()

    def _auto_discover_blueprints(self):
        blueprints = []
        for app_name in self.app_list:
            for module_name in self.get_app_modules(self.get_app_path(app_name)):
                try:
                    blueprints.append(self.create_api_blueprint(app_name, module_name))
                except Exception as e:
                    logger.warn('Exception while auto discovering %(app_name)s.%(module_name)s: %(exc_type)s (%(msg)s)' % {
                        'app_name': app_name,
                        'module_name': module_name,
                        'exc_type': e.__class__.__name__,
                        'msg': str(e),
                    })
        return blueprints

    def get_app_path(self, app_name):
        return app_name.replace('.','/')

    def get_app_modules(self, app_path):
        return [pkg[1] for pkg in pkgutil.iter_modules([app_path]) if pkg[2] == True]

    def create_api_blueprint(self, app_name, module_name):
        blueprint = Blueprint(self.get_blueprint_name(app_name, module_name), self.get_module_import_name(app_name, module_name, 'views'))
        api = Api(blueprint, prefix=self.get_api_path_prefix(self.get_app_path(app_name), module_name))
        url_module = import_module(self.get_module_import_name(app_name, module_name, 'urls'))
        for view,urls in url_module.urls.items():
            api.add_resource(view, *urls)        
        return blueprint

    def get_blueprint_name(self, app_name, module_name):
        return '__'.join([app_name,module_name])

    def get_module_import_name(self, app_name, module_name, sub_module):
        return '.'.join([app_name, module_name, sub_module])

    def get_api_path_prefix(self, app_path, module_name):
        return '/'.join(['', app_path, module_name, ''])