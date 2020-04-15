# chat/views.py
from django.shortcuts import render
from .models import ChatLog
from django import db
from django.db import close_old_connections
from tinderforeduapp.models import *


def room(request, room_name):
    splitlog = []
    log = ""
    user = room_name.split("_")
    usercheck1 = user[0]
    usercheck2 = user[1]
    username = request.user.username
    if ChatLog.objects.filter(name=room_name, user_one=usercheck1, user_two=usercheck2).exists():
        if (ChatLog.objects.get(name=room_name).user_one == username) or (
                ChatLog.objects.get(name=room_name).user_two == username):
            log = ChatLog.objects.get(name=room_name).chat
            splitlog = log.split("`~`~`~`~`~`")
            usercheck1 = ChatLog.objects.get(name=room_name).user_one
            usercheck2 = ChatLog.objects.get(name=room_name).user_two
    close_old_connections()
    db.connection.close()
    return render(request, 'chat/room.html',
                  {'name': UserInfo.objects.get(name=request.user.username), 'room_name': room_name,
                   'log': log,
                   'usercheck1': usercheck1,
                   'usercheck2': usercheck2,
                   'splitlog': splitlog})
