import pytest
from django.conf import settings
@pytest.mark.django_db
def test_product_list_empty(api_client):
    response = api_client.get('/api/products/')
    data = response.json()
    assert response.status_code == 200
    assert 'count' in data
    assert 'results' in data
    assert data['count'] == 0
    assert data['results'] == []

@pytest.mark.django_db
def test_product_list_with_data(api_client,product_factory):
    product_1 = product_factory(name='Product a')
    product_2 = product_factory(name='Product B')
    response = api_client.get('/api/products/')
    data = response.json()
    first_product = data['results'][0]
    assert response.status_code == 200
    assert data['count'] == 2
    assert len(data['results']) == 2
    assert 'id' in first_product
    assert 'name' in first_product
    assert 'price' in first_product
def test_product_list_pagination(product_factory,api_client):
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    total_count = page_size + 2
    product_factory(_quantity=total_count)
    response = api_client.get('/api/products/')
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == total_count
    assert len(data['results']) == page_size
    assert data['next'] is not None
def test_product_search(product_factory,api_client):
    product_1 = product_factory(name='Macbook')
    product_2 = product_factory(name='Asus')
    product_3 = product_factory(name='Mouse')
    response = api_client.get('/api/products/?search=Macbook')
    data = response.json()
    assert response.status_code == 200
    assert data['count'] == 1
    assert data['results'][0]['name'] == 'Macbook'
def test_product_ordering_by_price(product_factory,api_client):
    product_1 = product_factory(name='Macbook',price=2000)
    product_2 = product_factory(name='Asus',price=1050)
    product_3 = product_factory(name='Mouse',price=100)
    response = api_client.get('/api/products/?ordering=-price')
    data = response.json()
    assert response.status_code == 200
    assert data['results'][0]['price'] > data['results'][1]['price'] and data['results'][0]['price'] > data['results'][2]['price']



