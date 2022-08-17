from django.contrib import admin
import datetime
from .models import Type,Shop,Edit,Nav,Category,Subcategory,Product, Brand, Image


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name', 'created']
    list_filter = ['name', 'created']
admin.site.register(Type, TypeAdmin)


class EditAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name', 'created']
    list_filter = ['name', 'created']
admin.site.register(Edit, EditAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name', 'created']
    list_filter = ['name', 'created']
admin.site.register(Brand, BrandAdmin)


class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name', 'created']
    list_filter = ['name', 'created']
admin.site.register(Shop, ShopAdmin)


class NavAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name', 'created']
    list_filter = ['name', 'created']
admin.site.register(Nav, NavAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name', 'created']
    list_filter = ['name', 'created']
admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name', 'created']
    list_filter = ['name', 'created']
admin.site.register(Subcategory, SubcategoryAdmin)


class ImageAdminInline(admin.TabularInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name', 'created']
    list_filter = ['name', 'created']
    inlines = (ImageAdminInline,)
admin.site.register(Product, ProductAdmin)



