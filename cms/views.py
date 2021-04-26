from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery

from .models import OrderItem,Order,Product,Category
from .forms import SearchForm
# Create your views here.

# this view will hep us receive input value on the form

def orders(request):

    if 'user' in request.session:
        current_user = request.session['user']
        param = {'current_user': current_user}
        #return render(request, 'base.html', param)

        form = SearchForm()
        q = ""
        orders =[]
        orders=[]
        delivered_orders=[]
        delivered_orders_count=[]
        pending_orders=[]
        OnTransit=[]
        total_orders=[]

        if 'q' in request.GET:
            form=SearchForm(request.GET)
            if form.is_valid():
                q = form.cleaned_data['q']
                # Utilizing PostgreSQL’s full text search engine by using SearchVector, SearchQuery to enable search on different fields in a module
                orders = Order.objects.annotate(search=SearchVector('customer', 'product', 'status', 'note'),).filter(search=SearchQuery(q))
        else:
            orders = Order.objects.all().order_by('id')

            delivered_orders = orders.filter(status='Delivered')
            pending_orders = orders.filter(status='Pending').count()
            OnTransit = orders.filter(status='OnTransit').count()
            delivered_orders_count = delivered_orders.count()
            total_orders = orders.count()
        context = {
            'form': form,
            'orders': orders,
            'delivered_orders': delivered_orders,
            'delivered_orders_count': delivered_orders_count,
            'pending_orders': pending_orders,
            'OnTransit': OnTransit,
            'total_orders': total_orders,
            'param': param,
        }
        return render(request, 'cms/orders.html', context)

    else:
        return redirect('login')

    return render(request, 'accounts/orders.html', context)



