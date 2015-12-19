import mock
import os

from django.core.files import File
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from photoapp.models import UserProfile, Images
from photoapp.views import HomeView, FilterView
from photoapp.forms import ImageForm
from PIL import Image


class PhotoAppTestClass(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test',
            password='tester',
        )
        self.profile = UserProfile.objects.get_or_create(user=self.user)[0]
        self.profile.photo = "https://sampleurotoprofileimage"
        self.profile.save

        # creating a mock image
        self.file_mock = mock.MagicMock(spec=File, name="FileMock")
        self.file_mock.name = "testimg.jpg"

    # mock the form save method
    @mock.patch("photoapp.forms.ImageForm.save")
    @mock.patch("photoapp.models.Images.objects.filter")
    def test_can_upload_image(self, mock_save, mock_filter):
        request = self.factory.post('/home', {
            'image': self.file_mock
        })

        # simulate a logged-in user
        request.user = self.user

        HomeView.as_view()(request)

        # assert that the form save method was called
        self.assertTrue(ImageForm.save.called)

    @mock.patch("photoapp.models.Images.objects.get")
    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("os.remove")
    def test_can_delete_image(self, mock_get, mock_path, mock_remove):
        request = self.factory.delete(
            '/home',
            'image_id=1'
        )

        # simulate a logged-in user
        request.user = self.user

        # return response
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        # assert that image model was queried
        self.assertTrue(Images.objects.get)

        # assert that delete method to remove file from file system was called
        self.assertTrue(os.remove)

    @mock.patch("photoapp.models.Images.objects.get")
    @mock.patch.object(Image, "open")
    def test_filter(self, mock_get, mock_open):
        request = self.factory.get('/filter', {
            'img_src': self.file_mock,
            'img_id': 1,
            'img_filter': 'BLUR'
        })

        # simulate a logged-in user
        request.user = self.user

        response = FilterView.as_view()(request)
        self.assertEqual(response.status_code, 200)
