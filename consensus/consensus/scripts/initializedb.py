import os
import sys
import transaction
import uuid

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    User,
    Role,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = User('Tinned_Tuna','mypass','mysalt') 
        role_user = Role("ROLE_USER","The most basic role anyone can have")
        role_anon = Role("ROLE_ANON","Any unauthenticated user.")
        DBSession.add(model)
        DBSession.add(role_user)
        DBSession.add(role_anon)
