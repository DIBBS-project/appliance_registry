import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient

from . import models

class TestSiteObject(TestCase):
    def test_basic(self):
        # no foreign keys...this one is kinda boring.
        models.Site.objects.create(
            name='asdf',
            type='asdf',
            api_url='asdf',
        )


class TestSiteAccess(TestCase):
    def setUp(self):
        User = get_user_model()
        self.rfclient = APIClient()

        username = 'alice'
        password = 'ALICE'
        self.user = User.objects.create_superuser(
            username,
            '{}@example.com'.format(username),
            password,
        )

        self.rfclient.force_authenticate(user=self.user)

    def test_list(self):
        some_site = models.Site.objects.create(
            name='asdf',
            type='asdf',
            api_url='asdf',
        )

        response = self.rfclient.get('/sites/')
        assert 200 <= response.status_code < 300, (response.status_code, response.content)
        rtext = response.content.decode(response.charset)
        data = json.loads(rtext)
        self.assertEqual(len(data), 1)

        models.Site.objects.create(name='zxcv', type='zxcv', api_url='zxcv')
        self.assertEqual(len(self.rfclient.get('/sites/').json()), 2)

    def test_create(self):
        response = self.rfclient.post('/sites/', format='json', data={
            'name': 'a_name',
            'type': 'a_type',
            'api_url': 'a_url',
        })
        assert response.status_code == 201, (response.status_code, response.content)


class TestApplianceObject(TestCase):
    def setUp(self):
        User = get_user_model()
        username = 'alice'
        password = 'ALICE'
        self.user = User.objects.create_superuser(
            username,
            '{}@example.com'.format(username),
            password,
        )

    def test_basic(self):
        models.Appliance.objects.create(
            name='basic',
            owner=self.user,
            description='hello world!',
        )


class TestApplianceAccess(TestCase):
    endpoint = '/appliances/'

    def setUp(self):
        User = get_user_model()
        self.rfclient = APIClient()

        username = 'alice'
        password = 'ALICE'
        self.user = User.objects.create_superuser(
            username,
            '{}@example.com'.format(username),
            password,
        )

        self.rfclient.force_authenticate(user=self.user)

    def test_list(self):
        some_app = models.Appliance.objects.create(
            name='asdf',
            description='asdf',
            owner=self.user,
        )

        response = self.rfclient.get(self.endpoint)
        assert 200 <= response.status_code < 300, (response.status_code, response.content)
        rtext = response.content.decode(response.charset)
        data = json.loads(rtext)
        self.assertEqual(len(data), 1)

        models.Appliance.objects.create(name='zxcv', description='zxcv', owner=self.user)
        self.assertEqual(len(self.rfclient.get(self.endpoint).json()), 2)

    def test_create(self):
        response = self.rfclient.post(self.endpoint, format='json', data={
            'name': 'a_name',
            'description': 'a_type',
        })
        assert response.status_code == 201, (response.status_code, response.content)


class TestImplementationBasic(TestCase):
    pass
