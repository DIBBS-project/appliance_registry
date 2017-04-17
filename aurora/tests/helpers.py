from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


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
