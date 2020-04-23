import os
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Store all subject that add by all user
class SubjectContainer(models.Model):
    # keep subject that enter by all user in website in original form
    subject_name = models.TextField(max_length=200, blank=True)
    # keep subject that enter by all user in website in reduced form
    # (remove spacebar and change all letter to lowercase)
    subject_common_name = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.subject_name


# Store all request that sent between user
class RequestSender(models.Model):
    # keep sender username (who's send request)
    request_sender = models.TextField(max_length=200, blank=True)
    # keep introduction message from request sender
    request_message = models.TextField(max_length=600, blank=True)
    # keep receiver username (who's receive request)
    request_receiver = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.request_sender


# Store all matched user
class MatchContainer(models.Model):
    # keep partner username (matched user)
    partner_username = models.TextField(max_length=200, blank=True)
    # keep your username (current user)
    your_username = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.partner_username


# Main model. Store most of user data
class UserInfo(models.Model):
    # keep user's username
    name = models.TextField(max_length=200, blank=True)
    # keep user's first name
    firstname = models.TextField(max_length=200, blank=True)
    # keep user's last name
    lastname = models.TextField(max_length=200, blank=True)
    # keep user's age
    age = models.TextField(max_length=10, blank=True)
    # keep user's school
    school = models.TextField(max_length=200, blank=True)
    # keep user's school in reduced name (remove spacebar and change all letter to lowercase)
    school_common_name = models.TextField(max_length=200, blank=True)
    # keep user's gender
    gender = models.TextField(blank=True)
    # keep user's Facebook profile link
    fb_link = models.TextField(null=True)
    # keep user's expertise subject by linked with SubjectContainer class
    expertise_subject = models.ManyToManyField(SubjectContainer, related_name='Userinfos', blank=True)
    # keep user's request received by linked with RequestSender class
    request = models.ManyToManyField(RequestSender, blank=True)
    # keep user's matched list by linked with MatchContainer class
    match = models.ManyToManyField(MatchContainer, blank=True)
    # keep user's request count to be shown at notification bar
    match_request = models.IntegerField(default=0)
    # keep user's unread message count to be shown at notification bar (not used due lack of feature on chat app)
    massage_list = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    # clear notification when user click request list
    def read(self):
        # when user click on notification bar
        self.match_request = 0
        self.save()

    # increase notification count when user receive match request
    def increase_noti_count(self):
        # when user receive match request
        self.match_request = self.match_request + 1
        self.save()

    # decrease notification count when user cancel match request
    def decrease_noti_count(self):
        # when request sender cancel request
        self.match_request = self.match_request - 1
        self.save()


# Store all comment on all user
class Comment(models.Model):
    # store all data below (name to active) and linked to UserInfo class to tell that data below is belong to whom)
    post = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='comments', null=True)
    # keep reviewer's username
    name = models.CharField(max_length=80, null=True)
    # keep content that reviewer post to selected user
    comment = models.CharField(max_length=500, null=True)
    # keep score that reviewer post to selected user
    star = models.CharField(max_length=500, null=True)
    # keep date and time reviewer posted to selected user
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    # flag that tell this comment is approved or not (approve by default)
    active = models.BooleanField(default=True, null=True)

    class Meta:
        # order comment by date
        ordering = ['created_on']

    def __str__(self):
        return 'Comment to {} by {}'.format(self.post, self.name)


# Store user data, linked with User and UserInfo (use to create additional field on signup page)
class Profile(models.Model):
    # keep user's username
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # keep user's first name
    first_name = models.CharField(max_length=100, blank=True)
    # keep user's last name
    last_name = models.CharField(max_length=100, blank=True)
    # keep user's school
    college = models.CharField(max_length=100, blank=True)
    # keep user's email
    email = models.EmailField(max_length=150)
    # keep user's age
    age = models.TextField(max_length=10, blank=True)
    # keep user's gender
    gender = models.TextField()

    def __str__(self):
        return self.user.username


# Store user's pictures and set default profile picture for all user
class PictureContainer(models.Model):
    # keep user's object by linked with UserInfo class
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='image', null=True)
    # keep user's image
    images = models.ImageField(default='default.png', upload_to='media')
    # flag to tell image is profile picture or not
    is_profile_pic = models.BooleanField(default=False, null=True)

    def __str__(self):
        # If object is profile picture
        if self.is_profile_pic is True:
            return str(self.user) + " (Profile Picture)"
        return str(self.user)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    # when new user is created
    if created:
        # use Profile cass to store user's data
        Profile.objects.create(user=instance)
    # save new user's data
    instance.profile.save()


# when object from class PictureContainer is deleted, delete relate file
@receiver(models.signals.post_delete, sender=PictureContainer)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # if instance is images variable
    if instance.images:
        # get file path from images variable
        if os.path.isfile(instance.images.path):
            # delete it
            os.remove(instance.images.path)


@receiver(models.signals.pre_save, sender=PictureContainer)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = PictureContainer.objects.get(pk=instance.pk).images
    except PictureContainer.DoesNotExist:
        return False

    new_file = instance.images
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
