import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from routes.mapper import SubMapper
import ckan.model as model
import ckan.logic as logic
from ckan.common import c, request
get_action = logic.get_action

@toolkit.auth_allow_anonymous_access
def request_reset(context, data_dict=None):
    if request.method == 'POST':
        context = {'model': model,
                   'user': c.user}
        data_dict = {'id': request.params.get('user')}
        user_dict = get_action('user_show')(context, data_dict)
        if user_dict['state'] == 'pending':
            return {'success': False, 'msg': 'Only allowed users can get reset pass'}
    return {'success': True}


class AccessRequestsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IAuthFunctions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'accessrequests')

    def before_map(self, map):
        with SubMapper(map,
                       controller='ckanext.accessrequests.controller:AccessRequestsController') as m:
            m.connect('account_requests',
                      '/admin/account_requests',
                      action='account_requests')
            m.connect('request_account',
                      '/user/register',
                      action='request_account')
            m.connect('account_requests_management',
                      '/admin/account_requests_management',
                      action='account_requests_management')
        return map

    def after_map(self, map):
        return map

    def get_auth_functions(self):
        return {'request_reset': request_reset}



