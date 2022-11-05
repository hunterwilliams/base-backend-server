# """
# User manager's views tests
# """
from rest_framework.reverse import reverse
from user_manager.models import User
from config.helpers import BaseTestCase


class TestAuthViews(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_email = "test@divertise.asia"
        self.user_password = "ABC!@#22AAdd"

    def test_login_success_returns_token(self):
        self.given_a_new_user(email=self.user_email, password=self.user_password)
        self.given_url(reverse("v1:auth-login"))

        self.when_user_posts_and_gets_json(
            {"email": self.user_email, "password": self.user_password}
        )

        self.assertResponseSuccess()
        self.assertIn("token", self.response_json)
        print(">> test_login_success_returns_token: OK <<")

    def test_login_updates_last_login(self):
        user = self.given_a_new_user(email=self.user_email, password=self.user_password)
        self.assertIsNone(user.last_login)
        self.given_url(reverse("v1:auth-login"))

        self.when_user_posts_and_gets_json(
            {"email": self.user_email, "password": self.user_password}
        )

        self.assertResponseSuccess()
        user.refresh_from_db()
        first_login = user.last_login
        self.assertIsNotNone(first_login)

        self.when_user_posts_and_gets_json(
            {"email": self.user_email, "password": self.user_password}
        )

        self.assertResponseSuccess()
        user.refresh_from_db()
        self.assertGreater(user.last_login, first_login)
        print(">> test_login_updates_last_login: OK <<")

    def test_login_with_inactive_user_fails(self):
        user = self.given_a_new_user(email=self.user_email, password=self.user_password)
        user.is_active = False
        user.save()
        self.given_url(reverse("v1:auth-login"))

        self.when_user_posts_and_gets_json(
            {"email": self.user_email, "password": self.user_password}
        )

        self.assertResponseBadRequest()
        self.assertNotIn("token", self.response_json)
        self.assertIn("non_field_errors", self.response_json)
        self.assertEqual(
            self.response_json["non_field_errors"], ["This email is inactive."]
        )
        print(">> test_login_with_inactive_user_fails: OK <<")

    def test_login_requires_email_and_password(self):
        self.given_url(reverse("v1:auth-login"))

        self.when_user_posts_and_gets_json({})

        self.assertResponseBadRequest()
        self.assertIn("email", self.response_json)
        self.assertIn("password", self.response_json)
        self.assertEqual(self.response_json["email"], ["This field is required."])
        self.assertEqual(self.response_json["password"], ["This field is required."])
        print(">> test_login_requires_email_and_password: OK <<")

    def test_login_with_nonexistant_email_fails(self):
        modified_email = self.user_email + ".dne"
        self.assertEquals(0, User.objects.filter(email=modified_email).count())

        self.given_url(reverse("v1:auth-login"))

        self.when_user_posts_and_gets_json(
            {"email": self.user_email, "password": self.user_password}
        )

        self.assertResponseBadRequest()

        self.assertIn("non_field_errors", self.response_json)
        self.assertEqual(
            self.response_json["non_field_errors"], ["This email does not exist."]
        )
        print(">> test_login_with_nonexistant_email_fails: OK <<")

    def test_login_wrong_pass_fails(self):
        self.given_a_new_user(email=self.user_email, password=self.user_password)
        self.given_url(reverse("v1:auth-login"))

        self.when_user_posts_and_gets_json(
            {"email": self.user_email, "password": self.user_password + "."}
        )

        self.assertResponseNotAuthorized()
        self.assertNotIn("token", self.response_json)
        self.assertIn("non_field_errors", self.response_json)
        self.assertEqual(
            self.response_json["non_field_errors"], ["Password is incorrect."]
        )
        print(">> test_login_wrong_pass_fails: OK <<")

    def test_change_password_success(self):
        user = self.given_a_new_user(email=self.user_email, password=self.user_password)
        self.given_logged_in_as_user(user)
        self.given_url(reverse("v1:auth-change-password"))

        self.when_user_posts(
            {
                "confirm_password": self.user_email,
                "new_password": self.user_email,
                "old_password": self.user_password,
            }
        )
        self.assertResponseSuccess()
        print(">> test_change_password_success: OK <<")

    def test_change_password_is_bad_request_when_wrong_password(self):
        user = self.given_a_new_user(email=self.user_email, password=self.user_password)
        self.given_logged_in_as_user(user)
        self.given_url(reverse("v1:auth-change-password"))

        self.when_user_posts_and_gets_json(
            {
                "confirm_password": self.user_email,
                "new_password": self.user_email,
                "old_password": self.user_password + "a",
            }
        )
        self.assertResponseBadRequest()
        self.assertIn("non_field_errors", self.response_json)
        self.assertEquals(
            ["Your old password is incorrect."],
            self.response_json["non_field_errors"],
        )
        print(">> test_change_password_is_bad_request_when_wrong_password: OK <<")

    def test_change_password_is_bad_request_when_passwords_do_not_match(self):
        user = self.given_a_new_user(email=self.user_email, password=self.user_password)
        self.given_logged_in_as_user(user)
        self.given_url(reverse("v1:auth-change-password"))

        self.when_user_posts_and_gets_json(
            {
                "confirm_password": self.user_email,
                "new_password": self.user_email + "a",
                "old_password": self.user_password,
            }
        )
        self.assertResponseBadRequest()
        self.assertIn("non_field_errors", self.response_json)
        self.assertEquals(
            ["New password and confirm password do not match."],
            self.response_json["non_field_errors"],
        )
        print(
            ">> test_change_password_is_bad_request_when_passwords_do_not_match: OK <<"
        )

    def test_change_password_fails_when_password_fails_validator(self):
        user = self.given_a_new_user(email=self.user_email, password=self.user_password)
        self.given_logged_in_as_user(user)
        self.given_url(reverse("v1:auth-change-password"))

        self.when_user_posts_and_gets_json(
            {
                "confirm_password": "a",
                "new_password": "a",
                "old_password": self.user_password,
            }
        )
        self.assertResponseBadRequest()
        self.assertIn("non_field_errors", self.response_json)
        self.assertEquals(
            [
                "This password is too short. It must contain at least 8 characters.",
                "This password is too common.",
            ],
            self.response_json["non_field_errors"],
        )
        print(">> test_change_password_fails_when_password_fails_validator: OK <<")
