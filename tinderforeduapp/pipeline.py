# pipeline is custom function use when user logged in with facebook

from .models import UserInfo, PictureContainer
from django.contrib.auth.models import User
from social_core.pipeline.user import get_username as social_get_username
from datetime import datetime

user_email = ""


# get email from facebook
def get_email(backend, user, response, *args, **kwargs):
    # set email as global variable
    global user_email
    # if facebook user doesn't have email associate in account, use name instead
    if response.get('email') is None:
        user_email = (response.get('name')).split(" ")[0] + (response.get('name')).split(" ")[1]
    else:
        user_email = (response.get('email')).split("@")[0]


# create user UserInfo object
def user_profile_db(backend, user, response, *args, **kwargs):
    # check if UserInfo object not exist
    if not User.objects.filter(email=response.get('email')).exists():
        # receive data from facebook
        gender = ''
        birth_date = response.get('birthday')
        # calculate age from current date
        born = datetime.strptime(birth_date, '%m/%d/%Y')
        age = int((datetime.today() - born).days / 365)
        if response.get('gender') == 'male':
            gender = 'Male'
        if response.get('gender') == 'female':
            gender = 'Female'
        # if facebook user doesn't have email associate in account
        if response.get('email') is None:
            # create UserInfo object for new user
            user = UserInfo.objects.create(
                name=(response.get('name')).split(" ")[0] + (response.get('name')).split(" ")[1],
                school='',
                age=age,
                firstname=(response.get('name')).split(" ")[0],
                lastname=(response.get('name')).split(" ")[1],
                gender=gender, fb_link=response.get('link'))
        else:
            # create UserInfo object for new user
            user = UserInfo.objects.create(name=(response.get('email')).split("@")[0],
                                           school='',
                                           age=age,
                                           firstname=(response.get('name')).split(" ")[0],
                                           lastname=(response.get('name')).split(" ")[1],
                                           gender=gender, fb_link=response.get('link'))
        # assign default profile picture for new user
        PictureContainer.objects.create(user=user, images='default.png')


# set username for new user by using email account (remove email domain)
def get_username(strategy, details, backend, user=None, *args, **kwargs):
    result = social_get_username(strategy, details, backend, user=user, *args, **kwargs)
    result['username'] = user_email
    return result
