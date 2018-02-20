# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

