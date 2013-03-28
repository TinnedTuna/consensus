import transaction 
import json
import uuid

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
    Method,
    Election,
    )

from consensus.authentication import (
    AuthenticationStrategy,
    AuthenticationError,
    Authentication,
    )

def is_authenticated(request):
    try:
        auth_token = request.session['authentication']
        return auth_token.is_authenticated()
    except KeyError:
        return False

@view_config(route_name='create_electionp', renderer='templates/create_election.mako')
def create_election(request):
    if (not is_authenticated(request)):
        return HTTPUnauthorized()
    try:
        election_name = request.POST.getone('name')
        election_desc = request.POST.getone('body')
        method = request.POST.getone('method')
    except KeyError:
        return HTTPBadRequest()
    read_method = DBSession.query(Method).filter_by(python_name=method).first()
    if (read_method is None):
        return HTTPBadRequest()
    election = Election(election_name, election_desc, read_method)
    with transaction.manager:
        new_id = DBSession.add(election)
    return HTTPFound(location=request.route_url('view_election', id=new_id))
        
@view_config(route_name='view_all_elections', renderer='all_elections.mako')
def view_all_elections(request):
    if (not is_authenticated(request)):
        return HTTPUnauthorized()
    elections = DBSession.query(Election).all()
    elections = {}
    result = {}
    for election in elections:
        elections[election.name] = {'view_url'  : request.route_url('view_election', id=election.id.urn), \
                                 'name': election.name \
                                }
    result['page_name'] = 'All Elections' 
    result['elections'] = elections
    return result

@view_config(route_name='view_election', renderer='election.mako')
def view_election(request):
    if (not is_authenticated(request)):
        return HTTPUnauthorized()
    try:
        election_id = uuid.UUID(request.matchdict['id'])
    except KeyError, ValueError:
        raise HTTPBadRequest()
    
    election = DBSession.query(Election).filter_by(id=election_id).first()
    return { 'id' : election.id.urn, \
             'page_name' : election.name, \
             'name' : election.name, \
             'body' : election.body, \
             'method' : { 'name' : election.method.name, \
                          'description' : election.method.description } }  

    
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

