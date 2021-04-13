# -*- coding: utf-8 -*-
from django.urls import reverse

from taiga.base.utils import json

from tests import factories as f
from tests.utils import disconnect_signals, reconnect_signals

import pytest
pytestmark = pytest.mark.django_db


def setup_module(module):
    disconnect_signals()


def teardown_module(module):
    reconnect_signals()


def test_auth_create(client):
    url = reverse('auth-list')

    user = f.UserFactory.create()

    login_data = json.dumps({
        "type": "normal",
        "username": user.username,
        "password": user.username,
    })

    result = client.post(url, login_data, content_type="application/json")
    assert result.status_code == 200


def test_auth_action_register_with_short_password(client, settings):
    settings.PUBLIC_REGISTER_ENABLED = True
    url = reverse('auth-register')

    register_data = json.dumps({
        "type": "public",
        "username": "test",
        "password": "test",
        "full_name": "test",
        "email": "test@test.com",
        "accepted_terms": True,
    })

    result = client.post(url, register_data, content_type="application/json")
    assert result.status_code == 400, result.json()


def test_auth_action_register(client, settings):
    settings.PUBLIC_REGISTER_ENABLED = True
    url = reverse('auth-register')

    register_data = json.dumps({
        "type": "public",
        "username": "test",
        "password": "test123",
        "full_name": "test123",
        "email": "test@test.com",
        "accepted_terms": True,
    })

    result = client.post(url, register_data, content_type="application/json")
    assert result.status_code == 201, result.json()
