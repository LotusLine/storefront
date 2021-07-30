from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F , Value, Func, ExpressionWrapper
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models.functions import Concat
from django.db.models.expressions import Value
from django.db.models.fields import DecimalField
from django.db import transaction
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist, TooManyFieldsSent
from store.models import *
from tags.models import *


def say_hello(request):
    
    
    #product_exists = Product.objects.filter(id=0)

    #GT stands for greater than and is basically like unit_price > 20
    #query_set = Product.objects.filter(unit_price__gt=20)
    #query_set.filter().filter().order_by()

    #query_set = Product.objects.filter(unit_price__range=(20,100))
    #query_set = Product.objects.filter(collection__id__range=(1,2,3))
    #query_set = Product.objects.filter(title__icontains='coffee')
    #query_set = Product.objects.filter(description__isnull=True)
    #query_set = Customer.objects.filter(email__endswith='.com')

    #query_set = Collection.objects.filter(featured_product__isnull=True)

    #query_set = Product.objects.filter(inventory__lt=10)
    #query_set = Order.objects.filter(customer_id=1)

    #Order items for products in collection 3
    #query_set = OrderItem.objects.filter(product__collection__id=3)


    #Products: Inventory <10 AND  Price >20
    #query_set = Product.objects.filter(inventory__gt=10000).filter(unit_price__lt=2)


    #Products: Inventory <10 AND NOT Price >20
    #query_set = Product.objects.filter(Q(inventory__gt=10)| ~Q(unit_price__lt=20))


    #Products: Inventory <10 OR Price >20
    #query_set = Product.objects.filter(Q(inventory__gt=10000)| Q(unit_price__lt=2))

    #Products: Where inventory = price
    #query_set = Product.objects.filter(inventory=F('unit_price'))


    #query_set = Product.objects.order_by('unit_price','-title')
    #query_set = Product.objects.filter(collection_id=3).order_by('unit_price')

    #As soon as its an individual element, the variable should be renamed not to queryset but normal variable name
    #product_dummy = Product.objects.filter(collection_id=3).order_by('unit_price')[0]
    
    #Returns the Price in ASC order. For DESC order, use objects.latest
    #second_product_dummy = Product.objects.earliest('unit_price')

    #GETS all products within a range
    #query_set = Product.objects.all()[:50]

    #GETS selected fields and returns them as a dictionary
    #query_set = Product.objects.values_list('id','title')

    #GETS selected fields and returns them as a tuples
    #query_set = Product.objects.values('id','title')


    #Select products that have been ordered and sort them by the title, make sure theres no duplicates by using distinct
    #query_set = OrderItem.objects.values('product_id').distinct()
    #query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id')).distinct().order_by('title')

    #**Important! To optimize speed. select_related is like a JOIN and is suitable when other end of the relationship has 1 instance only
    #query_set = Product.objects.select_related('collection').all()

    #Prefetch related : Used when the when other end of the relationship has many objects
    #query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()

    #GET the latest 5 orders with their customer and items
    #query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]


    #result = Product.objects.aggregate(
            #countmama=Count('id'),minnimumpricey=Min('unit_price'))

    
    #How many orders has customer 1 placed?
    #result = Order.objects.filter(customer__id=1).aggregate(customer1bought=Count('id'))

    
    
    #What is the min, max and average price of the products in collection 3?
    #result = Product.objects\
        #.filter(collection__id=3)\
        #.aggregate(
        #minprice=Min('unit_price'),
        #maxprice=Max('unit_price'), 
        #avgprice=Avg('unit_price'),
        #)


    #Annotation is when we want to add additional attributes to objects while querying them.
    #Here every new customer will be having the value true in the column "iam_new"
    #query_set = Customer.objects.annotate(iam_new=Value(True))

    #New columnn "NEW ID"  which is populated with the same value as the customer id + 1
    #query_set = Customer.objects.annotate(new_id=F('id')+ 1)


    #Call a database function
    #query_set = Customer.objects.annotate(
        #CONCAT function
        #full_name=Concat('first_name', Value('  '), 'last_name'))

    #Count how many orders any specific customer has placed
    #query_set=Customer.objects.annotate(
        #orders_count=Count('order'))

    #Using ExpressionWrappers here because the unit price field is a floatfield and not a decimalfield
    #so by wrapping the expression into a decimalfield we can operate as we like
    #discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    #query_set = Product.objects.annotate(discounted_price=discounted_price)


    #Customers with their last order ID
    #query_set = Customer.objects.annotate(last_orderid=Max('order__id'))
  

    #Collection and count of their products
    #query_set = Collection.objects.annotate(product_count=Count('product'))


    #Customers with more than 5 orders
    #query_set = Customer.objects.annotate(orders_count=Count('order')).filter(orders_count__gt=5)


    #Customers and the total amount they spent
    #query_set = Customer.objects.annotate(
        #total_amount_spent=Sum(
        #F('order__orderitem__unit_price') *
        #F('order__orderitem__quantity')))


    #Top 5 best selling products and their total sales
    #query_set = Product.objects.annotate(
        #bestsellers_totalamount=Sum(
            #F('orderitem__unit_price') *
            #F('orderitem__quantity'))) \
            #.order_by('-bestsellers_totalamount')[:5]


    #Utilizing the Custom Manager we created in the tagged item manager class
    #query_set = TaggedItem.objects.get_tags_for(Product, 1)


    #Insert a record in the database
    #collection = Collection()
    #collection.title = 'Video Games'
    #collection.featured_product = Product(pk=1)
    #collection.save()

    #Update a record in the database
    #collection = Collection.objects.get(pk=11)
    #collection.title = 'Garden tools'
    #collection.featured_product = Product(pk=40)
    #collection.save()


    #Delete a record in the database
    #Version 1 of doing it
    #collection = Collection(pk=11)
    #collection.delete()

    #Version 2 of doing it
    #Collection.objects.filter(id__gt=8).delete()


    #Create a shopping cart with an item
    #shoppingcart = Cart()
    #shoppingcart.save()

    #item = CartItem()
    #item.cart = shoppingcart
    #item.product = Product(pk=44)
    #item.quantity = 2
    #item.save()


    #Update the quantity of an item in the shopping cart
    #cartitem = CartItem.objects.get(pk=5)
    #cartitem.quantity = 9
    #cartitem.save()


    #Remove a shopping cart with its items
    #cartitem = CartItem(pk=30)
    #cartitem.delete()


    #Create an order transaction
    """"
    with transaction.atomic():
        order = Order()
        order.customer_id = 50
        order.save()

        item = OrderItem()
        item.order = order
        orderitem.product_id = 4
        item.quantity = 5
        item.unit_price = 70
    """

    #Create RAW SQL queries
    #query_set = Product.objects.raw('SELECT id,title FROM store_product')

    #Skip Django ORM and connect to the DB directly
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_product')
    



    #for product in query_set:
        #print(product)

    #return render(request, 'hello.html', {'name': 'Azadeh Brownlee', 'result': result })

    #return render(request, 'hello.html', {'name': 'Azadeh Brownlee', 'query_set': list(query_set) })

    #return render(request, 'hello.html', {'name': 'Azadeh Brownlee', 'query_set': list(query_set)})