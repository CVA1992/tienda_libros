from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ventas.models import Pedido
import random

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request,'ventas/lista_pedidos.html', {'pedidos': pedidos})
