from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context_processors import csrf
from .models import Category, Product
from cart.forms import CartAddProductForm

def ProductList(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    order_by = request.GET.get("order_by", "")
    if order_by in ("name", "price", "created", "updated"):
        products = products.order_by(order_by)
        if request.GET.get("reverse", "") == '1':
            products = products.reverse()
    else:
        products = products.order_by("created").reverse()

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    context.update(csrf(request))
    return render_to_response('shop/product/detail.html', context)
