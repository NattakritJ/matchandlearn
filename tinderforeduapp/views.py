from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .forms import SignUpForm, CommentForm, AdditionalForm, EditProfileForm, ProfilePictureForm, AddPictureForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponse


@login_required
def home(request):
    return render(request, 'tinder/home.html')


def test_redirect():
    return HttpResponseRedirect("/")


# signup page
def signup(request):
    # Receive data from POST
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # Form is valid
        if form.is_valid():
            # create new user object and save it
            user = form.save(commit=False)
            # Not active this user
            user.is_active = False
            user.save()
            user.refresh_from_db()
            # Save user's value into variable
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.college = form.cleaned_data.get('college')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.gender = form.cleaned_data.get('gender')
            # Create user's UserInfo objects that store every user's data show on site
            create_user = UserInfo.objects.create(name=user.username, school=user.profile.college,
                                                  school_common_name=school_lowercase(user.profile.college),
                                                  age=user.profile.age, firstname=user.profile.first_name,
                                                  lastname=user.profile.last_name, gender=user.profile.gender)
            # Set user's profile picture to default and link PictureContainer object to user's object
            PictureContainer.objects.create(user=create_user, images='default_profile_image.png', is_profile_pic=True)
            # Save all objects
            create_user.save()
            user.save()
            # send verification email to user's email
            site_url = get_current_site(request)
            mail_subject = 'Please verify your email address.'
            message = render_to_string('tinder/send_email_template.html', {
                'user': user,
                'domain': site_url.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user), })
            send_to = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[send_to])
            email.send()
            return render(request, 'tinder/email_sent.html')
    # didn't receive POST
    else:
        form = SignUpForm()
    return render(request, 'tinder/signup.html', {'form': form})


# receive confirmation link from email
def confirmation_email_income(request, uidb64, token):
    # check user's verification by decode base64 to user's id
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    # if not found user in database
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # activate user
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'tinder/Activation_success.html')
    # link invalid (maybe activated or token invalid)
    else:
        return HttpResponse('''Activation link is invalid! <META HTTP-EQUIV="Refresh" CONTENT="5;URL=/login">''')


# show logged in user's profile page
def my_profile(request, user_id):
    # get logged in user's UserInfo object
    login_user_object = UserInfo.objects.get(name=request.user.username)
    # get only active comment
    comments = login_user_object.comments.filter(active=True)
    # get logged in user's profile picture
    login_user_profile_picture = login_user_object.image.filter(is_profile_pic=True)
    # get logged in user's additional picture
    additional_pic = login_user_object.image.filter(is_profile_pic=False)
    # when receive POST from expertise_subject_form form
    if request.POST.get('expertise_subject_form'):
        # create subject's object that contain name and common name (all lowercase) of subject enter by user
        subject = SubjectContainer.objects.create(subject_name=request.POST['expertise_subject_form'],
                                                  subject_common_name=search_lowercase(
                                                      request.POST['expertise_subject_form']))
        # add created subject into user's object
        add_subject = UserInfo.objects.get(name=request.user.username)
        add_subject.expertise_subject.add(subject)
        add_subject.save()
        return render(request, 'tinder/my_profile.html',
                      {'comments': comments, 'pic': login_user_profile_picture,
                       'additional_pic': additional_pic,
                       'name': UserInfo.objects.get(id=user_id),
                       'subject': UserInfo.objects.get(name=request.user.username).expertise_subject.all()})
    return render(request, 'tinder/my_profile.html',
                  {'comments': comments, 'pic': login_user_profile_picture,
                   'additional_pic': additional_pic, 'name': UserInfo.objects.get(id=user_id),
                   'subject': UserInfo.objects.get(name=request.user.username).expertise_subject.all(),
                   'test': UserInfo.objects.get(name=request.user.username).match.all()})


# if login successful, redirect user to home
def login_redirect(request):
    if request.POST.get('login'):
        return render(request, 'tinder/home.html', {'name': request.user.username})


# show another profile (not logged in user's profile) that clicked on search result
def searched_profile(request, user_id):
    # get searched user's object
    selected_user_object = get_object_or_404(UserInfo, id=user_id)
    # get searched user's profile picture
    selected_user_profile_picture = selected_user_object.image.filter(is_profile_pic=True)
    # get searched user's additional picture
    additional_pic = selected_user_object.image.filter(is_profile_pic=False)
    # get only active comment
    selected_user_object = UserInfo.objects.get(id=user_id)
    comments = selected_user_object.comments.filter(active=True)
    # get searched user's model
    get_user_model = get_object_or_404(UserInfo, id=user_id)
    # get searched user's object
    selected_user_object = UserInfo.objects.get(id=user_id)
    # get logged in user's model
    login_user_object = UserInfo.objects.get(name=request.user.username)
    # get logged in user and searched user username
    chat_room_username = [login_user_object.name, selected_user_object.name]
    # sort two username by alphabet
    chat_sort_username = sorted(chat_room_username)
    # create string with sorted username format (user1_user2)
    chat_url = chat_sort_username[0] + "_" + chat_sort_username[1]
    # if logged in user send match request to searched user
    if selected_user_object.request.filter(request_sender=login_user_object.name).exists():
        # send flag match_send to template to change match request button to unsent request button
        return render(request, 'tinder/profile.html',
                      {'comments': comments, 'pic': selected_user_profile_picture,
                       'name': UserInfo.objects.get(name=request.user.username),
                       'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                       'test': UserInfo.objects.get(
                           name=request.user.username).match.all(),
                       'profile': UserInfo.objects.get(id=user_id), 'match_send': 1, "chat_room_name": chat_url})
    return render(request, 'tinder/profile.html',
                  {'comments': comments, 'pic': selected_user_profile_picture, 'additional_pic': additional_pic,
                   'profile': get_user_model,
                   'subject': get_user_model.expertise_subject.all(),
                   'name': UserInfo.objects.get(name=request.user.username), "chat_room_name": chat_url})


# when new user use continue with facebook for the first time, site request additional data (school)
def facebook_additional_data_request(request):
    if request.method == "POST":
        form = AdditionalForm(request.POST)
        if form.is_valid():
            # get school data from form
            school = form.cleaned_data.get('school')
            # add data to logged in user's UserInfo object
            additional_data = UserInfo.objects.get(name=request.user.username)
            additional_data.school = school
            additional_data.school_common_name = school_lowercase(school)
            additional_data.save()
            return HttpResponseRedirect('/')
    else:
        form = AdditionalForm()
    return render(request, 'tinder/fb_data.html', {'form': form})


# homepage and search function on homepage
def homepage(request):
    # create list of search result
    search_filter = []
    # flag for check that logged in user is search or not
    form_submit_flag = 0
    # if user go to homepage without login, redirect to login page
    if UserInfo.objects.filter(name=request.user.username).count() == 0:
        return HttpResponseRedirect('/login')
    # if user register with facebook, redirect user to add school data
    if UserInfo.objects.get(name=request.user.username).school == '':
        return HttpResponseRedirect('/fb_data')
    # if user send subject_find POST form (search function)
    if request.POST.get('subject_find'):
        # send flag to template that user use search function
        form_submit_flag = 1
        # store key of search result to dict
        user_information_dict = {}
        # convert search subject input to lowercase
        search_keyword = search_lowercase(request.POST['subject_find'])
        # search have 4 types. 1.search with gender and school. 2.search with gender only. 3.search with school only
        # 4.search with subject only.
        # if user use type 1
        if request.POST['filter'] != "" and request.POST['location_school'] != " ":
            # filter UserInfo object using subject, gender and school
            search_filter = UserInfo.objects.filter(expertise_subject__subject_common_name=search_keyword,
                                                    school_common_name=school_lowercase(
                                                        request.POST['location_school']),
                                                    gender=request.POST['filter'])
            # store list of matched user in dict
            for key in search_filter:
                user_information_dict[key] = PictureContainer.objects.get(user=key, is_profile_pic=True)
        # if user use type 2
        elif request.POST['filter'] != "":
            # filter UserInfo object using subject and gender
            search_filter = UserInfo.objects.filter(expertise_subject__subject_common_name=search_keyword,
                                                    gender=request.POST['filter'])
            # store list of matched user in dict
            for key in search_filter:
                user_information_dict[key] = PictureContainer.objects.get(user=key, is_profile_pic=True)
        # if user use type 3
        elif request.POST['location_school'] != "":
            # filter UserInfo object using subject and school
            search_filter = UserInfo.objects.filter(expertise_subject__subject_common_name=search_keyword,
                                                    school_common_name=school_lowercase(
                                                        request.POST['location_school']))
            # store list of matched user in dict
            for key in search_filter:
                user_information_dict[key] = PictureContainer.objects.get(user=key, is_profile_pic=True)
        # if user use type 4
        else:
            # filter UserInfo object using subject
            search_filter = UserInfo.objects.filter(expertise_subject__subject_common_name=search_keyword)
            # store list of matched user in dict
            for key in search_filter:
                user_information_dict[key] = PictureContainer.objects.get(user=key, is_profile_pic=True)
        # return search result
        return render(request, 'tinder/home.html',
                      {'user_information_dict': user_information_dict,
                       'name': UserInfo.objects.get(name=request.user.username),
                       "search_result": search_filter, "search_size": len(search_filter), 'sendPOST': form_submit_flag,
                       "what_sub": request.POST['subject_find']})
    return render(request, 'tinder/home.html',
                  {'name': UserInfo.objects.get(name=request.user.username), "search_size": len(search_filter),
                   'sendPOST': form_submit_flag,
                   'test': UserInfo.objects.get(name=request.user.username).request.all()})


# delete logged in user's expertise subject
def delete_subject(request, user_id):
    # get logged in user's id
    login_user_id = UserInfo.objects.get(id=user_id)
    check_object_exist = get_object_or_404(UserInfo, id=user_id)
    # get list of subjects select to delete
    list_subject = request.POST.getlist("subject_list")
    if len(list_subject) == 0:
        pass
    # if user send POST with selected subject to delete
    else:
        for subject in list_subject:
            # delete subject that link to user
            select = check_object_exist.expertise_subject.get(pk=subject)
            select.delete()
    return HttpResponseRedirect(reverse('tinder:my_profile', args=(login_user_id.id,)))


# show list of match request that sent to logged in user
def match_request(request, user_id):
    # get all match request on logged in user's RequestSender model
    login_user_all_match_request = UserInfo.objects.get(name=request.user.username).request.all()
    # list to store user that sent match request to logged in user
    match_list = []
    # get logged in user object
    login_user_object = UserInfo.objects.get(name=request.user.username)
    login_user_object.read()
    login_user_object.save()
    # append all user UserInfo object found in logged in user's request_sender (on RequestSender model)
    for request_name in login_user_all_match_request:
        match_list.append(UserInfo.objects.get(name=request_name.request_sender))
    # return list of user's object that sent match request to logged in user
    return render(request, 'tinder/match_request.html', {'name': UserInfo.objects.get(name=request.user.username),
                                                         'match_request': UserInfo.objects.get(
                                                             name=request.user.username).request.all(),
                                                         'list_match': match_list})


# match request sender
def match(request, user_id):
    # get logged in user object
    login_user_object = UserInfo.objects.get(name=request.user.username)
    # get selected user object
    selected_user_object = UserInfo.objects.get(id=user_id)
    # get selected user's profile picture
    selected_user_profile_picture = selected_user_object.image.filter(is_profile_pic=True)
    # get selected user's additional picture
    selected_user_additional_pic = selected_user_object.image.filter(is_profile_pic=False)
    # get selected user (from searched result) comments
    selected_user_comments = Comment.objects.filter(post=request.user.id)
    # get selected user (from searched result) object
    selected_user_object = UserInfo.objects.get(id=user_id)
    # get logged in user and selected user username
    chat_room_username = [login_user_object.name, selected_user_object.name]
    # sort two username by alphabet
    chat_sort_username = sorted(chat_room_username)
    # create string with sorted username format (user1_user2)
    chat_url = chat_sort_username[0] + "_" + chat_sort_username[1]
    # create match flag to check if user was sent match request or not
    already_match = 0
    if request.method == "POST":
        # if user was sent match request or selected user sent match request to logged in user
        if selected_user_object.request.filter(request_sender=login_user_object.name,
                                               request_receiver=selected_user_object.name) \
                or login_user_object.request.filter(request_sender=selected_user_object.name,
                                                    request_receiver=login_user_object.name):
            # change match flag to tell template that user was sent request
            already_match = 1
            return render(request, 'tinder/profile.html',
                          {'already_match': already_match, 'comments': selected_user_comments,
                           'pic': selected_user_profile_picture,
                           'additional_pic': selected_user_additional_pic,
                           'name': UserInfo.objects.get(name=request.user.username),
                           'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                           'test': UserInfo.objects.get(name=request.user.username).match.all(), 'check': 1,
                           'profile': UserInfo.objects.get(id=user_id), 'chat_room_name': chat_url})
        # send match request to selected user
        else:
            user_name = RequestSender.objects.create(request_sender=login_user_object.name,
                                                     request_message=request.POST['text_request'],
                                                     request_receiver=selected_user_object.name)
            # add logged in user username to selected user request list
            selected_user_object.request.add(user_name)
            # increase notification count on selected user
            UserInfo.objects.get(id=user_id).increase_noti_count()
            UserInfo.objects.get(id=user_id).save()
            return render(request, 'tinder/profile.html',
                          {'already_match': already_match, 'comments': selected_user_comments,
                           'pic': selected_user_profile_picture,
                           'name': UserInfo.objects.get(name=request.user.username),
                           'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                           'test': UserInfo.objects.get(name=request.user.username).match.all(), 'check': 1,
                           'profile': UserInfo.objects.get(id=user_id), 'chat_room_name': chat_url})


# remove match between two user
def unmatch(request, user_id):
    # get logged in user object
    login_user_object = UserInfo.objects.get(name=request.user.username)
    # get selected user profile picture
    selected_user_profile_pic = PictureContainer.objects.get(user=user_id, is_profile_pic=True)
    selected_user_object = UserInfo.objects.get(id=user_id)
    # get only active comment
    selected_user_comment_object = get_object_or_404(UserInfo, name=selected_user_object.name)
    comments = selected_user_comment_object.comments.filter(active=True)
    # get selected user object
    selected_user_object = UserInfo.objects.get(id=user_id)
    # get logged in user and selected user username
    chat_room_username = [login_user_object.name, selected_user_object.name]
    # sort two username by alphabet
    chat_sort_username = sorted(chat_room_username)
    # create string with sorted username format (user1_user2)
    chat_url = chat_sort_username[0] + "_" + chat_sort_username[1]
    # if logged in user send unmatch form
    if request.POST.get('Unmatched'):
        # get linked object of logged in user and selected user
        remove_match = selected_user_object.request.get(request_sender=login_user_object.name,
                                                        request_receiver=selected_user_object.name)
        # remove linked object
        selected_user_object.request.remove(remove_match)
        # decrease notification count on selected user
        UserInfo.objects.get(id=user_id).decrease_noti_count()
        UserInfo.objects.get(id=user_id).save()
        return render(request, 'tinder/profile.html',
                      {'comments': comments, 'pic': selected_user_profile_pic,
                       'name': UserInfo.objects.get(name=request.user.username),
                       'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                       'test': UserInfo.objects.get(
                           name=request.user.username).match.all(),
                       'profile': UserInfo.objects.get(id=user_id), 'chat_room_name': chat_url})
    return render(request, 'tinder/profile.html',
                  {'comments': comments, 'pic': selected_user_profile_pic,
                   'name': UserInfo.objects.get(name=request.user.username),
                   'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                   'test': UserInfo.objects.get(name=request.user.username).match.all(),
                   'profile': UserInfo.objects.get(id=user_id), 'chat_room_name': chat_url})


# accept request sent from another user
def accept_request(request, user_id):
    # get logged in user object
    login_user_object = UserInfo.objects.get(name=request.user.username)
    # get selected user's profile picture
    selected_user_profile_picture = PictureContainer.objects.get(user=user_id, is_profile_pic=True)
    # get selected user's object
    selected_user_object = UserInfo.objects.get(id=user_id)
    # get only active comment
    selected_user_comment_object = get_object_or_404(UserInfo, name=selected_user_object.name)
    comments = selected_user_comment_object.comments.filter(active=True)
    # get logged in user and selected user username
    chat_room_username = [login_user_object.name, selected_user_object.name]
    # sort two username by alphabet
    chat_room_sort = sorted(chat_room_username)
    # create string with sorted username format (user1_user2)
    chat_url = chat_room_sort[0] + "_" + chat_room_sort[1]
    # if logged in user decided to accept match request
    if request.POST.get('accept'):
        # create linked match object to link between selected user and logged in user
        match_obj_login_user = MatchContainer.objects.create(partner_username=selected_user_object.name,
                                                             your_username=login_user_object.name)
        # add linked match object to logged in user
        login_user_object.match.add(match_obj_login_user)
        # get request linked object between selected user and logged in user
        request_obj = login_user_object.request.get(request_sender=selected_user_object.name,
                                                    request_receiver=login_user_object.name)
        # remove that linked request object
        login_user_object.request.remove(request_obj)
        # create linked match object to link between logged in user and select user
        match_obj_selected_user = MatchContainer.objects.create(partner_username=login_user_object.name,
                                                                your_username=selected_user_object.name)
        # add linked match object to selected user
        selected_user_object.match.add(match_obj_selected_user)
        return HttpResponseRedirect(reverse('tinder:match_request', args=(login_user_object.id,)))
    # if logged in user decided to decline match request
    if request.POST.get('decline'):
        # get request linked object between selected user and logged in user
        request_obj = login_user_object.request.get(request_sender=selected_user_object.name,
                                                    request_receiver=login_user_object.name)
        # remove that linked request object
        login_user_object.request.remove(request_obj)
        return HttpResponseRedirect(reverse('tinder:match_request', args=(login_user_object.id,)))
    return render(request, 'tinder/accept_request.html',
                  {'comments': comments, 'pic': selected_user_profile_picture,
                   'name': UserInfo.objects.get(name=request.user.username),
                   'chat_room_name': chat_url, 'profile': UserInfo.objects.get(id=user_id),
                   'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                   'request': login_user_object.request.get(request_sender=selected_user_object.name)})


# show all student and tutor matched list on logged in user
def students_list(request, user_id):
    # get logged in user matched list
    match_list = UserInfo.objects.get(name=request.user.username).match.all()
    # create match list dict to store matched user's object
    list_match = {}
    for match_username in match_list:
        # get UserInfo object of matched user
        key = UserInfo.objects.get(name=match_username.partner_username)
        # sort name of logged in user and matched user by alphabet
        list_sort = sorted(
            [UserInfo.objects.get(name=request.user.username).name,
             UserInfo.objects.get(name=match_username.partner_username).name])
        # add value of matched user name to matched UserInfo object key
        value = list_sort[0] + "_" + list_sort[1]
        list_match[key] = value
    return render(request, 'tinder/students_list.html', {"name": UserInfo.objects.get(name=request.user.username),
                                                         'tutor_list': UserInfo.objects.get(id=user_id).match.all(),
                                                         'list_match': list_match})


# view profile of matched user (by clicking user from Students and Tutor list page)
def matched_profile(request, user_id):
    # get selected user object
    selected_user_object = UserInfo.objects.get(id=user_id)
    # get selected user comment
    selected_user_comment_object = get_object_or_404(UserInfo, name=selected_user_object.name)
    # get only active comment
    comments = selected_user_comment_object.comments.filter(active=True)
    # get selected user profile picture
    selected_user_profile_picture = selected_user_comment_object.image.filter(is_profile_pic=True)
    # get selected user additional picture
    additional_pic = selected_user_comment_object.image.filter(is_profile_pic=False)
    # send form to template
    if request.user.is_authenticated:
        logged_in_user_commented = \
            len(selected_user_comment_object.comments.filter(active=True, name=request.user.username))
    if logged_in_user_commented != 0:
        # Don't send form to template
        comment_form = False
    else:
        comment_form = True
    # if logged in user decide to unmatch this selected user
    if request.POST.get('unmatch'):
        # get logged in user object
        login_user_object = UserInfo.objects.get(name=request.user.username)
        # get linked object between selected user and logged in user
        unmatch_obj_login_user = login_user_object.match.get(partner_username=selected_user_object.name,
                                                             your_username=login_user_object.name)
        # remove linked object from logged in user
        login_user_object.match.remove(unmatch_obj_login_user)
        # get linked object between logged in user and select user
        unmatch_obj_selected_user = selected_user_object.match.get(partner_username=login_user_object.name,
                                                                   your_username=selected_user_object.name)
        # remove linked object from selected user
        selected_user_object.match.remove(unmatch_obj_selected_user)
        return HttpResponseRedirect(reverse('tinder:students_list', args=(login_user_object.id,)))
    return render(request, 'tinder/matched_profile.html',
                  {'pic': selected_user_profile_picture, 'additional_pic': additional_pic,
                   'name': UserInfo.objects.get(name=request.user.username),
                   'username': request.user.username,
                   'profile': UserInfo.objects.get(id=user_id), 'post': selected_user_comment_object,
                   'comments': comments, 'comment_form': comment_form})


# create comment object when logged in user comment to selected user
def create_comment(request, user_id):
    # get selected user object
    selected_user_object = UserInfo.objects.get(id=user_id)
    # get selected user comment
    selected_user_comment_object = get_object_or_404(UserInfo, name=selected_user_object.name)
    # get comment that commented by logged in user
    if request.user.is_authenticated:
        logged_in_user_commented = \
            len(selected_user_comment_object.comments.filter(active=True, name=request.user.username))
    if request.method == 'POST':
        # if found comment object that created by logged in user
        if logged_in_user_commented != 0:
            # alert logged in user
            return render(request, 'tinder/error_logged_in_user_try_to_comment.html',
                          {'url': get_current_site(request).domain, 'user_id': user_id})
        comment_form = CommentForm(data=request.POST)
        # if form valid
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = selected_user_comment_object
            new_comment.name = request.user.username
            # Save the comment to the database
            new_comment.save()
            return redirect('{}#comment_section_end'.format(reverse('tinder:matched_profile', args=(user_id,))))


# delete comment that logged in user comment on another user
def delete_comment(request, user_id):
    # if receive delete comment POST
    if request.method == "POST":
        # get comment id POST
        comment_id = request.POST['comment_id']
        # find object of class Comment by id
        comment_object = Comment.objects.get(id=comment_id)
        # check if selected object is belong to logged in user
        if comment_object.name == request.user.username:
            # delete it
            comment_object.delete()
    return redirect('{}#comment_section_start'.format(reverse('tinder:matched_profile', args=(user_id,))))


# Add new image to user's gallery
def add_image(request, user_id):
    # get logged in user object
    login_user_object = UserInfo.objects.get(name=request.user.username)
    # if user send add image form
    if request.method == "POST":
        # add picture object that linked with add picture form
        add_picture_form = AddPictureForm(request.POST, request.FILES)
        # if all form is valid
        if add_picture_form.is_valid():
            new_image = add_picture_form.save(commit=False)
            # Assign this image to login user
            new_image.user = login_user_object
            # set flag profile picture to false
            new_image.is_profile_pic = False
            # save all value
            new_image.save()
            return HttpResponseRedirect(reverse('tinder:my_profile', args=(user_id,)))
    # send form to template
    else:
        add_picture_form = ProfilePictureForm()
    return render(request, 'tinder/add_image.html', {'add_picture_form': add_picture_form})


# edit logged in user profile
def edit_profile(request, user_id):
    # get logged in user object
    login_user_object = UserInfo.objects.get(name=request.user.username)
    # get logged in user profile picture
    login_user_profile_picture = PictureContainer.objects.get(user=login_user_object, is_profile_pic=True)
    # if user send edited value
    if request.method == "POST":
        # edit UserInfo object that linked with edit profile form
        form = EditProfileForm(request.POST, instance=login_user_object)
        # edit picture object that linked with picture edit form
        picture_edit_form = ProfilePictureForm(request.POST, request.FILES, instance=login_user_profile_picture)
        # if all form is valid
        if form.is_valid() and picture_edit_form.is_valid():
            # save all value
            form.save()
            picture_edit_form.save()
            return HttpResponseRedirect(reverse('tinder:my_profile', args=(user_id,)))
    # send form to template
    else:
        form = EditProfileForm(instance=login_user_object)
        picture_edit_form = ProfilePictureForm(instance=login_user_profile_picture)
    return render(request, 'tinder/edit_profile.html', {"pic": login_user_profile_picture,
                                                        'form': form, 'picture_edit_form': picture_edit_form})


# convert subject input to lowercase
def search_lowercase(keyword):
    keyword = keyword.lower()
    keyword = keyword.replace(' ', '')
    return keyword


# convert school input to lowercase
def school_lowercase(keyword):
    keyword = keyword.upper()
    keyword = keyword.replace(' ', '')
    return keyword
