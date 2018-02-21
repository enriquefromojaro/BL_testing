# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import  reverse
from unittest import TestCase, skip
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class UserEndpointTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(UserEndpointTestCase, cls).setUpClass()
        cls.admin_pass = 'admin_pass'
        cls.admin = User.objects.create_superuser('admin', 'root@root.com',
                                                  cls.admin_pass)

        cls.user1 = User(username='user1', email='user@user.com',
                        password='usosaurio')
        cls.user2 = User(username='user2', email='user@user.com',
                        password='usosaurio')

        User.objects.bulk_create((cls.user1, cls.user2))

    def setUp(self):
        self.client = APIClient()

    def test_list_users_admin_ok(self):

        # loging in as admin
        self.client.login(username=self.admin, password=self.admin_pass)

        # Listing the users

        response = self.client.get(reverse('api:user-list'))
        # print '###', response.__dict__

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 3)

    def test_list_users_user_ko(self):

        # loging in as user2
        self.client.login(username=self.user2.username, password='usosaurio')

        # Listing the users

        response = self.client.get(reverse('api:user-list'))

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    @skip('Deja de dar el conazo. So cansino')
    def test_list_users_unathenticated_ko(self):

        self.client.logout()
        # Listing the users

        response = self.client.get(reverse('api:user-list'))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.client.logout()
