from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings)
    config.include('pyramid_beaker')
    config.set_session_factory(session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include(routes_setup)
    config.scan()
    return config.make_wsgi_app()

def routes_setup(config):
    # Out here for unittest
    config.add_route('login', '/login', request_method='GET')
    config.add_route('auth', '/authenticate', request_method='POST')
    config.add_route('signupp', '/signup', request_method='POST')
    config.add_route('signup', '/signup', request_method='GET')
    config.add_route('create_electionp', '/create_election', request_method='POST')
    config.add_route('create_election', '/create_election', request_method='GET')
    config.add_route('view_all_elections','/elections')
    config.add_route('view_election','/election/{election_id}', request_method='GET')
 
