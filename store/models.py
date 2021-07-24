from django.db import models


class Promotion(models.Model):
    #ManytoMany relationship betw Products & Promotions
    description = models.CharField(max_length=255)
    discount = models.FloatField()
   




class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL,null=True, related_name='+') #solving circular relationships



class Product(models.Model):
    sku = models.CharField(max_length=10)
    slug = models.SlugField(default='-')
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)



class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]

class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'D'

    PAYMENT_STATUS=[
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    
    ]


    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS,default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)



class Adress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100, null=True)
    #customer = models.OneToOneField(Customer, on_delete=models.CASCADE) # on_delete=models.SET_NULL if you want the child to not get deleted after the parent. #PROTECT doesnt allow the cancellation of parent
    
    #OneToOne relationship between Adress and Customer
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, unique=True) #Now the adress.customer is dependant on a link/foreign key to a Customer // Setting unique=True on a ForeignKey has the same effect as using a OneToOneField



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)




class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()