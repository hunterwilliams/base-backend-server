from config.helpers import BaseTestCase
from user_manager.models import Profile


class TestUserModel(BaseTestCase):
    def test_user_has_no_profile_to_start(self):
        user = self.given_a_new_user()

        self.assertIsNone(user.get_profile())
        self.assertEquals(0, Profile.objects.filter(user=user).count())

    def test_user_has_lowercase_email_always(self):
        email_case_sensitive = "SomeWonkyemail@gmail.com"
        user = self.given_a_new_user(email_case_sensitive)
        user.refresh_from_db()
        self.assertEquals(email_case_sensitive.lower(), user.email)
