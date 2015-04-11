# from django.test import Client
# from django.test.testcases import TestCase
# from ClanClasher.forms.registration import RegistrationForm
#
#
# class testRegistration(TestCase):
#     def setUp(self):
#         pass
#
#     def test_registration_form_with_valid_data_is_valid(self):
#         data = {
#             'email': 'bob@email.com',
#             'password1': 'secret',
#             'password2': 'secrdet',
#             'chiefName': 'chiefbob',
#             'chiefLevel': 6
#         }
#
#         regForm = RegistrationForm(data)
#         regForm.full_clean()
#         self.assertTrue(regForm.is_valid())
