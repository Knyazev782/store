from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory



class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset().order_by('id')
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context


@login_required
def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def baskets_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_update(request, basket_id):
    if request.method == 'POST':
        basket = Basket.objects.get(id=basket_id, user=request.user)
        new_quantity = int(request.POST.get('quantity', 0))
        if new_quantity >= 0:
            basket.quantity = new_quantity
            basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('products:index')))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('products:index')))