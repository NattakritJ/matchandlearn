from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Store all subject that add by all user
class SubjectContainer(models.Model):
    subject_name = models.TextField(max_length=200, blank=True)
    subject_store = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.subject_name


# Store all request that sent between user
class RequestSender(models.Model):
    request_list = models.TextField(max_length=200, blank=True)
    request_message = models.TextField(max_length=600, blank=True)
    receiver = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.request_list


# Store all matched user
class MatchContainer(models.Model):
    user_one = models.TextField(max_length=200, blank=True)
    user_two = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.user_one


# Main model. Store most of user data
class UserInfo(models.Model):
    name = models.TextField(max_length=200, blank=True)
    firstname = models.TextField(max_length=200, blank=True)
    lastname = models.TextField(max_length=200, blank=True)
    age = models.TextField(max_length=10, blank=True)
    school = models.TextField(max_length=200, blank=True)
    school_common_name = models.TextField(max_length=200, blank=True)
    gender = models.TextField(blank=True)
    fb_link = models.TextField(null=True)
    expertise_subject = models.ManyToManyField(SubjectContainer, related_name='Userinfos', blank=True)
    request = models.ManyToManyField(RequestSender, blank=True)
    match = models.ManyToManyField(MatchContainer, blank=True)
    match_request = models.IntegerField(default=0)
    massage_list = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    # clear notification when user click request list
    def read(self):
        self.match_request = 0
        self.save()

    # increase notification count when user receive match request
    def increase_noti_count(self):
        self.match_request = self.match_request + 1
        self.save()

    # decrease notification count when user cancel match request
    def decrease_noti_count(self):
        self.match_request = self.match_request - 1
        self.save()


# Store all comment on all user
class Comment(models.Model):
    post = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='comments', null=True)
    name = models.CharField(max_length=80, null=True)
    comment = models.CharField(max_length=500, null=True)
    star = models.CharField(max_length=500, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True, null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment to {} by {}'.format(self.post, self.name)


# Store user data, linked with User and UserInfo
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    age = models.TextField(max_length=10, blank=True)
    gender = models.TextField()

    def __str__(self):
        return self.user.username


# Store user's profile picture and set default picture for all user
class ProfilePic(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    images = models.ImageField(default='default.png', upload_to='media')


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
