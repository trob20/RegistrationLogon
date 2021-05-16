from django.db import models
from datetime import date, datetime
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 characters"

        if postData["first_name"].isalpha() == False:
            errors["first_name"] = "First name should only contain letters"

        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"

        if postData["last_name"].isalpha() == False:
            errors["last_name"] = "Last name should only contain letters"

        if postData['birthdate'] == "":
            errors["birthdate"] = "Birthdate date cannot be blank"
        else:
            today = date.today()
            bDate = datetime.strptime(postData['birthdate'], "%Y-%m-%d").date()
            if bDate >= today:
                errors["birthdate"] = "Birthdate must be in the past"
            if bDate < today:
                age = today.year - bDate.year - ((today.month, today.day) < (bDate.month, bDate.day))
                if age < 13:
                    errors["birthdate"] = "You must be at least 13 years old to register"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address"

        try:
            user = User.objects.get(email = postData['email'])
            errors["emailNotUnique"] = "Email already exists, enter a different email"
        except User.DoesNotExist:
            email = None

        if len(postData["password"]) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if postData["password"] != postData["confirm_password"]:
            errors["password"] = "Passwords do not match"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    birthdate = models.DateField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
