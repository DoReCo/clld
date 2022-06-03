import collections
import functools

import pyramid.config.routes
from pyramid.config import Configurator
from clld.web.app import menu_item
from clld.interfaces import IMapMarker, IValueSet, IValue, IDomainElement
from clldutils.svg import pie, icon, data_url

# we must make sure custom models are known at database initialization!
from dorelld import models

#from dorelld.interfaces import ILinkingAudio
#from dorelld.models import LinkingAudio


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
                         # ('audios', lambda c, r: (r.route_url('audio'),
                         #                         'audios')),
                         #('audio\'s', functools.partial(menu_item,
                         #                              'audio')),
                         )
    #config.register_resource('linkingAudio', LinkingAudio, ILinkingAudio)
    config.add_route('audio', '/audio')
    # Download link (see 'views.py')
    config.add_route('doreLoad', '/doreLoad')

    #config.add_404('/contributors');
    print(config.route_prefix)
    print(config.basepath)
    print(config.registry)
    return config.make_wsgi_app()
