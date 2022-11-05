from config.helpers import BaseTestCase

from user_manager.models import Profile


class TestUserModel(BaseTestCase):
    def test_user_has_no_profile_to_start(self):
        user = self.given_a_new_user()

        self.assertIsNone(user.get_profile())
        self.assertEquals(0, Profile.objects.filter(user=user).count())
