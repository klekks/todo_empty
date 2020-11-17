from .models import API, User, Auth
from random import randint
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import IntegrityError


def CreateUser():
    api = API(token=createToken(),
              delete_time=datetime.datetime.today() + datetime.timedelta(50 * 365),
              last_connection=datetime.datetime.now() - datetime.timedelta(1))
    api.save()
    auth = Auth(api=api)
    auth.save()
    user = User(id=createId(), auth=auth)
    user.save()
    print("CREATE USER")
    return user


def LogAuth(request, ifNotExist=True):
    user = getUser(request, ifNotExist)
    if user:
            return user, None
    else:
        return False, error(1)


def createToken(length=64):
    s = ""
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(length):
        s += alphabet[randint(0, len(alphabet) - 1)]
    return s


def createId():
    return randint(1000000, 99999999999)


def getUser(request, ifNotExist):
    token = request.COOKIES.get("token", False) or request.headers.get("token", False)
    if token:
        try:
            return API.objects.get(token=token).auth.user
        except ObjectDoesNotExist:
            return False
    elif ifNotExist:
        return CreateUser()
    else:
        return False


def error(code):
    j = JsonResponse(ERRORS[code])
    j["Access-Control-Allow-Origin"] = "*"

    return j


def success(code, args=''):
    j = JsonResponse(SUCCESS[code](args))
    j["Access-Control-Allow-Origin"] = "*"
    return j


def successTodo(id):
    return {"status": "ok", "id": id}


def changeId(id):
    return {"status": "error", "code": 100, "message": "Already exist.", "new_id": id}


def Allsuccess(*args):
    return {"status": "ok"}


ERRORS = [
    '',
    {"status": "error",  # 1
     "code": 200,
     "message": "Authorization failed. Invalid token.",
     },
    {"status": "error",  # 2
     "code": 201,
     "message": "Too many requests."
     },
    {"status": "error",  # 3
     "code": 202,
     "message": "Id was not passed."
     },
    {"status": "error",  # 4
     "code": 203,
     "message": "Text was not passed."
     },
    {"status": "error",  # 5
     "code": 204,
     "message": "Id and text was not passed."
     },
    {"status": "error",  # 6
     "code": 205,
     "message": "Text is too long."
     },
    {"status": "error",  # 7
     "code": 206,
     "message": "Text is too short."
     },
    {"status": "error",  # 8
     "code": 207,
     "message": "Does not exist."
     },
    {"status": "error",  # 9
     "code": 208,
     "message": "Todo_id was not passed."
     },
]
SUCCESS = {1: successTodo, 2: changeId, 3: Allsuccess}
