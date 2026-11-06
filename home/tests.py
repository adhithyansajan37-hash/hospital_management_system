from django.conf import settings
from django.contrib import admin
from django.test import TestCase
from django.core.files.base import ContentFile
from django.test import override_settings
from django.urls import include, path, reverse
from django.views.static import serve

from django.contrib.auth.models import User

from .models import UserProfile, booking, contact, dept, doctors


urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', include('home.urls')),
]


@override_settings(ROOT_URLCONF='home.tests')
class DoctorImageTests(TestCase):
    def test_uploaded_doctor_image_is_rendered_and_served(self):
        user = User.objects.create_user(username='patient', password='test-password')
        self.client.force_login(user)
        department = dept.objects.create(
            dept_name='Cardiology',
            dept_description='Heart care',
        )
        doctor = doctors(
            doctor_name='Test Doctor',
            doctor_specialization='Cardiology',
            dept_name=department,
        )
        image_data = bytes.fromhex(
            '89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489'
            '0000000b49444154789c636000020000050001a5f645400000000049454e44ae426082'
        )
        doctor.doctor_image.save(
            'doctor-test.png',
            ContentFile(image_data),
            save=True,
        )
        self.addCleanup(doctor.doctor_image.delete, save=False)

        response = self.client.get(reverse('doctors'))

        self.assertContains(response, doctor.doctor_image.url)
        image_response = self.client.get(doctor.doctor_image.url)

        self.assertEqual(image_response.status_code, 200)
        self.assertEqual(image_response['Content-Type'], 'image/png')
        image_response.close()

    def test_existing_doctor_images_are_served(self):
        for image_name in ('download.jpg', 'download_1.jpg'):
            response = self.client.get(f'/media/doctor_images/{image_name}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'image/jpeg')
            response.close()


@override_settings(ROOT_URLCONF='home.tests')
class BookingViewTests(TestCase):
    def test_booking_view_renders_get_request(self):
        user = User.objects.create_user(username='patient', password='test-password')
        self.client.force_login(user)

        response = self.client.get(reverse('booking'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking.html')

    def test_booking_page_renders_on_get(self):
        user = User.objects.create_user(username='patient', password='test-password')
        self.client.force_login(user)
        response = self.client.get(reverse('booking'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient Name')
        self.assertContains(response, 'class="nav-booking"')
        self.assertContains(response, '/static/home/css/style.css')
        self.assertContains(response, 'form-card--booking')
        self.assertContains(response, 'class="form-submit">Confirm booking</button>')
        self.assertContains(response, 'type="date" name="booked_on"')
        self.assertContains(response, 'name="doctor_name" class="form-control"')

    def test_invalid_booking_post_renders_form_errors(self):
        user = User.objects.create_user(username='patient', password='test-password')
        self.client.force_login(user)
        response = self.client.post(reverse('booking'), {})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')


@override_settings(ROOT_URLCONF='home.tests')
class ContactViewTests(TestCase):
    def test_contact_page_renders_contact_fields_not_booking_fields(self):
        user = User.objects.create_user(username='patient', password='test-password')
        self.client.force_login(user)
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'adhiii.ig')
        self.assertContains(response, '+91 7012 345 678')
        self.assertContains(response, 'class="contacting-form"')
        self.assertContains(response, '/static/home/css/style.css')
        self.assertContains(response, 'class="form-submit"')
        self.assertContains(response, 'form-card--contact')
        self.assertContains(response, 'class="form-submit">Send message</button>')
        self.assertContains(response, 'name="subject"')
        self.assertContains(response, 'name="address"')
        self.assertContains(response, 'name="message"')
        self.assertLess(
            response.content.index(b'name="address"'),
            response.content.index(b'name="subject"'),
        )
        self.assertLess(
            response.content.index(b'name="address"'),
            response.content.index(b'name="message"'),
        )
        self.assertNotContains(response, 'name="doctor_name"')
        self.assertNotContains(response, 'name="booked_on"')

    def test_contact_submission_is_saved_as_a_message_not_a_booking(self):
        user = User.objects.create_user(username='patient', password='test-password')
        self.client.force_login(user)
        response = self.client.post(
            reverse('contact'),
            {
                'name': 'Alex Patient',
                'email': 'alex@example.com',
                'phone': '5551234567',
                'subject': 'Question about services',
                'address': '123 Example Street',
                'message': 'Could you share more information?',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(contact.objects.count(), 1)
        self.assertEqual(booking.objects.count(), 0)
        self.assertEqual(contact.objects.get().address, '123 Example Street')
        self.assertContains(response, 'Your message has been sent.')


@override_settings(ROOT_URLCONF='home.tests')
class ProfileViewTests(TestCase):
    def test_authenticated_patient_profile_renders_profile_form(self):
        user = User.objects.create_user(
            username='patient',
            password='test-password',
            first_name='Alex',
            email='alex@example.com',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_profile.html')
        self.assertContains(response, 'My profile')
        self.assertContains(response, 'name="phone"')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_patient_profile_updates_user_and_profile_details(self):
        user = User.objects.create_user(username='patient', password='test-password')
        self.client.force_login(user)

        response = self.client.post(
            reverse('profile'),
            {
                'first_name': 'Alex',
                'last_name': 'Patient',
                'email': 'alex@example.com',
                'phone': '5551234567',
                'address': '123 Example Street',
                'date_of_birth': '1990-01-02',
                'gender': 'Other',
                'blood_group': 'O+',
                'emergency_contact': '5557654321',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(user.get_full_name(), 'Alex Patient')
        self.assertEqual(user.email, 'alex@example.com')
        self.assertEqual(profile.phone, '5551234567')
        self.assertEqual(profile.address, '123 Example Street')

    def test_staff_profile_renders_admin_profile(self):
        user = User.objects.create_user(
            username='administrator',
            password='test-password',
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_profile.html')
        self.assertContains(response, 'Administrator profile')
        self.assertContains(response, 'Administrator account')
        self.assertContains(response, 'Administration at a glance')
        self.assertNotContains(response, 'name="blood_group"')
        self.assertNotContains(response, 'name="emergency_contact"')

        home_response = self.client.get(reverse('index'))
        self.assertContains(home_response, 'Admin Dashboard')
        self.assertContains(home_response, 'class="header-account"')
        self.assertContains(home_response, 'class="account-icon"')

    def test_patient_does_not_see_admin_dashboard_link(self):
        user = User.objects.create_user(username='patient', password='test-password')
        self.client.force_login(user)

        response = self.client.get(reverse('index'))

        self.assertNotContains(response, 'Admin Dashboard')
