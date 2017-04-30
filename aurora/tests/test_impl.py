import json
import textwrap

from django.test import TestCase
# from rest_framework.request import Request
from rest_framework.serializers import ValidationError
from rest_framework.test import APIRequestFactory, APIClient

from aurora import models
from aurora import serializers

from .helpers import PreAuthMixin


MINIMAL_VALID_TEMPLATE_YAML = """\
key: value
key2: value2
outputs:
    master_ip: whatever
"""


class TestImplementationDeserialize(TestCase):
    def test_works(self):
        out = serializers.template_deserialize_yaml(MINIMAL_VALID_TEMPLATE_YAML)
        self.assertIn('key', out)

    def test_raises_expected(self):
        try:
            serializers.template_deserialize_yaml('garbage yaml\nsomething: else')
        except ValidationError as e:
            pass
        else:
            self.fail('allowed malformed data')


class TestImplementationReserialize(TestCase):
    def test_works(self):
        out = serializers.template_serialize_json({'hello': 'there'})
        self.assertIn('hello', out)

    def test_raises_expected(self):
        try:
            serializers.template_serialize_json(...) # ellipsis!
        except ValidationError as e:
            pass
        else:
            self.fail('allowed malformed data')


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

    def post_endpoint(self, data=None, **kwdata):
        if data is None:
            data = kwdata
        return self.rfclient.post(self.endpoint, format='json', data=data)


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
            'template': MINIMAL_VALID_TEMPLATE_YAML,
        })
        # print(response.content)
        self.assertEqual(response.status_code, 201, response.json())


class TestImplementationReading(TestImplementationBase):
    def setUp(self):
        super().setUp()
        self.imp = models.Implementation.objects.create(
            site=self.site, appliance=self.app, owner=self.user,
            template='hey guys')

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
        self.assertIn('template', data)
        # parsed data probably not valid because we
        # directly inserted it, bypassing the validator
        self.assertIn('template_parsed', data)


class TestImplementationCreate(TestImplementationBase):

    def post_script(self, script, dedent=True):
        if dedent:
            script = textwrap.dedent(script)

        return self.rfclient.post(self.endpoint, format='json', data={
            'site': self.site.id,
            'appliance': self.app.id,
            'template': script,
        })

    def test_create(self):
        response = self.post_script(MINIMAL_VALID_TEMPLATE_YAML)

        self.assertEqual(response.status_code, 201, response.json())
        data = response.json()
        try:
            parsed = json.loads(data['template_parsed'])
        except ValueError as e:
            self.fail(f'failed to parse JSON: {e}')

        self.assertIn('key', parsed)
        self.assertEqual(parsed['key'], 'value')
        self.assertEqual(parsed['key2'], 'value2')

    def test_ignore_set_parsed(self):
        """
        Don't allow bypassing of the script parser; the framework shouldn't
        allow direct setting of the parsed value.
        """
        response = self.rfclient.post(self.endpoint, format='json', data={
            'site': self.site.id,
            'appliance': self.app.id,
            'template': MINIMAL_VALID_TEMPLATE_YAML,
            'template_parsed': 'zxcvbn',
        })
        self.assertEqual(response.status_code, 201, response.json())
        data = response.json()
        self.assertNotIn('zxcvbn', data['template_parsed'])

    def test_handle_htv(self):
        htv_date = '2012-04-15'
        response = self.post_script(f"""\
            heat_template_version: {htv_date}
            outputs: {{'master_ip': 0}}
            something:
            - 1
            - 2
            - 3
        """)

        self.assertEqual(response.status_code, 201, response.json())
        data = response.json()
        try:
            parsed = json.loads(data['template_parsed'])
        except ValueError as e:
            self.fail(f'failed to parse JSON: {e}')

        self.assertEqual(parsed['heat_template_version'], htv_date)

    def test_kinda_handle_datelikes(self):
        htv_date = '2012-04-15'
        response = self.post_script(f"""\
            not_the_heat_template_version: {htv_date}
            outputs: {{'master_ip': 0}}
            something: [2, 3, 4]
        """)
        self.assertTrue(response.status_code < 500, response.content)
        # not defined what happens, just don't implode the server.

    def test_bad_yaml(self):
        htv_date = '2012-04-15'
        response = self.post_script("""\
            key value
            key2: value2
        """)
        self.assertEqual(400, response.status_code, response.json())
        self.assertIn('template', response.json()) # which field
        self.assertTrue(any('parse' in err for err in response.json()['template'])) # why

    def test_require_masterip(self):
        response = self.post_script("""\
            key: value
            outputs:
                not_the_master_ip: whatever
        """)

        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn('template', response.json()) # which field
        self.assertTrue(any('master_ip' in err for err in response.json()['template'])) # why


class TestImplementationSimpleApp(TestImplementationBase):
    def test_basic_fields(self):
        image_name = 'my-image'
        imp = models.Implementation(
            site=self.site,
            appliance=self.app,
            owner=self.user,
            image=image_name,
        )
        imp.save()

    def test_basic_load(self):
        image_name = 'my-image2'
        response = self.post_endpoint({
            'site': self.site.id,
            'appliance': self.app.id,
            'image': image_name,
        })
        self.assertEqual(response.status_code, 201, response.json())
        data = response.json()

        self.assertIn('template_parsed', data)
        template = json.loads(data['template_parsed'])

        self.assertIn('heat_template_version', template)
        self.assertEqual(template['resources']['appliance_instance']['properties']['image'], image_name)
