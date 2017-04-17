import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APIClient

from aurora import models
from aurora import serializers


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
        assert 'id' in response.json(), response.json()
