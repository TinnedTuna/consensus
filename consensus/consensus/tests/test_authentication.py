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
    )

from consensus.views import auth

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
            model = User('TestUser','TestPass','TestSalt')
            role = Role('ROLE_USER', 'The default role for all users.')
            DBSession.add(role)
            model.roles.append(DBSession.query(Role).filter_by(alias='ROLE_USER').first())
            #DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_auth_strategy(self):
        request = testing.DummyRequest() 
        request.POST = MultiDict()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        auth_token = AuthenticationStrategy().authenticate(request)
        self.assertTrue(auth_token.is_authenticated())

    def test_auth_strategy_bad_pass(self):
        request = testing.DummyRequest() 
        request.POST = MultiDict()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'BadPass'
        with self.assertRaises(AuthenticationError):
            AuthenticationStrategy().authenticate(request)

    def test_auth_strategy_bad_pass(self):
        request = testing.DummyRequest() 
        request.POST = MultiDict()
        request.POST['username'] = 'BadUser'
        request.POST['password'] = 'TestPass'
        with self.assertRaises(AuthenticationError):
            AuthenticationStrategy().authenticate(request)


    def test_no_auth(self):
        request = testing.DummyRequest()
        request.POST = MultiDict()
        response = auth(request)
        self.assertEqual(response.status_int, 401)

    def test_auth_actual(self):
        request = testing.DummyRequest()
        request.POST = MultiDict()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = auth(request)
        self.assertEqual(response.status_int, 200)
        auth_token = request.session['authentication']
        self.assertEqual(auth_token.user.username, 'TestUser')
        self.assertTrue(auth_token.is_authenticated())


    def test_auth_view_bad_pass(self):
        request = testing.DummyRequest()
        request.POST = MultiDict()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'BadPass'
        response = auth(request)
        self.assertEqual(response.status_int, 401)
        auth_token = request.session['authentication']
        self.assertFalse(auth_token.is_authenticated())
