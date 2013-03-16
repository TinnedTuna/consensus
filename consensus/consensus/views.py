from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    )

@view_config(route_name='home', renderer='templates/login.pt')
def login(request):
  return {}

@view_config(route_name="auth", renderer='templates/auth.pt')
def auth(request):
  try: 
    authenticated = request.session['authenticated']
  except KeyError:
    authenticated = False;
  username = request.POST.getone('username')
  password = request.POST.getone('password')
  return {'authentication':authenticated, \
          'username' : username, \
          'password' : password}
  

#@view_config(route_name='authenticate' renderer='templaters/auth.py')
#def authenticate(request):
#  username = request.
conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_consensus_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

