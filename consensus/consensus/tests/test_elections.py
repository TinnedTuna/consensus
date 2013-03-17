import unittest
import transaction
import uuid

from pyramid import testing

from pyramid.httpexceptions import HTTPOk

from webob.multidict import MultiDict

from consensus.models import (
    DBSession,
    Role,
    User,
    Election,
    Method,
    )

from consensus.views.user import (
    auth,
    )

from consensus.views.elections import (
    create_election,
    )

from consensus.authentication import (
    AuthenticationError,
    AuthenticationStrategy,
    Authentication,
    )

class TestElection(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.auth_strategy = AuthenticationStrategy()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from consensus.models import (
            Base,
            User,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            ballot_method = Method('TestMethod','Test Method','A test balloting method')
            model = User('TestUser','TestPass','TestSalt')
            role = Role('ROLE_USER', 'The default role for all users.')
            DBSession.add(ballot_method)
            DBSession.add(role)
            model.roles.append(DBSession.query(Role).filter_by(alias='ROLE_USER').first())
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_create_election_no_auth(self):
        request = testing.DummyRequest()
        response = create_election(request)
        self.assertEqual(response.status_int, 403)
        

    def test_create_election(self):
        request = testing.DummyRequest() 
        request.POST = MultiDict()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = auth(request)
        auth_session = request.session
        self.assertTrue(auth_session['authentication'].is_authenticated())
        request = testing.DummyRequest() 
        request.session = auth_session
        request.POST = MultiDict()
        request.POST['name'] = 'Test'
        request.POST['body'] = 'An election for testing.'
        request.POST['method'] = 'TestMethod'
        response = create_election(request)
        self.assertEqual(response.status_int, 302)
