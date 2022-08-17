from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, When, Value, Case, PositiveSmallIntegerField
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.utils.decorators import method_decorator
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django_ajax.decorators import ajax
from .models import  Image, User, Product, Type, Feature, Size, Edit, Shop, Category, Subcategory, Brand
from .forms import ProductForm, ImageFormSet, FeatureFormSet, SizeFormSet

from dal import autocomplete


class ProductListView(ListView):
    model = Product
    template_name = 'clothes/list.html'

    def get_queryset(self):
        qs = super(ProductListView, self).get_queryset()
        return qs.filter(seller=self.request.user)


class SellerMixin(object):
    def get_queryset(self):
        qs = super(SellerMixin, self).get_queryset()
        return qs.filter(seller=self.request.user)


class SellerEditMixin(object):
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super(SellerEditMixin, form).form_valid(form)


class SellerProductMixin(SellerMixin, LoginRequiredMixin):
    model = Product

    success_url = reverse_lazy('clothes:my_list')


class SellerProductEditMixin(SellerProductMixin, SellerEditMixin):

    template_name = 'clothes/create.html'


class ManageProductListView(SellerProductMixin, ListView):
    template_name = 'clothes/list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12
    queryset = Product.objects.all()


@method_decorator([login_required, ], name='dispatch')
class ProductCreateView(SuccessMessageMixin, SellerProductMixin, CreateView, PermissionRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'clothes/create.html'


    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['productimages_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
            context['feature_formset'] = FeatureFormSet(self.request.POST, self.request.FILES)
            context['size_formset'] = SizeFormSet(self.request.POST, self.request.FILES)

        else:
            context['productimages_formset'] = ImageFormSet()
            context['feature_formset'] = FeatureFormSet()
            context['size_formset'] = SizeFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        productimages_formset = context['productimages_formset']
        features_formset = context['feature_formset']
        size_formset = context['size_formset']

        if productimages_formset.is_valid() and features_formset.is_valid() and size_formset.is_valid():
            form.instance.seller = self.request.user
            self.object = form.save()
            productimages_formset.instance = self.object
            productimages_formset.save()
            features_formset.instance = self.object
            features_formset.save()
            size_formset.instance = self.object
            size_formset.save()

            messages.success(self.request, 'Product Successfully Added')
            return redirect('clothes:my_list')

        else:
            return self.render_to_response(self.get_context_data(form=form))


@method_decorator([login_required,], name='dispatch')
class ProductUpdateView(SuccessMessageMixin, SellerProductMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'clothes/create.html'
    form_class = ProductForm
    success_url = reverse_lazy('clothes:my_list')
    success_message = '%(name)s Successfully Updated'


@method_decorator([login_required, ], name='dispatch')
class ProductDeleteView(SuccessMessageMixin, SellerProductMixin, DeleteView, PermissionRequiredMixin):
    template_name = 'clothes/delete.html'
    success_url = reverse_lazy('clothes:my_list')

    success_message = '%(name)s Successfully Deleted'


@method_decorator([login_required, ], name='dispatch')
@method_decorator([login_required, ], name='dispatch')
class ProductImageUpdateView(TemplateResponseMixin, View):
    template_name = 'clothes/formset.html'
    product = None

    def get_formset(self, data=None):
        return ImageFormSet(instance=self.product, data=data)

    def dispatch(self, request, pk):
        self.product = get_object_or_404(Product, id=pk, seller=request.user)
        return super(ProductImageUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'product': self.product, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if request.method == 'POST':
            formset = ImageFormSet(request.POST, request.FILES, instance=self.product)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Image(s) Successfully  Updated')
            return redirect('clothes:my_list')
        else:
            messages.error(request, 'There was a problem updating image(s)')
        return self.render_to_response({'product': self.product, 'formset': formset})


@method_decorator([login_required, ], name='dispatch')
@method_decorator([login_required, ], name='dispatch')
class ProductFeatureUpdateView(TemplateResponseMixin, View):
    template_name = 'clothes/features_formset.html'
    product = None

    def get_formset(self, data=None):
        return FeatureFormSet(instance=self.product, data=data)

    def dispatch(self, request, pk):
        self.product = get_object_or_404(Product, id=pk, seller=request.user)
        return super(ProductFeatureUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'product': self.product, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if request.method == 'POST':
            formset = FeatureFormSet(request.POST, request.FILES, instance=self.product)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Feature(s) Successfully  Updated')
            return redirect('clothes:my_list')
        else:
            messages.error(request, 'There was a problem updating size(s)')
        return self.render_to_response({'product': self.product, 'formset': formset})


@method_decorator([login_required, ], name='dispatch')
@method_decorator([login_required, ], name='dispatch')
class ProductSizeUpdateView(TemplateResponseMixin, View):
    template_name = 'clothes/size_formset.html'
    product = None

    def get_formset(self, data=None):
        return SizeFormSet(instance=self.product, data=data)

    def dispatch(self, request, pk):
        self.product = get_object_or_404(Product, id=pk, seller=request.user)
        return super(ProductSizeUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'product': self.product, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if request.method == 'POST':
            formset = SizeFormSet(request.POST, request.FILES, instance=self.product)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Size(s) Successfully  Updated')
            return redirect('clothes:my_list')
        else:
            messages.error(request, 'There was a problem updating size(s)')
        return self.render_to_response({'product': self.product, 'formset': formset})


def product_detail(request,year,month,day, product):
    product = get_object_or_404(Product, slug=product)
    images = Image.objects.filter(product=product)
    features = Feature.objects.filter(product=product)
    sizes = Size.objects.filter(product=product)
    product_tag_ids = product.tags.values_list('id', flat=True)
    similar_products = Product.objects.filter(Q(tags__in=product_tag_ids) & Q(seller=product.seller)).exclude(
        id=product.id)
    similar_products = similar_products.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:5]
    return render(request, 'clothes/product_detail.html', {'product': product, 'images': images, 'features': features,
                                                     'sizes': sizes, 'similar_products': similar_products})


def edit_detail(request,year,month,day, edit, tag_slug=None):
    edit = get_object_or_404(Edit, slug=edit)
    products = Product.objects.filter(edit=edit)
    order = request.GET.get('order', 'price')
    products = products.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    total_products = products.count()
    paginator = Paginator(products, 24)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'clothes/edit_detail.html', {'order': order, 'products': products, 'page': page, 'tag': tag,
                                                      'total_products': total_products, 'edit': edit})


def shop_detail(request,year,month,day, shop, tag_slug=None):
    shop = get_object_or_404(Shop, slug=shop)
    products = Product.objects.filter(shop=shop)
    order = request.GET.get('order', 'price')
    products = products.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    total_products = products.count()
    paginator = Paginator(products, 24)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'clothes/shop_detail.html', {'order': order, 'products': products, 'page': page, 'tag': tag,
                                                      'total_products': total_products, 'shop': shop})


def category_detail(request,year,month,day, category):
    category = get_object_or_404(Category, slug=category)
    subcategories = Subcategory.objects.filter(category=category)
    order = request.GET.get('order', 'name')
    subcategories = subcategories.order_by(order)

    total_subcategories = subcategories.count()
    paginator = Paginator(subcategories, 24)
    page = request.GET.get('page')
    try:
        subcategories = paginator.page(page)
    except PageNotAnInteger:
        subcategories = paginator.page(1)
    except EmptyPage:
        subcategories = paginator.page(paginator.num_pages)
    return render(request, 'clothes/category_detail.html', {'order': order, 'subcategories': subcategories, 'page': page,
                                                      'total_subcategories': total_subcategories, 'category': category})


def subcategory_detail(request,year,month,day, subcategory, tag_slug=None):
    subcategory = get_object_or_404(Subcategory, slug=subcategory)
    products = Product.objects.filter(subcategory=subcategory)
    order = request.GET.get('order', 'price')
    products = products.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    total_products = products.count()
    paginator = Paginator(products, 24)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'clothes/subcategory_detail.html', {'order': order, 'products': products, 'page': page, 'tag': tag,
                                                      'total_products': total_products, 'subcategory': subcategory})


def products_by_tag(request, tag_slug=None):
    products = Product.objects.all()
    order = request.GET.get('order', 'price')
    products = products.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    total_products = products.count()
    paginator = Paginator(products, 24)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'clothes/product_by_tag.html', {'order': order, 'products': products, 'page': page, 'tag': tag,
                                                      'total_products': total_products})


def type_detail(request,year,month,day, type, tag_slug=None):
    type = get_object_or_404(Type, slug=type)
    products = Product.objects.filter(type=type)
    order = request.GET.get('order', 'price')
    products = products.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    total_products = products.count()
    paginator = Paginator(products, 24)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'clothes/type_detail.html', {'order': order, 'products': products, 'page': page, 'tag': tag,
                                                      'total_products': total_products, 'type': type})


def brand_detail(request,year,month,day, brand, tag_slug=None, ):
    brand = get_object_or_404(Brand, slug=brand)
    products = Product.objects.filter(brand=brand)
    order = request.GET.get('order', 'price')
    products = products.order_by(order)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    total_products = products.count()
    paginator = Paginator(products, 24)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'clothes/brand_detail.html', {'order': order, 'products': products, 'page': page, 'tag': tag,
                                                      'total_products': total_products, 'brand': brand})


def all_brands(request):
    brands = Brand.objects.all()
    order = request.GET.get('name', )
    brands = brands.order_by('name')

    total_brands = brands.count()
    paginator = Paginator(brands, 12)
    page = request.GET.get('page')
    try:
        brands = paginator.page(page)
    except PageNotAnInteger:
        brands = paginator.page(1)
    except EmptyPage:
        brands = paginator.page(paginator.num_pages)
    return render(request, 'clothes/brand_all.html', {'order': order, 'brands': brands, 'page': page, 'total_brands': total_brands})