import transaction 

from pyramid.response import Response

from pyramid.view import view_config

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPFound,
    HTTPForbidden,
    HTTPUnauthorized,
    HTTPOk,
    )

from sqlalchemy.exc import (
    DBAPIError,
    IntegrityError
    )

from consensus.models import (
    DBSession,
    User,
    Role,
    )

from consensus.authentication import (
    AuthenticationStrategy,
    AuthenticationError,
    Authentication,
    )


@view_config(route_name='create_election', renderer='templates/create_election.py')
def create_election(request):
    try:
        auth_token = request.session['authentication']
    except KeyError:
        return HTTPForbidden()
        


@view_config(route_name='signup', renderer='templates/signup.pt')
def signup(request):
    try:
        username = request.POST.getone('username')
        password = request.POST.getone('password')
    except KeyError: 
        return HTTPBadRequest()
    new_user = User(username,password,"salt")
    role_user = DBSession.query(Role).filter_by(alias='ROLE_USER').first()
    try:
        with transaction.manager:
             DBSession.add(new_user)
             user = DBSession.query(User).filter_by(username=username).first()
             user.roles.append(role_user)
    except IntegrityError:
        return HTTPBadRequest()
    return HTTPOk()
    
    
    
        
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

