from django.test import TestCase
from django.urls import reverse
from .models import *


class Test(TestCase):
    def test_user_comment_and_delete_comment(self):
        """Create user and match these user section"""
        # Nattakrit and Kitsanapong signup to MatchandLearn
        nattakrit = User.objects.create_user('nattakrit', 'tongu20068@hotmail.co.th', '1qaz2wsx3edc4rfv5tgb')
        User.objects.create_user('kitsanapong', 'kitsanspong.rodleaw@gmail.com', '1qaz2wsx3edc4rfv5tgb')

        # Create UserInfo that belong to these user
        nattakrit_object = UserInfo.objects.create(name='nattakrit', firstname='Nattakrit',
                                                   lastname='Jatupattaradit', age='21',
                                                   school='KMUTNB', gender="Male")
        kitsanapong_object = UserInfo.objects.create(name='kitsanapong', firstname='Kitsanapong',
                                                     lastname='Rodjing', age='21',
                                                     school='KMUTNB', gender="Male")
        # Assign expertise subject for these user
        nattakrit_subject = SubjectContainer.objects.create(subject_name='Software Development 2',
                                                            subject_common_name='softwaredevelopment2')
        kitsanapong_subject = SubjectContainer.objects.create(subject_name='Math',
                                                              subject_common_name='math')
        nattakrit_object.expertise_subject.add(nattakrit_subject)
        kitsanapong_object.expertise_subject.add(kitsanapong_subject)
        # Add profile picture to these user
        PictureContainer.objects.create(user=nattakrit_object)
        PictureContainer.objects.create(user=kitsanapong_object)

        # They match each other
        kitsanapong_matched_list = MatchContainer.objects.create(partner_username=nattakrit_object.name,
                                                                 your_username=kitsanapong_object.name)
        nattakrit_matched_list = MatchContainer.objects.create(partner_username=kitsanapong_object.name,
                                                               your_username=nattakrit_object.name)
        kitsanapong_object.match.add(kitsanapong_matched_list)
        nattakrit_object.match.add(nattakrit_matched_list)

        # Nattakrit login
        self.client.force_login(nattakrit)

        """Go to profile and post comment section (function create_comment)"""
        # he go to his matched tutor and student list
        student_and_tutor_list_page = self.client.post('/' + str(nattakrit_object.id) + '/students_list/')
        # he saw Kitsanapong Rodjing
        self.assertEqual(student_and_tutor_list_page.status_code, 200)
        self.assertContains(student_and_tutor_list_page, 'Kitsanapong Rodjing')
        # Then he go to Kitsanapong profile
        kitsanapong_profile = self.client.post('/' + str(kitsanapong_object.id) + '/matched_profile/')
        # he saw his name on profile page
        self.assertEqual(kitsanapong_profile.status_code, 200)
        self.assertContains(kitsanapong_profile, kitsanapong_object.firstname)
        self.assertContains(kitsanapong_profile, kitsanapong_object.lastname)
        # he post comment to Kitsanapong profile
        post_comment_to_profile = self.client.post(reverse('tinder:create_comment', args=[kitsanapong_object.id]),
                                                   data={'comment': 'he is a best student, fast learner.', 'star': '5'},
                                                   follow=True)
        # he saw his comment result and star
        self.assertEqual(post_comment_to_profile.status_code, 200)
        self.assertContains(post_comment_to_profile, 'Comment : he is a best student, fast learner.')
        self.assertContains(post_comment_to_profile, 'Star : 5')

        """Go to delete comment section (function delete_comment)"""
        # then, he delete it
        comment_object = Comment.objects.get(post=kitsanapong_object, name=nattakrit_object.name)
        remove_comment_on_profile = self.client.post(
            reverse('tinder:delete_comment', args=[kitsanapong_object.id]),
            {'comment_id': str(comment_object.id)}, follow=True)
        # he mustn't see his comment result and star anymore
        self.assertEqual(remove_comment_on_profile.status_code, 200)
        self.assertNotContains(remove_comment_on_profile, 'Comment : he is a best student, fast learner.')
        self.assertNotContains(remove_comment_on_profile, 'Star : 5')
        comment_detect = len(Comment.objects.filter(post=kitsanapong_object, name=nattakrit_object.name))
        self.assertEqual(comment_detect, 0)
