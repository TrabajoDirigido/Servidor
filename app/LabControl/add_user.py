__author__ = 'Camila Alvarez'
from django.contrib.auth.models import User


def add_Teacher():
    user = User.objects.create_user('profesor', '', 'profesor')
    user.save()

if __name__=="__main__":
    add_Teacher()