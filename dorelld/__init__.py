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
        # Menu
    config.register_menu(('dataset', functools.partial(menu_item, 'dataset',
                          label='Home')),
                         ('about', lambda c, r: (r.route_url('about'),
                          'About')),
                         ('languages', functools.partial(menu_item,
                          'languages')),
                        )
        # Download link (see 'views.py')
    config.add_route('doreLoad','/doreLoad')
    return config.make_wsgi_app()
