from django.db import models


class API (models.Model):
    token = models.CharField(max_length=64, unique=True)
    api_token = models.CharField(max_length=64, blank=True, null=True)
    delete_time = models.DateTimeField()
    last_connection = models.CharField(max_length=20)


class Password (models.Model):
    hash = models.BinaryField()
    salt = models.BinaryField()


class Auth(models.Model):
    api = models.OneToOneField(API, on_delete=models.CASCADE)
    password = models.OneToOneField(Password, on_delete=models.CASCADE, blank=True, null=True)


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    email = models.EmailField(blank=True)
    login = models.BooleanField(default=False)
    auth = models.OneToOneField(Auth, on_delete=models.CASCADE)


class Todo(models.Model):
    todo_id = models.BigIntegerField(unique=True)
    body = models.CharField(max_length=36)
    done = models.BooleanField(default=False)
    user_id = models.BigIntegerField()


class Test (models.Model):
    i = models.IntegerField(unique=True)