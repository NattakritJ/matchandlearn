# chat/views.py
from django.shortcuts import render
from .models import ChatLog
from tinderforeduapp.models import *


# chat room
def room(request, room_name):
    # store all chat message in list
    split_log = []
    # store all chat in one line (string)
    log = ""
    # list of user associate in chat room
    user = room_name.split("_")
    # send associate user to template to check that logged in user is associate in this chat or not
    user_check_one = user[0]
    user_check_two = user[1]
    # get logged in username
    username = request.user.username
    # check that this chat room have chat log or not
    if ChatLog.objects.filter(name=room_name, user_one=user_check_one, user_two=user_check_two).exists():
        # if logged in user is associate with this chat log
        if (ChatLog.objects.get(name=room_name).user_one == username) or (
                ChatLog.objects.get(name=room_name).user_two == username):
            # load chat from ChatLog object into log
            log = ChatLog.objects.get(name=room_name).chat
            # Split log and store it in list when found "`~`~`~`~`~`" in log string
            split_log = log.split("`~`~`~`~`~`")
            # assign user on ChatLog to check user privilege
            user_check_one = ChatLog.objects.get(name=room_name).user_one
            user_check_two = ChatLog.objects.get(name=room_name).user_two
    return render(request, 'chat/room.html',
                  {'name': UserInfo.objects.get(name=request.user.username), 'room_name': room_name,
                   'log': log,
                   'user_check_one': user_check_one,
                   'user_check_two': user_check_two,
                   'split_log': split_log})
