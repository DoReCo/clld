import functools
from pyramid.config import Configurator
from clld.web.app import menu_item
# we must make sure custom models are known at database initialization!
from dorelld import models

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')
    config.register_menu(('dataset', functools.partial(menu_item, 'dataset',
                          label='Home')),
                         ('about', lambda c, r: (r.route_url('about'),
                          'about')),
                         ('languages', functools.partial(menu_item,
                          'languages')),
                         ('sources', functools.partial(menu_item, 'sources')),
                        )
    return config.make_wsgi_app()
