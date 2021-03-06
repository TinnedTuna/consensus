import unittest
import transaction
import uuid

from bkrypt import Password

from pyramid import testing

from pyramid.httpexceptions import HTTPOk

from webob.multidict import MultiDict

from consensus.models import (
    DBSession,
    Role,
    User,
    )

from consensus.views.user import auth

from consensus.authentication import (
    AuthenticationError,
    AuthenticationStrategy,
    Authentication,
    )

class TestAuthentication(unittest.TestCase):
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
            model = User('TestUser',str(Password.create('TestPass')))
            role = Role('ROLE_USER', 'The default role for all users.')
            DBSession.add(role)
            model.roles.append(DBSession.query(Role).filter_by(alias='ROLE_USER').first())
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def _get_request(self):
        self.config.include('consensus.routes_setup')
        request = testing.DummyRequest()
        request.POST = MultiDict()
        return request

    def test_auth_strategy(self):
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        auth_token = AuthenticationStrategy().authenticate(request)
        self.assertTrue(auth_token.is_authenticated())

    def test_auth_strategy_bad_pass(self):
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'BadPass'
        with self.assertRaises(AuthenticationError):
            AuthenticationStrategy().authenticate(request)

    def test_auth_strategy_no_pass(self):
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        with self.assertRaises(AuthenticationError):
            AuthenticationStrategy().authenticate(request)

    def test_auth_strategy_bad_pass(self):
        request = self._get_request()
        request.POST['username'] = 'BadUser'
        request.POST['password'] = 'TestPass'
        with self.assertRaises(AuthenticationError):
            AuthenticationStrategy().authenticate(request)


    def test_no_auth(self):
        request = self._get_request()
        response = auth(request)
        self.assertEqual(response.status_int, 401)

    def test_auth_actual(self):
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = auth(request)
        self.assertEqual(response.status_int, 302)
        auth_token = request.session['authentication']
        self.assertEqual(auth_token.user.username, 'TestUser')
        self.assertTrue(auth_token.is_authenticated())


    def test_auth_view_bad_pass(self):
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'BadPass'
        response = auth(request)
        self.assertEqual(response.status_int, 401)
        auth_token = request.session['authentication']
        self.assertFalse(auth_token.is_authenticated())
