from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import SignUpForm, CommentForm, AdditionalForm, Editprofileform, profilepicture
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


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.college = form.cleaned_data.get('college')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.gender = form.cleaned_data.get('gender')
            create_user = UserInfo.objects.create(name=user.username, school=user.profile.college,
                                                  school_common_name=school_lowercase(user.profile.college),
                                                  age=user.profile.age, firstname=user.profile.first_name,
                                                  lastname=user.profile.last_name, gender=user.profile.gender)
            ProfilePic.objects.create(user=create_user, images='default.png')
            create_user.save()
            user.save()
            site_url = get_current_site(request)
            mail_subject = 'Please verify your email address.'
            message = render_to_string('tinder/acc_active_email.html', {
                'user': user,
                'domain': site_url.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user), })
            send_to = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[send_to])
            email.send()
            return render(request, 'tinder/email_sent.html')

    else:
        form = SignUpForm()
    return render(request, 'tinder/signup.html', {'form': form})


def confirmation_email_income(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'tinder/Activation_success.html')
    else:
        return HttpResponse('''Activation link is invalid! <META HTTP-EQUIV="Refresh" CONTENT="5;URL=/login">''')


def my_profile(request, user_id):
    login_user_object = UserInfo.objects.get(name=request.user.username)
    comments = Comment.objects.filter(post=request.user.id)
    login_user_profile_picture = ProfilePic.objects.get(user=login_user_object)
    if request.POST.get('subject_good'):
        subject = SubjectContainer.objects.create(subject_name=request.POST['subject_good'],
                                                  subject_store=search_lowercase(request.POST['subject_good']))
        add_subject = UserInfo.objects.get(name=request.user.username)
        add_subject.expertise_subject.add(subject)
        add_subject.save()
        return render(request, 'tinder/your_subject.html',
                      {'comments': comments, 'pic': login_user_profile_picture,
                       'name': UserInfo.objects.get(id=user_id),
                       'subject': UserInfo.objects.get(name=request.user.username).expertise_subject.all()})
    return render(request, 'tinder/your_subject.html',
                  {'comments': comments, 'pic': login_user_profile_picture, 'name': UserInfo.objects.get(id=user_id),
                   'subject': UserInfo.objects.get(name=request.user.username).expertise_subject.all(),
                   'test': UserInfo.objects.get(name=request.user.username).match.all()})


def login_redirect(request):
    if request.POST.get('login'):
        return render(request, 'tinder/home.html', {'name': request.user.username})


def searched_profile(request, user_id):
    selected_user_profile_picture = ProfilePic.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    get_user_model = get_object_or_404(UserInfo, id=user_id)
    login_user_object = UserInfo.objects.get(name=request.user.username)
    opponent_user_object = UserInfo.objects.get(id=user_id)
    chat_room_username = [login_user_object.name, opponent_user_object.name]
    chat_sort_name = sorted(chat_room_username)
    chat_url = chat_sort_name[0] + "_" + chat_sort_name[1]
    if request.POST.get('comment_input'):
        comment_text = Comment.objects.create(comment=request.POST['comment_input'])
        if not Comment.objects.filter(whocomment=login_user_object, commentto=opponent_user_object):
            add_comment = Comment.objects.create(comment_value=comment_text, whocomment=login_user_object,
                                                 commentto=opponent_user_object)
            add_comment.save()
        else:
            add_comment = Comment.objects.get(whocomment=login_user_object, commentto=opponent_user_object)
            add_comment.comment_value = comment_text
            add_comment.save()
    if request.POST.get('star_input'):
        star_score = Comment.objects.create(comment=request.POST['star_input'])
        if not Comment.objects.filter(whocomment=login_user_object, commentto=opponent_user_object):
            add_comment = Comment.objects.create(comment_value=star_score, whocomment=login_user_object,
                                                 commentto=opponent_user_object)
            add_comment.save()
        else:
            add_comment = Comment.objects.get(whocomment=login_user_object, commentto=opponent_user_object)
            add_comment.comment_value = star_score
            add_comment.save()
    if opponent_user_object.request.filter(request_list=login_user_object.name).exists():
        return render(request, 'tinder/profile.html',
                      {'comments': comments, 'pic': selected_user_profile_picture,
                       'name': UserInfo.objects.get(name=request.user.username),
                       'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                       'test': UserInfo.objects.get(
                           name=request.user.username).match.all(),
                       'profile': UserInfo.objects.get(id=user_id), 'check': 1, "chat_room_name": chat_url})
    return render(request, 'tinder/profile.html',
                  {'comments': comments, 'pic': selected_user_profile_picture, 'profile': get_user_model,
                   'subject': get_user_model.expertise_subject.all(),
                   'name': UserInfo.objects.get(name=request.user.username), "chat_room_name": chat_url})


def facebook_additional_data_request(request):
    if request.method == "POST":
        form = AdditionalForm(request.POST)
        if form.is_valid():
            school = form.cleaned_data.get('school')
            additional_data = UserInfo.objects.get(name=request.user.username)
            additional_data.school = school
            additional_data.school_common_name = school_lowercase(school)
            additional_data.save()
            return HttpResponseRedirect('/')
    else:
        form = AdditionalForm()
    return render(request, 'tinder/adddata.html', {'form': form})


def homepage(request):
    search_filter = []
    send_form_counter = 0
    if UserInfo.objects.filter(name=request.user.username).count() == 0:
        return HttpResponseRedirect('/login')
    if UserInfo.objects.get(name=request.user.username).school == '':
        return HttpResponseRedirect('/adddata')
    if request.POST.get('subject_find'):
        send_form_counter = 1
        user_information_dict = {}
        search_keyword = search_lowercase(request.POST['subject_find'])
        if request.POST['filter'] != "" and request.POST['location_school'] != " ":
            search_filter = UserInfo.objects.filter(expertise_subject__subject_store=search_keyword,
                                                    school_common_name=school_lowercase(
                                                        request.POST['location_school']),
                                                    gender=request.POST['filter'])
            for key in search_filter:
                user_information_dict[key] = ProfilePic.objects.get(user=key)
        elif request.POST['filter'] != "":
            search_filter = UserInfo.objects.filter(expertise_subject__subject_store=search_keyword,
                                                    gender=request.POST['filter'])
            for key in search_filter:
                user_information_dict[key] = ProfilePic.objects.get(user=key)
        elif request.POST['location_school'] != "":
            search_filter = UserInfo.objects.filter(expertise_subject__subject_store=search_keyword,
                                                    school_common_name=school_lowercase(
                                                        request.POST['location_school']))
            for key in search_filter:
                user_information_dict[key] = ProfilePic.objects.get(user=key)
        else:
            search_filter = UserInfo.objects.filter(expertise_subject__subject_store=search_keyword)
            for key in search_filter:
                user_information_dict[key] = ProfilePic.objects.get(user=key)
        return render(request, 'tinder/home.html',
                      {'user_information_dict': user_information_dict,
                       'name': UserInfo.objects.get(name=request.user.username),
                       "search_result": search_filter, "search_size": len(search_filter), 'sendPOST': send_form_counter,
                       "what_sub": request.POST['subject_find']})
    return render(request, 'tinder/home.html',
                  {'name': UserInfo.objects.get(name=request.user.username), "search_size": len(search_filter),
                   'sendPOST': send_form_counter,
                   'test': UserInfo.objects.get(name=request.user.username).request.all()})


def delete_subject(request, user_id):
    selected_user_object = UserInfo.objects.get(id=user_id)
    check_object_exist = get_object_or_404(UserInfo, id=user_id)
    list_subject = request.POST.getlist("subject_list")
    if len(list_subject) == 0:
        pass
    else:
        for subject in list_subject:
            select = check_object_exist.expertise_subject.get(pk=subject)
            select.delete()

    return HttpResponseRedirect(reverse('tinder:your_subject', args=(selected_user_object.id,)))


def match_request(request, user_id):
    login_user_all_match_request = UserInfo.objects.get(name=request.user.username).request.all()
    match_list = []
    login_user_object = UserInfo.objects.get(name=request.user.username)
    login_user_object.read()
    login_user_object.save()
    for request_name in login_user_all_match_request:
        match_list.append(UserInfo.objects.get(name=request_name.request_list))
    return render(request, 'tinder/match_request.html', {'name': UserInfo.objects.get(name=request.user.username),
                                                         'match_request': UserInfo.objects.get(
                                                             name=request.user.username).request.all(),
                                                         'list_match': match_list})


def match(request, user_id):
    login_user_object = UserInfo.objects.get(name=request.user.username)
    selected_user_profile_picture = ProfilePic.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    selected_user_object = UserInfo.objects.get(id=user_id)
    chat_room_username = [login_user_object.name, selected_user_object.name]
    chat_sort_username = sorted(chat_room_username)
    chat_url = chat_sort_username[0] + "_" + chat_sort_username[1]
    already_match = 0
    if request.method == "POST":
        if selected_user_object.request.filter(request_list=login_user_object.name, receiver=selected_user_object.name)\
                or login_user_object.request.filter(request_list=selected_user_object.name,
                                                    receiver=login_user_object.name):
            already_match = 1
            return render(request, 'tinder/profile.html',
                          {'already_match': already_match, 'comments': comments, 'pic': selected_user_profile_picture,
                           'name': UserInfo.objects.get(name=request.user.username),
                           'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                           'test': UserInfo.objects.get(name=request.user.username).match.all(), 'check': 1,
                           'profile': UserInfo.objects.get(id=user_id), 'chat_room_name': chat_url})
        else:
            user_name = RequestSender.objects.create(request_list=login_user_object.name,
                                                     request_message=request.POST['text_request'],
                                                     receiver=selected_user_object.name)
            selected_user_object.request.add(user_name)
            UserInfo.objects.get(id=user_id).increase_noti_count()
            UserInfo.objects.get(id=user_id).save()
            return render(request, 'tinder/profile.html',
                          {'already_match': already_match, 'comments': comments, 'pic': selected_user_profile_picture,
                           'name': UserInfo.objects.get(name=request.user.username),
                           'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                           'test': UserInfo.objects.get(name=request.user.username).match.all(), 'check': 1,
                           'profile': UserInfo.objects.get(id=user_id), 'chat_room_name': chat_url})


def unmatch(request, user_id):
    login_user_object = UserInfo.objects.get(name=request.user.username)
    selected_user_profile_pic = ProfilePic.objects.get(user=user_id)
    comments = Comment.objects.filter(post=request.user.id)
    selected_user_object = UserInfo.objects.get(id=user_id)
    chat_room_username = [login_user_object.name, selected_user_object.name]
    chat_sort_username = sorted(chat_room_username)
    chat_url = chat_sort_username[0] + "_" + chat_sort_username[1]
    if request.POST.get('Unmatched'):
        login_user_object = UserInfo.objects.get(name=request.user.username)
        selected_user_object = UserInfo.objects.get(id=user_id)
        remove_match = selected_user_object.request.get(request_list=login_user_object.name,
                                                        receiver=selected_user_object.name)
        selected_user_object.request.remove(remove_match)
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


def accept_request(request, user_id):
    login_user_object = UserInfo.objects.get(name=request.user.username)
    selected_user_profile_picture = ProfilePic.objects.get(user=user_id)
    selected_user_object = UserInfo.objects.get(id=user_id)
    comments = Comment.objects.filter(post=user_id)
    chat_room_username = [login_user_object.name, selected_user_object.name]
    chat_room_sort = sorted(chat_room_username)
    chat_url = chat_room_sort[0] + "_" + chat_room_sort[1]
    if request.POST.get('accept'):
        login_user_object = UserInfo.objects.get(name=request.user.username)
        selected_user_object = UserInfo.objects.get(id=user_id)
        match_obj = MatchContainer.objects.create(user_one=selected_user_object.name, user_two=login_user_object.name)
        login_user_object.match.add(match_obj)
        request_obj = login_user_object.request.get(request_list=selected_user_object.name,
                                                    receiver=login_user_object.name)
        login_user_object.request.remove(request_obj)
        match_obj2 = MatchContainer.objects.create(user_one=login_user_object.name, user_two=selected_user_object.name)
        selected_user_object.match.add(match_obj2)
        return HttpResponseRedirect(reverse('tinder:match_request', args=(login_user_object.id,)))
    if request.POST.get('decline'):
        login_user_object = UserInfo.objects.get(name=request.user.username)
        selected_user_object = UserInfo.objects.get(id=user_id)
        request_obj = login_user_object.request.get(request_list=selected_user_object.name,
                                                    receiver=login_user_object.name)
        login_user_object.request.remove(request_obj)
        return HttpResponseRedirect(reverse('tinder:match_request', args=(login_user_object.id,)))
    return render(request, 'tinder/accept_request.html',
                  {'comments': comments, 'pic': selected_user_profile_picture,
                   'name': UserInfo.objects.get(name=request.user.username),
                   'chat_room_name': chat_url, 'profile': UserInfo.objects.get(id=user_id),
                   'subject': UserInfo.objects.get(id=user_id).expertise_subject.all(),
                   'request': login_user_object.request.get(request_list=selected_user_object.name)})


def students_list(request, user_id):
    match_list = UserInfo.objects.get(name=request.user.username).match.all()
    list_match = {}
    for match_username in match_list:
        key = UserInfo.objects.get(name=match_username.user_one)
        list_sort = sorted(
            [UserInfo.objects.get(name=request.user.username).name,
             UserInfo.objects.get(name=match_username.user_one).name])
        value = list_sort[0] + "_" + list_sort[1]
        list_match[key] = value
    return render(request, 'tinder/students_list.html', {"name": UserInfo.objects.get(name=request.user.username),
                                                         'tutor_list': UserInfo.objects.get(id=user_id).match.all(),
                                                         'list_match': list_match})


def another_profile(request, user_id):
    selected_user_object = UserInfo.objects.get(id=user_id)
    selected_user_comment_object = get_object_or_404(UserInfo, name=selected_user_object.name)
    selected_user_profile_picture = ProfilePic.objects.get(user=user_id)
    comments = selected_user_comment_object.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = selected_user_comment_object
            new_comment.name = request.user.username
            # Save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForm()
    if request.POST.get('unmatch'):
        login_user_object = UserInfo.objects.get(name=request.user.username)
        selected_user_object = UserInfo.objects.get(id=user_id)
        unmatch_obj = login_user_object.match.get(user_one=selected_user_object.name, user_two=login_user_object.name)
        login_user_object.match.remove(unmatch_obj)
        unmatch_obj2 = selected_user_object.match.get(user_one=login_user_object.name,
                                                      user_two=selected_user_object.name)
        selected_user_object.match.remove(unmatch_obj2)
        return HttpResponseRedirect(reverse('tinder:students_list', args=(login_user_object.id,)))
    return render(request, 'tinder/another_profile.html',
                  {'pic': selected_user_profile_picture, 'name': UserInfo.objects.get(name=request.user.username),
                   'profile': UserInfo.objects.get(id=user_id), 'post': selected_user_comment_object,
                   'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


def edit_profile(request, user_id):
    login_user_object = UserInfo.objects.get(name=request.user.username)
    login_user_profile_picture = ProfilePic.objects.get(user=login_user_object)
    if request.method == "POST":
        form = Editprofileform(request.POST, instance=login_user_object)
        picture_edit_form = profilepicture(request.POST, request.FILES, instance=login_user_profile_picture)
        if form.is_valid() and picture_edit_form.is_valid():
            form.save()
            picture_edit_form.save()
            return HttpResponseRedirect(reverse('tinder:your_subject', args=(user_id,)))

    else:
        form = Editprofileform(instance=login_user_object)
        picture_edit_form = profilepicture(instance=login_user_profile_picture)
    return render(request, 'tinder/edit_profile.html', {"pic": login_user_profile_picture,
                                                        'form': form, 'picture_edit_form': picture_edit_form})


def search_lowercase(keyword):
    keyword = keyword.lower()
    keyword = keyword.replace(' ', '')
    return keyword


def school_lowercase(keyword):
    keyword = keyword.upper()
    keyword = keyword.replace(' ', '')
    return keyword
