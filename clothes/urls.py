from . import views
from django.conf.urls import url


app_name = 'clothes'
urlpatterns = [
    url(r'^mine/$', views.ManageProductListView.as_view(), name='my_list'),
    url(r'^create/$', views.ProductCreateView.as_view(), name='product_add'),
    url(r'^(?P<pk>\d+)/edit/$', views.ProductUpdateView.as_view(), name='product_edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.ProductDeleteView.as_view(), name='product_delete'),
    url(r'^(?P<pk>\d+)/images/$', views.ProductImageUpdateView.as_view(), name='product_image_update'),
    url(r'^(?P<pk>\d+)/features/$', views.ProductFeatureUpdateView.as_view(), name='product_feature_update'),
    url(r'^(?P<pk>\d+)/sizes/$', views.ProductSizeUpdateView.as_view(), name='product_size_update'),
    url(r'^product/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<product>[-\w]+)/$',
        views.product_detail,
        name='product-detail'),
    url(r'^brands/$', views.all_brands, name='brands'),
    url(r'^edit/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<edit>[-\w]+)/$',
        views.edit_detail,
        name='edit-detail'),
    url(r'^shop/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<shop>[-\w]+)/$',
        views.shop_detail,
        name='shop-detail'),

    url(r'^category/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<category>[-\w]+)/$',
        views.category_detail,
        name='category-detail'),

    url(r'^type/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<type>[-\w]+)/$',
        views.type_detail,
        name='type-detail'),

    url(r'^brand/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<brand>[-\w]+)/$',
        views.brand_detail,
        name='brand-detail'),

    url(r'^subcategory/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<subcategory>[-\w]+)/$',
        views.subcategory_detail,
        name='subcategory-detail'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.products_by_tag,
        name='products_by_tag'),

         ]


