import json

from django.test import TestCase, Client

from joke.models import User, Joke


class GenerateTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_auth(self):
        users = User.objects.all()
        self.assertEqual(0, len(users))
        response = self.client.get(
            path='/jokes/generate/',
        )
        self.assertEquals(200, response.status_code)
        users = User.objects.all()
        self.assertEqual(1, len(users))

    def test_generate(self):
        response = self.client.get(
            path='/jokes/generate/',
        )
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json())


class JokeTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_update_valid(self):
        user = User.objects.create(address='127.0.0.1')
        joke = Joke.objects.create(text='Some funny joke', user=user)
        new_joke_text = 'New funny joke'
        response = self.client.put(
            path='/jokes/{}/'.format(joke.id),
            data=json.dumps({
                'text': new_joke_text
            }),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        joke = Joke.objects.get(id=joke.id).text
        self.assertEqual(new_joke_text, joke)

    def test_update_invalid_id(self):
        new_joke_text = 'Here should be error'
        response = self.client.put(
            path='/jokes/100500/',
            data=json.dumps({
                'text': new_joke_text
            }),
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)
        response = json.loads(response.json())
        self.assertEqual(response['error_message'], 'Item not exist')

    def test_update_no_permissions(self):
        user = User.objects.create(address='127.0.0.1')
        joke = Joke.objects.create(text='Some funny joke', user=user)
        another_user = User.objects.create(address='888.888.111.111')
        another_joke = Joke.objects.create(text='New joke', user=another_user)
        response = self.client.put(
            path='/jokes/{}/'.format(another_joke.id),
            data=json.dumps({
                'text': 'Error?'
            }),
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)
        response = json.loads(response.json())
        self.assertEqual(response['error_message'],
                         'Have no permission to update')

    def test_update_incorrect_request(self):
        response = self.client.put(
            path='/jokes/1/',
            data=json.dumps({
                'TeXt': 'Error!!!'
            }),
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)
        response = json.loads(response.json())
        self.assertEqual(response['error_message'],
                         'Send json is not valid')

    def test_delete_valid(self):
        user = User.objects.create(address='127.0.0.1')
        joke = Joke.objects.create(text='Some funny joke', user=user)
        response = self.client.delete(
            path='/jokes/{}/'.format(joke.id)
        )
        self.assertEqual(200, response.status_code)

    def test_delete_invalid_id(self):
        response = self.client.delete(
            path='/jokes/100500/'
        )
        self.assertEqual(400, response.status_code)
        response = json.loads(response.json())
        self.assertEqual(response['error_message'], 'Item not exist')

    def test_delete_no_permissions(self):
        user = User.objects.create(address='127.0.0.1')
        joke = Joke.objects.create(text='Some funny joke', user=user)
        another_user = User.objects.create(address='888.888.111.111')
        another_joke = Joke.objects.create(text='New joke', user=another_user)
        response = self.client.delete(
            path='/jokes/{}/'.format(another_joke.id)
        )
        self.assertEqual(400, response.status_code)
        response = json.loads(response.json())
        self.assertEqual(response['error_message'],
                         'Have no permission to delete')

    def test_get_user_jokes_valid(self):
        user = User.objects.create(address='127.0.0.1')
        jk1 = Joke.objects.create(text='First joke', user=user)
        jk2 = Joke.objects.create(text='Second joke', user=user)
        jk3 = Joke.objects.create(text='Third joke', user=user)

        response = self.client.get(
            path='/jokes/'
        )
        self.assertEqual(200, response.status_code)
        response_json = response.json()

        self.assertEqual(response_json['jokes'][0]['id'], jk1.id)

    def test_get_user_jokes_another(self):
        user = User.objects.create(address='127.0.0.1')
        joke = Joke.objects.create(text='Funny joke', user=user)
        another_user = User.objects.create(address='1.1.1.1')
        no_access_joke = Joke.objects.create(text='Another joke',
                                             user=another_user)
        response = self.client.get(
            path='/jokes/'
        )
        self.assertEqual(200, response.status_code)
        response_json = response.json()
        response_joke_ids = []
        for joke in response_json['jokes']:
            response_joke_ids.append(joke['id'])
        self.assertFalse(no_access_joke.id in response_json)
