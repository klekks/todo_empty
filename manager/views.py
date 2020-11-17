from django.http import JsonResponse, HttpResponse
from .models import Todo
from .utils import *
from django.db import IntegrityError


def createTodo (request, *args, **kwargs):
    user, response = LogAuth(request)
    if not user:
        return response
    if request.method == "GET":
        todoBody = request.GET.get("text", False)
        Done = request.GET.get("done", False)
        id = request.GET.get("id", False)
        if todoBody and id:
            if len(todoBody) > 36:
                return error(6)
            elif len(todoBody) < 3:
                return error(7)
            try:
                thisTodo = Todo(todo_id=id, user_id=user.id, body=todoBody, done=Done)
                thisTodo.save()
                return success(1, thisTodo.todo_id)
            except IntegrityError:
                thisTodo = Todo(todo_id=createId(), user_id=user.id, body=todoBody, done=Done)
                thisTodo.save()
                return success(2, thisTodo.todo_id)
        elif not id and not todoBody:
            return error(5)
        elif not id:
            return error(3)
        else:
            return error(4)


def makeDone(request, *args, **kwargs):
    user, response = LogAuth(request, ifNotExist=False)
    if not user:
        return response
    if request.method == "GET":
        todo_id, done = request.GET.get("id", False), request.GET.get("done", True)
        try:
            done = bool(int(done))
        except:
            done = bool(done)
        if todo_id:
            try:
                todo = Todo.objects.get(user_id=user.id, todo_id=todo_id)
            except:
                return error(8)
            todo.done = bool(done)
            todo.save()
            return success(3)
        else:
            return error(9)


def getAll(request, *args, **kwargs):
    user, response = LogAuth(request)
    if not user:
        return response
    if request.method == "GET":
        ans = {"status": "ok", "todos": []}
        for i in Todo.objects.filter(user_id=user.id).all():
            ans["todos"].append( {"id": i.todo_id, "done": i.done, "text": i.body})
        j = JsonResponse(ans)
        j.set_cookie("token", user.auth.api.token, max_age=50*365*24*60*60, domain=".todolist.space")
        return j


def deleteTodos(request, *args, **kwargs):
    user, response = LogAuth(request)
    if not user:
        return response
    if request.method == "GET":
        try:
            todo_ids = [int(i) for i in request.GET.get("ids", "").replace(",", ' ').strip().replace(" ", ",").split(",")]
        except:
            return error(8)
        for i in todo_ids:
            try:
                Todo.objects.get(user_id=user.id, todo_id=i).delete()
            except:
                pass
        return success(3)


def deleteTodo(request, *args, **kwargs):
    user, response = LogAuth(request)
    if not user:
        return response
    if request.method == "GET":
        todo_id = request.GET.get("id", -1)
        try:
            Todo.objects.get(user_id=user.id, todo_id=todo_id).delete().save()
            return success(3)
        except:
            return error(8)