from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


#Creating a custom filter class
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [('<10', 'LOW')]

    def lookups(self, request, model_admin):
        return [('>50', 'WELL STOCKED')]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

    def queryset(self, request, queryset):
        if self.value() == '>50':
            return queryset.filter(inventory__gt=50)






@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection'] #gives a search field in the drop down list
    prepopulated_fields = {
        'slug':['title']
    }
    exclude = ['promotions']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price','description','inventory_status','collection','last_update']
    list_editable = ['unit_price', ]
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 100
    search_fields = ['title']
    list_select_related = ['collection']


    def collection_title(self, product):
        return product.collection.title


    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        threshold = 10
        if product.inventory < threshold:
            return 'Low'
        return 'OK'


    #Creating a custom action
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} Products were succesfully updated', messages.WARNING)
    






@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership','birth_date','email', 'orders_placed']
    ordering = ['first_name']
    readonly_fields = ['birth_date']
    list_per_page = 10
    list_editable = ['membership']
    list_filter =  ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith'] #Case insensitive search


    @admin.display(ordering='orders_placed')
    def orders_placed(self,customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{}</a>', url, customer.orders_placed)

    def get_queryset(self,request):
        return super().get_queryset(request).annotate(orders_placed=Count('order'))
        


#Overriding Base Querysets to create a column that doesnt exist as an attribute to the object
#such as product count
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured_product','products_count']
    search_fields = ['title']

    #Here we are making sure when clicking collection, user is sent to a filtered view of products
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist') 
            + '?' 
            + urlencode({
                'collection__id': str(collection.id)
            }))

        return format_html('<a href="{}">{}<a/>', url, collection.products_count)
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))



class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0 # if you dont want additional row placeholders
    
    



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['placed_at','payment_status','customer']
    list_filter =  ['payment_status']
    list_select_related = ['customer']

   



@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity','unit_price']



@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['description','discount']

