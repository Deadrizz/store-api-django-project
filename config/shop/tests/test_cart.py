import pytest
from shop.models import CartItem
@pytest.mark.django_db
def test_no_auth_client_cart(product_factory,api_client):
    response = api_client.post('/api/cart/items/')
    data = response.json()
    assert response.status_code == 401
@pytest.mark.django_db
def test_auth_client_cart(auth_client,product_factory):
    initial_count = CartItem.objects.count()
    product = product_factory(name='Macbook',price=2000)
    product.stock = 10
    product.save()
    payload = {'product':product.id,'quantity':1}
    response = auth_client.post('/api/cart/items/',payload,format='json')
    print(response.json())
    assert response.status_code == 201
    assert CartItem.objects.count() == initial_count +1
@pytest.mark.django_db
def test_auth_client_cart_cart_get(auth_client,product_factory):
    initial_count = CartItem.objects.count()
    product_1 = product_factory(name='Macbook')
    product_2 = product_factory(name='Asus')
    product_1.stock = 10
    product_2.stock = 10
    product_1.save()
    product_2.save()
    payload_1 = {'product':product_1.id,'quantity':1,}
    response = auth_client.post('/api/cart/items/',payload_1,format='json')
    assert response.status_code == 201
    payload_2 = {'product':product_2.id,'quantity':1}
    response = auth_client.post('/api/cart/items/',payload_2,format='json')
    assert response.status_code == 201
    response = auth_client.get('/api/cart/')
    data = response.json()
    assert response.status_code == 200
    assert 'items' in data
    assert len(data['items']) == 2
    assert CartItem.objects.count() == initial_count + 2
    first_item = data['items'][0]
    assert 'product' in first_item
    assert 'quantity' in first_item
