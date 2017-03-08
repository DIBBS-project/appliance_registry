import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APIClient

from . import models
from . import serializers


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
        assert 'url' in response.json()


class PreAuthMixin(object):
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


class TestImplementationAccess(PreAuthMixin, TestCase):
    endpoint = '/implementations/'

    def setUp(self):
        super().setUp()
        self.app = models.Appliance.objects.create(
            name='asdf',
            description='asdf',
            owner=self.user,
        )
        self.site = models.Site.objects.create(
            name='zxcv',
            type='zxcv',
            api_url='zxcv',
        )
        self.rf = APIRequestFactory()

    def test_basic(self):
        response = self.rfclient.get(self.endpoint)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        # need context to get hyperlink field: http://stackoverflow.com/a/34444082/194586
        request = self.rf.post(self.endpoint)
        context = {'request': Request(request)}
        site_url = serializers.SiteSerializer(self.site, context=context).data['url']
        app_url = serializers.ApplianceSerializer(self.app, context=context).data['url']

        response = self.rfclient.post(self.endpoint, format='json', data={
            'site': site_url,
            'appliance': app_url,
            'script': 'qwer',
        })
        # print(response.content)
        self.assertEqual(response.status_code, 201)


class TestImplementationReading(TestImplementationAccess):
    def setUp(self):
        super().setUp()
        self.imp = models.Implementation.objects.create(
            site=self.site, appliance=self.app, owner=self.user,
            script='hey guys')

    def test_list(self):
        response = self.rfclient.get(self.endpoint)
        data = response.json()
        self.assertEqual(len(data), 1)

    def test_details(self):
        url = self.endpoint + str(self.imp.id) + '/'
        response = self.rfclient.get(url)
        self.assertEqual(response.status_code, 200)
        # print(len(response.content))
        # print(response.content.decode(response.charset))
        data = response.json()
        self.assertIn('script', data)
