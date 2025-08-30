from django.contrib import admin

from products.models import Basket, Product, ProductCategory

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Basket)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', 'quantity', 'price', 'image', 'category')
    radio_fields = ('description', 'price')
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp', 'price')
    readonly_fields = ('created_timestamp',)
    extra = 0
