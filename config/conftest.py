from http.client import responses

import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()
@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(username='testuser',password='password12345')
@pytest.fixture
def jwt_token(api_client,user):
    response = api_client.post('/api/auth/token/',{'username':'testuser','password':'password12345'},format='json')
    if response.status_code == 200:
        token = response.json()
        return token['access']
@pytest.fixture
def auth_client(api_client,jwt_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    return api_client
@pytest.fixture
def product_factory(db):
    def make_product(**kwargs):
        product = baker.make('shop.Product',**kwargs)
        return product
    return make_product
