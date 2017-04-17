import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APIClient

from aurora import models
from aurora import serializers


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
