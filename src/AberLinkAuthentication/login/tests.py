from django.test.testcases import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from django.contrib import admin

from login import views
from login.models import OpenIDCUser, DiscordUser
# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_url_openidc(self):
        url = reverse('Home')
        self.assertEquals(resolve(url).func, views.openidc_response)

    def test_url_discord_oauth(self):
        url = reverse('Discord-login')
        self.assertEquals(resolve(url).func, views.discord_oauth2)

    def test_url_discord_redirect(self):
        url = reverse('Discord-response')
        self.assertEquals(resolve(url).func, views.discord_oauth2_redirect)

    def test_url_logged_in(self):
        url = reverse('logged-in-accounts')
        self.assertEquals(resolve(url).func, views.get_authenticated_user)

    def test_url_deleted_user(self):
        url = reverse('User-data-deleted')
        self.assertEquals(resolve(url).func, views.deleted_user)

    def test_url_privacy_policy(self):
        url = reverse('privacy-policy')
        self.assertEquals(resolve(url).func, views.privacy_policy_view)

    def test_url_major_project(self):
        url = reverse('major-project')
        self.assertEquals(resolve(url).func, views.about_major_project_view)

    def test_url_admin(self):
        url = reverse('Admin')
        self.assertEquals(resolve(url).func, admin.site.urls)

class TestModels(TestCase):

    def test_model_openidc_user(self):
        self.openidc_user1 = OpenIDCUser.objects.create(
            username="abc123",
            name="Bob Ross",
            email="abc123@aber.ac.uk",
            usertype="undergrad"
        )
        self.assertEquals(self.openidc_user1.username, "abc123")
        self.assertEquals(self.openidc_user1.name, "Bob Ross")
        self.assertEquals(self.openidc_user1.email, "abc123@aber.ac.uk")
        self.assertEquals(self.openidc_user1.usertype, "undergrad")

    def test_model_discord_user(self):
        self.discord_user1 = DiscordUser.objects.create(
            id=12213123123,
            openidc=self.discord_user1
        )
        self.assertEquals(self.discord_user1.id, 12213123123)
        self.assertEquals(self.discord_user1.openidc, self.openidc_user1)

    def test_model_discord_user_add_two(self):
        self.openidc_user1 = OpenIDCUser.objects.create(
            username="abc123",
            name="Bob Ross",
            email="abc123@aber.ac.uk",
            usertype="undergrad"
        )
        self.discord_user1 = DiscordUser.objects.create(
            id=12213123123,
            openidc=self.discord_user1
        )
        self.discord_user2 = DiscordUser.objects.create(
            id=78342545464,
            openidc=self.discord_user1
        )
        self.assertEquals(self.discord_user1.id, 12213123123)
        self.assertEquals(self.discord_user1.openidc, self.openidc_user1)
        self.assertEquals(self.discord_user2.id, 78342545464)
        self.assertEquals(self.discord_user1.openidc, self.openidc_user1)

    def test_model_openidc_user_staff(self):
        self.openidc_user2 = OpenIDCUser.objects.create(
            username="abc123",
            name="Bob Ross",
            email="abc123@aber.ac.uk",
            usertype="staff"
        )
        self.assertEquals(self.openidc_user2.username, "abc123")
        self.assertEquals(self.openidc_user2.name, "Bob Ross")
        self.assertEquals(self.openidc_user2.email, "abc123@aber.ac.uk")
        self.assertEquals(self.openidc_user2.usertype, "staff")
        self.assertEquals(self.openidc_user2.is_admin, True)
