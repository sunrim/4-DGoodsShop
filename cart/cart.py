from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID)   #self.session[settings.CART_ID]
        if not cart:
            cart = self.session[settings.CART_ID] = {}


    def __str__(self):
        return self.cart


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def __iter__(self): #for문에서 하나씩 요소를 꺼낼 때 return 값
        products_ids = self.cart.keys()

        products = Product.objects.filter(id__in=products_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product     #self.cart['0917']['product']

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item

    def add(self, product, quantity=1, is_update=False):  # cart에 product 추가하자
        if product.id not in self.cart:
            self.cart[product.id] = {'quantity': 0, 'price': str(product.price)}

        if is_update:
            self.cart[product.id]['quantity'] = quantity
        else:
            self.cart[product.id]['quantity'] += quantity

        self.save()
    
    def remove(self,product):               #cart에서 product  삭제하자
        if product.id in self.cart:
            del self.cart[product.id]
            self.save()

    def save(self):                         #cart를 session에 저장하자
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def clear(self):                        #cart를 비우자
        self.session[settings.CART_ID] = {}
        self.session.modified = True

    def get_product_total(self):            #cart의 product 가격 합계를 나타내자
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

