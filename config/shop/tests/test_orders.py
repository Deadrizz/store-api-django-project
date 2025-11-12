import pytest
from shop.models import Order
from shop.models import CartItem
@pytest.mark.django_db
def test_make_order_unknow_user(api_client):
    response = api_client.post('/api/orders/checkout/',{},format='json')
    assert response.status_code == 401

@pytest.mark.django_db
def test_auth_user_empty_cart(auth_client):
    response = auth_client.post('/api/orders/checkout/',{},format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_success_order(auth_client,product_factory,user):
    initial_count = Order.objects.count()
    product_1 = product_factory(name='Macbook')
    product_2 = product_factory(name='Asus')
    product_1.stock = 10
    product_2.stock = 10
    product_1.save()
    product_2.save()
    payload_1 = {'product':product_1.id,'quantity':1,}
    payload_2 = {'product': product_2.id, 'quantity': 1, }
    auth_client.post('/api/cart/items/',payload_1,format='json')
    auth_client.post('/api/cart/items/', payload_2, format='json')
    response = auth_client.post('/api/orders/checkout/', {}, format='json')
    assert response.status_code == 201
    assert Order.objects.count() == initial_count + 1
    assert CartItem.objects.filter(cart__user=user).count() == 0


@pytest.mark.django_db
def test_order_total_price(auth_client,product_factory,user):
    initial_count = Order.objects.count()
    product_1 = product_factory(name='Macbook',price=2000)
    product_2 = product_factory(name='Asus',price=1000)
    product_1.stock = 10
    product_2.stock = 10
    product_1.save()
    product_2.save()
    expected_total = 1*2000 + 2*1000
    payload_1 = {'product': product_1.id, 'quantity': 1, }
    payload_2 = {'product': product_2.id, 'quantity': 2, }
    auth_client.post('/api/cart/items/', payload_1, format='json')
    auth_client.post('/api/cart/items/', payload_2, format='json')
    response = auth_client.post('/api/orders/checkout/',{},format='json')
    assert response.status_code == 201
    assert Order.objects.count() == initial_count + 1
    order = Order.objects.latest('id')
    assert float(order.total_price) == float(expected_total)
    assert CartItem.objects.filter(cart__user=user).count() == 0