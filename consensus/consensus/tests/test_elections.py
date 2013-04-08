import unittest
import transaction
import uuid

from pyramid import testing

from pyramid.httpexceptions import HTTPOk

from pyramid.request import Request

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
    view_all_elections,
    view_election,
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


    def _get_request(self):
        self.config.include('consensus.routes_setup')
        req = testing.DummyRequest()
        req.POST = MultiDict()
        return req

    def test_create_election_no_auth(self):
        request = self._get_request()
        response = create_election(request)
        self.assertEqual(response.status_int, 401)
        

    def test_create_election(self):
        request = self._get_request() 
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = auth(request)
        auth_session = request.session
        self.assertTrue(auth_session['authentication'].is_authenticated())
        request = self._get_request() 
        request.session = auth_session
        request.POST['name'] = 'Test'
        request.POST['body'] = 'An election for testing.'
        request.POST['method'] = 'TestMethod'
        response = create_election(request)
        self.assertEqual(response.status_int, 302)

   
    def test_view_elections(self):
        request = self._get_request() 
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = auth(request)
        auth_session = request.session
        self.assertTrue(auth_session['authentication'].is_authenticated())
        request = self._get_request()
        request.session = auth_session
        request.POST['name'] = 'Test'
        request.POST['body'] = 'An election for testing.'
        request.POST['method'] = 'TestMethod'
        response = create_election(request)
        self.assertEqual(response.status_int, 302)
        request = self._get_request()
        request.session = auth_session
        response = view_all_elections(request)
        self.assertEqual(len(response['elections']), 1)
        self.assertEqual(response['Test']['name'], 'Test')

    def test_view_election(self):
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = auth(request)
        auth_session = request.session
        self.assertTrue(auth_session['authentication'].is_authenticated())
        request = self._get_request()
        request.session = auth_session
        request.POST['name'] = 'Test'
        request.POST['body'] = 'An election for testing.'
        request.POST['method'] = 'TestMethod'
        response = create_election(request)
        self.assertEqual(response.status_int, 302)
        requet = self._get_request()
        request.session = auth_session
        response = view_all_elections(request)
        self.assertEqual(len(response), 3)
        self.assertEqual(response['Test']['name'], 'Test')
        self._get_request()
        request.session = auth_session
        request.url = response['Test']['view_url']
        print(request.url)
        print(response['Test']['view_url'])
        response = view_election(request)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response['name'], 'Test')
        self.assertEqual(response['body'], 'An election for testing.')
        self.assertEqual(response['method']['name'], 'Test Method')
