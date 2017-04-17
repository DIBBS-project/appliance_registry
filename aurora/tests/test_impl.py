import json

from django.test import TestCase
# from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APIClient

from aurora import models
from aurora import serializers

from .helpers import PreAuthMixin


class TestImplementationBase(PreAuthMixin, TestCase):
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


class TestImplementationAccess(TestImplementationBase):

    def test_basic(self):
        response = self.rfclient.get(self.endpoint)
        self.assertEqual(response.status_code, 200, response.json())

    def test_create(self):
        # need context to get hyperlink field: http://stackoverflow.com/a/34444082/194586
        # request = self.rf.post(self.endpoint)
        # context = {'request': Request(request)}
        # site_url = serializers.SiteSerializer(self.site, context=context).data['url']
        # app_url = serializers.ApplianceSerializer(self.app, context=context).data['url']

        response = self.rfclient.post(self.endpoint, format='json', data={
            'site': self.site.id,
            'appliance': self.app.id,
            'script': 'test: hello',
        })
        # print(response.content)
        self.assertEqual(response.status_code, 201, response.json())


class TestImplementationReading(TestImplementationBase):
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
        self.assertEqual(response.status_code, 200, response.json())
        # print(len(response.content))
        # print(response.content.decode(response.charset))
        data = response.json()
        self.assertIn('script', data)
        # parsed data probably not valid because we
        # directly inserted it, bypassing the validator
        self.assertIn('script_parsed', data)


class TestImplementationCreate(TestImplementationBase):
    # def setUp(self):
    #     super().setUp()
    #     self.imp = models.Implementation.objects.create(
    #         site=self.site, appliance=self.app, owner=self.user,
    #         script='hey guys')

    def test_create(self):
        script = """\
key: value
key2: value2
        """

        response = self.rfclient.post(self.endpoint, format='json', data={
            'site': self.site.id,
            'appliance': self.app.id,
            'script': script,
        })
        self.assertEqual(response.status_code, 201, response.json())
        data = response.json()
        try:
            parsed = json.loads(data['script_parsed'])
        except ValueError as e:
            self.fail(f'failed to parse JSON: {e}')

        self.assertIn('key', parsed)
        self.assertEqual(parsed['key'], 'value')
        self.assertEqual(parsed['key2'], 'value2')

    def test_handle_htv(self):
        htv_date = '2012-04-15'
        script = f"""\
heat_template_version: {htv_date}
something:
- 1
- 2
- 3
        """

        response = self.rfclient.post(self.endpoint, format='json', data={
            'site': self.site.id,
            'appliance': self.app.id,
            'script': script,
        })
        self.assertEqual(response.status_code, 201, response.json())
        data = response.json()
        try:
            parsed = json.loads(data['script_parsed'])
        except ValueError as e:
            self.fail(f'failed to parse JSON: {e}')

        self.assertEqual(parsed['heat_template_version'], htv_date)

    def test_handle_datelikes(self):
        htv_date = '2012-04-15'
        script = f"""\
not_the_heat_template_version: {htv_date}
something: [2, 3, 4]
        """

        response = self.rfclient.post(self.endpoint, format='json', data={
            'site': self.site.id,
            'appliance': self.app.id,
            'script': script,
        })
        self.assertTrue(response.status_code < 500, response.content)
        # not defined what happens, just don't implode the server.

    def test_bad_yaml(self):
        script = """\
key value
key2: value2
        """

        response = self.rfclient.post(self.endpoint, format='json', data={
            'site': self.site.id,
            'appliance': self.app.id,
            'script': script,
        })
        self.assertTrue(400 <= response.status_code < 500, response.json())
        self.assertIn('script', response.json()) # which field
        self.assertTrue(any('parse' in err for err in response.json()['script'])) # why
