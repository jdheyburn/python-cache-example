

import unittest


from app import app


class GreetingsTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_empty_greetings(self):
        # When
        response = self.app.get('/greetings')

        # Then
        self.assertEqual(404, response.status_code)
        self.assertEqual('No greetings were found',
                         response.get_data().decode('utf-8'))

    def test_greeting_too_short(self):
        # Given
        greeting = ' '

        # When
        response = self.app.post(f'/greetings/{greeting}')

        # Then
        self.assertEqual(400, response.status_code)
        self.assertEqual('Invalid greeting',
                         response.get_data().decode('utf-8'))

    def test_greeting_too_long(self):
        # Given
        greeting = 'HelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorld'

        # When
        response = self.app.post(f'/greetings/{greeting}')

        # Then
        self.assertEqual(400, response.status_code)
        self.assertEqual('Invalid greeting',
                         response.get_data().decode('utf-8'))

    def test_submit_greeting_and_retrieve(self):
        # Given
        greeting = 'Hello, World!'

        # When
        response = self.app.post(f'/greetings/{greeting}')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello, World!', response.get_data().decode('utf-8'))

        response = self.app.get(f'/greetings')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello, World!', response.get_data().decode('utf-8'))
