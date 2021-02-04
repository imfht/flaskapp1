# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2016 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""
import unittest

import flask
from packaging import version
from ..base_test import FlaskCorsTestCase
from flask import Flask, abort
from flask_cors import *
from flask_cors.core import *


def add_routes(app):
    @app.route('/test_no_acl_abort_404')
    @app.route('/test_acl_abort_404')
    def test_acl_abort_404():
        abort(404)

    @app.route('/test_no_acl_abort_500')
    @app.route('/test_acl_abort_500')
    def test_acl_abort_500():
        abort(500)

    @app.route('/test_acl_uncaught_exception_500')
    def test_acl_uncaught_exception_500():
        raise Exception("This could've been any exception")

    @app.route('/test_no_acl_uncaught_exception_500')
    def test_no_acl_uncaught_exception_500():
        raise Exception("This could've been any exception")


class ExceptionInterceptionDefaultTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app, resources={
            r'/test_acl*': {},
        })
        add_routes(self.app)

    def test_acl_abort_404(self):
        '''
            HTTP Responses generated by calling abort are handled identically
            to normal responses, and should be wrapped by CORS headers if thep
            path matches. This path matches.

        '''
        resp = self.get('/test_acl_abort_404', origin='www.example.com')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(ACL_ORIGIN in resp.headers)

    def test_no_acl_abort_404(self):
        '''
            HTTP Responses generated by calling abort are handled identically
            to normal responses, and should be wrapped by CORS headers if thep
            path matches. This path does not match.
        '''
        resp = self.get('/test_no_acl_abort_404', origin='www.example.com')
        self.assertEqual(resp.status_code, 404)
        self.assertFalse(ACL_ORIGIN in resp.headers)

    def test_acl_abort_500(self):
        '''
            HTTP Responses generated by calling abort are handled identically
            to normal responses, and should be wrapped by CORS headers if thep
            path matches. This path matches
        '''
        resp = self.get('/test_acl_abort_500', origin='www.example.com')
        self.assertEqual(resp.status_code, 500)
        self.assertTrue(ACL_ORIGIN in resp.headers)

    def test_no_acl_abort_500(self):
        '''
            HTTP Responses generated by calling abort are handled identically
            to normal responses, and should be wrapped by CORS headers if thep
            path matches. This path matches
        '''
        resp = self.get('/test_no_acl_abort_500', origin='www.example.com')
        self.assertEqual(resp.status_code, 500)
        self.assertFalse(ACL_ORIGIN in resp.headers)

    def test_acl_uncaught_exception_500(self):
        '''
            Uncaught exceptions will trigger Flask's internal exception
            handler, and should have ACL headers only if intercept_exceptions
            is set to True and if the request URL matches the resources pattern

            This url matches.
        '''

        resp = self.get('/test_acl_uncaught_exception_500', origin='www.example.com')
        self.assertEqual(resp.status_code, 500)
        self.assertTrue(ACL_ORIGIN in resp.headers)

    def test_no_acl_uncaught_exception_500(self):
        '''
            Uncaught exceptions will trigger Flask's internal exception
            handler, and should have ACL headers only if intercept_exceptions
            is set to True and if the request URL matches the resources pattern.

            This url does not match.
        '''

        resp = self.get('/test_no_acl_uncaught_exception_500', origin='www.example.com')
        self.assertEqual(resp.status_code, 500)
        self.assertFalse(ACL_ORIGIN in resp.headers)

    def test_acl_exception_with_error_handler(self):
        '''
            If a 500 handler is setup by the user, responses should have
            CORS matching rules applied, regardless of whether or not
            intercept_exceptions is enbaled.
        '''
        return_string = "Simple error handler"

        @self.app.errorhandler(404)
        @self.app.errorhandler(500)
        def catch_all_handler(error):
            '''
                This error handler catches 404s and 500s and returns
                status 200 no matter what. It is not a good handler.
            '''
            return return_string, 200

        acl_paths = [
            '/test_acl_abort_404',
            '/test_acl_abort_500',
            'test_acl_uncaught_exception_500'
        ]
        no_acl_paths = [
            '/test_no_acl_abort_404',
            '/test_no_acl_abort_500',
            'test_no_acl_uncaught_exception_500'
        ]

        def get_with_origins(path):
            return self.get(path, origin='www.example.com')

        for resp in map(get_with_origins, acl_paths):
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(ACL_ORIGIN in resp.headers)

        for resp in map(get_with_origins, no_acl_paths):
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(ACL_ORIGIN in resp.headers)


class NoExceptionInterceptionTestCase(ExceptionInterceptionDefaultTestCase):

    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app,
             intercept_exceptions=False,
             resources={
                 r'/test_acl*': {},
             })
        add_routes(self.app)

    def test_acl_exception_with_error_handler(self):
        '''
            If a 500 handler is setup by the user, responses should have
            CORS matching rules applied, regardless of whether or not
            intercept_exceptions is enbaled.
        '''
        return_string = "Simple error handler"

        @self.app.errorhandler(404)
        @self.app.errorhandler(500)
        def catch_all_handler(error):
            '''
                This error handler catches 404s and 500s and returns
                status 200 no matter what. It is not a good handler.
            '''
            return return_string, 200

        acl_paths = [
            '/test_acl_abort_404',
            '/test_acl_abort_500',
        ]
        no_acl_paths = [
            '/test_no_acl_abort_404',
            '/test_no_acl_abort_500',
            'test_no_acl_uncaught_exception_500'
            'test_acl_uncaught_exception_500'
        ]
        def get_with_origins(path):
            return self.get(path, origin='www.example.com')

        for resp in map(get_with_origins, acl_paths):
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(ACL_ORIGIN in resp.headers)

        for resp in map(get_with_origins, no_acl_paths):
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(ACL_ORIGIN in resp.headers)

    @unittest.skipIf(version.parse(flask.__version__) >= version.parse("1.1"),
                     "Flask 1.1 changed interception behavior, so after request handlers are always run. "
                     "This obviates the need for our hacky interception")
    def test_acl_uncaught_exception_500(self):
        '''
            Uncaught exceptions will trigger Flask's internal exception
            handler, and should have ACL headers only if intercept_exceptions
            is set to True. In this case it is not.
        '''
        resp = self.get('/test_acl_uncaught_exception_500', origin='www.example.com')
        self.assertEqual(resp.status_code, 500)
        self.assertFalse(ACL_ORIGIN in resp.headers)

if __name__ == "__main__":
    unittest.main()