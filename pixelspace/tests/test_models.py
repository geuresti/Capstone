from django.test import TestCase

from django.contrib.auth.models import User
from pixelspace.models import Account

class AccountModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        dummy = User.objects.create(
            username='John Doe',
            password='password123'
        )

        Account.objects.create(user = dummy)

    def test_user_account_are_linked(self):
        account = Account.objects.get(pk=1)
        user = account.user
        print("Testing account-user model relation")
        self.assertEqual(user.username, 'John Doe')
