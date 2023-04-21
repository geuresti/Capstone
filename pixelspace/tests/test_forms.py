from django.test import TestCase
from pixelspace.forms import AccountForm, UserForm, SettingsForm, LABForm, confirmDeleteForm
from pixelspace import authentication as auth
import pymongo

connect_string = 'mongodb+srv://mongodb_dao:uC3wPbLm7AIhkOUL@cluster0.nem4zbs.mongodb.net/?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['pixelspace']

# created a new collection for testing
collection_name = "test_users"
collection = dbname[collection_name]

mongo_auth = auth.MongoAuthBackend()

class LoginFormTest(TestCase):
    def test_login_form_good_input(self):
        testData = {'username':'meow', 'password':'bark'}
        form = UserForm(data=testData)
        self.assertTrue(form.is_valid())

    def test_login_form_no_username(self):
        testData = {'username':'', 'password':'bark'}
        form = UserForm(data=testData)
        self.assertFalse(form.is_valid())

    def test_login_form_no_password(self):
        testData = {'username':'meow', 'password':''}
        form = UserForm(data=testData)
        self.assertFalse(form.is_valid())

"""
class CreateAccountFormTest(TestCase):
    def test_user_form_good_input(self):
        testData = {'newUser':'meow', 'newPass':'bark', 'confirmPass': 'bark'}
        form = AccountForm(data=testData)
        self.assertTrue(form.is_valid())

    def test_user_form_no_username(self):
        testData = {'newUser':'', 'newPass':'bark', 'confirmPass': 'bark'}
        form = AccountForm(data=testData)
        self.assertFalse(form.is_valid())

    def test_user_form_mismatched_passwords(self):
        testData = {'newUser':'meow', 'newPass':'bark', 'confirmPass': 'moo'}
        form = AccountForm(data=testData)

        # (passwords mismatch)
        self.assertTrue(form.is_valid())

    def test_user_form_no_passwords(self):
        testData = {'newUser':'meow', 'newPass':'', 'confirmPass': ''}
        form = AccountForm(data=testData)

        # (no passwords)
        self.assertFalse(form.is_valid())

    def test_user_form_no_input(self):
        testData = {'newUser':'', 'newPass':'', 'confirmPass': ''}
        form = AccountForm(data=testData)
        self.assertFalse(form.is_valid())
"""

class LABFormTest(TestCase):
    def test_LAB_form(self):
        testData = {'lightness': 90,'axisA': -90, 'axisB': 100}
        form = LABForm(data=testData)
        self.assertTrue(form.is_valid())

    def test_LAB_form_partial_input(self):
        testData = {'lightness': 90,'axisA': -90, 'axisB': None}
        form = LABForm(data=testData)
        self.assertFalse(form.is_valid())

    def test_LAB_form_no_input(self):
        testData = {'lightness': None,'axisA': None, 'axisB': None}
        form = LABForm(data=testData)
        self.assertFalse(form.is_valid())

class SettingsFormTest(TestCase):
    def test_setting_form_delete_true(self):
        testData = {'newPassword': 'bark','retypePassword': 'bark', 'deleteAccount': True}
        form = SettingsForm(data=testData)
        self.assertTrue(form.is_valid())

    def test_setting_form_delete_false(self):
        testData = {'newPassword': 'bark','retypePassword': 'bark', 'deleteAccount': False}
        form = SettingsForm(data=testData)
        self.assertTrue(form.is_valid())

    def test_setting_form_one_password(self):
        testData = {'newPassword': 'bark','retypePassword': '', 'deleteAccount': True}
        form = SettingsForm(data=testData)

        self.assertFalse(form.is_valid())

    def test_setting_form_change_password(self):
        mongo_auth.create_account("dummy", "password", "asd@gmail.com")

        testData = {'newPassword': 'new_password','retypePassword': 'new_password', 'deleteAccount': False}
        form = SettingsForm(data=testData)

        user_original = mongo_auth.authenticate(collection_name="test_users", username="dummy", password="password")
        if user_original:
            mongo_auth.change_password(collection_name="test_users", username="dummy", new_password="new_password")
            user_new = mongo_auth.authenticate(collection_name="test_users", username=None, password=None)

        return (self.assertTrue(form.is_valid()) and user_new)

    def test_setting_form_mismtached_passwords(self):
        testData = {'newPassword': 'meow','retypePassword': 'bark', 'deleteAccount': True}
        form = SettingsForm(data=testData)

        # (mismatched passwords)
        self.assertTrue(form.is_valid())

    def test_setting_form_no_input(self):
        testData = {'newPassword': '', 'retypePassword': '', 'deleteAccount': None}
        form = SettingsForm(data=testData)

        self.assertFalse(form.is_valid())

class confirmDeleteFormTest(TestCase):
    def test_confirm_delete_form_delete_true(self):
        testData = {'confirmDelete': True}
        form = confirmDeleteForm(data=testData)
        self.assertTrue(form.is_valid())

    def test_confirm_delete_form_delete_false(self):
        testData = {'confirmDelete': False}
        form = confirmDeleteForm(data=testData)
        self.assertTrue(form.is_valid())
