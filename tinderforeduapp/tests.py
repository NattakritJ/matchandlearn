from django.test import TestCase
from django.urls import reverse
from .models import *


class Test(TestCase):
    def setUp(self):
        """Create user and match these user"""
        # Nattakrit and Kitsanapong signup to MatchandLearn
        self.nattakrit = User.objects.create_user('nattakrit', 'tongu20068@hotmail.co.th', '1qaz2wsx3edc4rfv5tgb')
        User.objects.create_user('kitsanapong', 'kitsanspong.rodleaw@gmail.com', '1qaz2wsx3edc4rfv5tgb')
        # Create UserInfo that belong to these user
        self.nattakrit_object = UserInfo.objects.create(name='nattakrit', firstname='Nattakrit',
                                                        lastname='Jatupattaradit', age='21',
                                                        school='KMUTNB', gender="Male")
        self.kitsanapong_object = UserInfo.objects.create(name='kitsanapong', firstname='Kitsanapong',
                                                          lastname='Rodjing', age='21',
                                                          school='KMUTNB', gender="Male")
        # Assign expertise subject for these user
        self.nattakrit_subject = SubjectContainer.objects.create(subject_name='Software Development 2',
                                                                 subject_common_name='softwaredevelopment2')
        self.kitsanapong_subject = SubjectContainer.objects.create(subject_name='Math',
                                                                   subject_common_name='math')
        self.nattakrit_object.expertise_subject.add(self.nattakrit_subject)
        self.kitsanapong_object.expertise_subject.add(self.kitsanapong_subject)
        # Add profile picture to these user
        PictureContainer.objects.create(user=self.nattakrit_object)
        PictureContainer.objects.create(user=self.kitsanapong_object)
        # They match each other
        kitsanapong_matched_list = MatchContainer.objects.create(partner_username=self.nattakrit_object.name,
                                                                 your_username=self.kitsanapong_object.name)
        nattakrit_matched_list = MatchContainer.objects.create(partner_username=self.kitsanapong_object.name,
                                                               your_username=self.nattakrit_object.name)
        self.kitsanapong_object.match.add(kitsanapong_matched_list)
        self.nattakrit_object.match.add(nattakrit_matched_list)

    def test_user_can_create_comment(self):
        """test post comment to another user"""
        # Nattakrit login
        self.client.login(username='nattakrit', password='1qaz2wsx3edc4rfv5tgb')
        # he post comment to Kitsanapong profile
        create_comment = self.client.post(reverse('tinder:create_comment', args=[self.kitsanapong_object.id]),
                                                   data={'comment': 'he is a best student, fast learner.', 'star': '5'},
                                                   follow=True)
        # he saw his comment result and star
        self.assertContains(create_comment, 'Comment : he is a best student, fast learner.')
        self.assertContains(create_comment, 'Star : 5')

    def test_user_can_delete_comment(self):
        """test delete comment from another user"""
        # create comment object to use in test
        comment_object = Comment.objects.create(post=self.kitsanapong_object, name=self.nattakrit_object.name,
                                                comment='he is a best student, fast learner.', star='5')
        # Nattakrit login
        self.client.login(username='nattakrit', password='1qaz2wsx3edc4rfv5tgb')
        # he delete comment that he posted to Kitsanapong
        delete_comment = self.client.post(
            reverse('tinder:delete_comment', args=[self.kitsanapong_object.id]),
            {'comment_id': str(comment_object.id)}, follow=True)
        # he mustn't see his comment result and star anymore
        self.assertNotContains(delete_comment, 'Comment : he is a best student, fast learner.')
        self.assertNotContains(delete_comment, 'Star : 5')
        comment_detect = len(Comment.objects.filter(post=self.kitsanapong_object, name=self.nattakrit_object.name))
        self.assertEqual(comment_detect, 0)
