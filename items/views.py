from datetime import datetime
import email
from nis import cat
from pickle import NONE
from tkinter import ON
from tkinter.tix import Tree
from typing_extensions import Self
from xml.etree.ElementTree import Element
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count, Q
from django.urls import reverse
from django.utils import timezone
from pyparsing import line

from items.models import item , categoria, usuario, prestamo


# Create your views here.


def index(request):
    print('Request para index')


    #
    # Descomentar y ejecutar sólo si se deben insertar datos de usuarios desde un .csv que se encuentre en la carpeta raíz
    #
    # arch = open('usuarios.csv', 'r')
    
    # for linea in arch:
    #     #print(linea)
    #     linea = linea.split(',')
    #     usuario_ = linea[1].replace('"','')
    #     rut_ = linea[0].replace('"','')
    #     rol_ = linea[0].replace('"','')
    #     correo_ = linea[4].replace('\n','').replace('"','')

    #     new_user = usuario(nombre = usuario_, rut=rut_, rol=rol_, correo=correo_)
    #     new_user.save()

    #     print("\nnombre: " + usuario_ + '\n\tcorreo: '+ correo_ + '\n\trol: '+ rol_+ '\n\trut: '+ rut_)
    # arch.close()

    items = item.objects.order_by("disponible")
    usuarios = usuario.objects.all()
    prestamos = prestamo.objects.all()
    categorias = categoria.objects.all()

    arreglo = []
    for caca in items:
        if caca.disponible == False:
            prestamo_aux = prestamos.filter(item__id = caca.id, devuelto = False).first()
            xd = caca , prestamo_aux.usuario, prestamo_aux.fecha_prestamo
            arreglo.append(xd)
        
        else:
            xd = caca, '',''
            arreglo.append(xd)

    return render(request, 'index.html', {'items': arreglo, 'usuarios':usuarios, 'prestamos':prestamos, 'categorias':categorias})



def filtro(request):
    print('Request para filtro')

    chek_1 = request.POST.get('Check-1')
    chek_2 = request.POST.get('Check-2')
    chek_3 = request.POST.get('Check-3')
    chek_4 = request.POST.get('Check-4')
    chek_5 = request.POST.get('Check-5')
    chek_6 = request.POST.get('Check-6')

    casillas = [chek_1, chek_2, chek_3, chek_4, chek_5, chek_6]
    print(casillas, '\n')

    if (chek_1 != None and chek_2 != None):
        items = item.objects.order_by("disponible")
    
    elif (chek_1 == None and chek_2 != None):
        items = item.objects.filter(disponible = False)
        
    elif (chek_1 != None and chek_2 == None):
        items = item.objects.filter(disponible = True)
    
    else:
        items = item.objects.filter(categoria = '')


    items_1 = []
    items_2 = []
    items_3 = []
    items_4 = []

    if (chek_4 != None ):
        items_1 = items.filter(categoria__categoria = 'juego')

    if (chek_3 != None ):
        items_2 = items.filter(categoria__categoria = 'computador')

    if (chek_5 != None ):
        items_3 = items.filter(categoria__categoria = 'raspberry')

    if (chek_6 != None ):
        items_4 = items.filter(categoria__categoria = 'otro')


    items = list(items_1) + list(items_2) + list(items_3) + list(items_4)

    usuarios = usuario.objects.all()
    prestamos = prestamo.objects.all()
    categorias = categoria.objects.all()

    print(items)

    arreglo = []
    for caca in items:
        if caca.disponible == False:
            prestamo_aux = prestamos.filter(item__id = caca.id, devuelto = False).first()
            xd = caca , prestamo_aux.usuario, prestamo_aux.fecha_prestamo
            arreglo.append(xd)
        
        else:
            xd = caca, '',''
            arreglo.append(xd)
    
    


    return render(request, 'index.html', {'items': arreglo, 'casillas': casillas, 'usuarios':usuarios, 'prestamos':prestamos, 'categorias':categorias})


def buscar(request):
    print('Request para busqueda')

    busqueda = request.POST.get('busqueda')

    def normalize(s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s
    
    busqueda = normalize(busqueda)

    items = item.objects.filter(Q(nombre__icontains = busqueda))

    usuarios = usuario.objects.all()
    prestamos = prestamo.objects.all()
    categorias = categoria.objects.all()

    arreglo = []
    for caca in items:
        if caca.disponible == False:
            prestamo_aux = prestamos.filter(item__id = caca.id, devuelto = False).first()
            xd = caca , prestamo_aux.usuario, prestamo_aux.fecha_prestamo
            arreglo.append(xd)
        
        else:
            xd = caca, '',''
            arreglo.append(xd)

    return render(request, 'index.html', {'items': arreglo, 'usuarios':usuarios, 'prestamos':prestamos, 'categorias':categorias})



def prestar(request):
    print('Request para prestar')

    item_id= request.POST.get('itemid')
    rol = request.POST.get('user_name')

    print('\n\t usuario: '+ str(rol)+'\t\n')

    print("id del item: ",item_id)

    elemento = get_object_or_404(item, pk=item_id)

    user = usuario.objects.filter(Q(rol=rol) | Q(rut=rol)).first()

    if(user):
        print(elemento)
        print(user)

        prestamo_ = prestamo(usuario = user, item = elemento, fecha_prestamo = timezone.now())
        prestamo_.save()

        elemento.disponible = False
        item.save(elemento)

    else:
        items = item.objects.order_by("disponible")
        usuarios = usuario.objects.all()
        prestamos = prestamo.objects.all()
        categorias = categoria.objects.all()

        arreglo = []
        for caca in items:
            if caca.disponible == False:
                prestamo_aux = prestamos.filter(item__id = caca.id, devuelto = False).first()
                xd = caca , prestamo_aux.usuario, prestamo_aux.fecha_prestamo
                arreglo.append(xd)
            
            else:
                xd = caca, '',''
                arreglo.append(xd)

        return render(request, 'index.html', {'items': arreglo, 'usuarios':usuarios, 'prestamos':prestamos, 'categorias':categorias, 'mensaje_alerta':'usuario no encontrado'})

    items = item.objects.order_by("disponible")
    usuarios = usuario.objects.all()
    prestamos = prestamo.objects.all()
    categorias = categoria.objects.all()

    arreglo = []
    for caca in items:
        if caca.disponible == False:
            prestamo_aux = prestamos.filter(item__id = caca.id, devuelto = False).first()
            xd = caca , prestamo_aux.usuario, prestamo_aux.fecha_prestamo
            arreglo.append(xd)
            
        else:
            xd = caca, '',''
            arreglo.append(xd)

    mensaje = str(elemento) , 'prestado correctamente'
    
    return render(request, 'index.html', {'items': arreglo, 'usuarios':usuarios, 'prestamos':prestamos, 'categorias':categorias, 'mensaje_prestado':mensaje})



def devolver(request):
    print('Request para devolver')

    item_id= request.POST.get('itemidd')
    elemento = get_object_or_404(item, pk=item_id)
    elemento_prestamo = prestamo.objects.filter(item=elemento, devuelto = False).first()

    elemento_prestamo.fecha_devuelto = timezone.now()
    elemento_prestamo.devuelto = True
    prestamo.save(elemento_prestamo)

    elemento.disponible = True
    item.save(elemento)

    return HttpResponseRedirect(reverse('index'))

def agregar(request):
    print("request agregar")

    return(render(request, 'agregar_item.html'))

def agregar_item(request):
    print("request agregar_item")

    nombre = request.POST.get('nombre')
    codigo = request.POST.get('codigo')
    categoria_ = request.POST.get('categoria')
    description = request.POST.get('comentario')

    categoria_aux = categoria.objects.filter(categoria=categoria_).first()

    item_ = item(nombre = nombre, codigo=codigo, categoria = categoria_aux, description = description, disponible=True)
    item_.save()

    mensaje = str(nombre), ' agregado correctamente '


    return(render(request, 'agregar_item.html', {'mensaje':mensaje}))

def item_(request, id):
    print("request de item")

    item_ = get_object_or_404(item, pk=id)
    prestamos = prestamo.objects.filter(item=item_).order_by("-fecha_prestamo")



    return(render(request, 'item.html', {'item':item_, 'prestamos':prestamos}))

def view_404(request, exception=None):
    # make a redirect to homepage
    # you can use the name of url or just the plain link
    return HttpResponseRedirect(reverse('index')) # or redirect('name-of-index-url')

def usuarios(request):
    usuarios = usuario.objects.all()

    return(render(request, 'usuarios.html', {'usuarios':usuarios}))

def agregar_usuario(request):
    print("request agregar_usuario")

    return(render(request, 'agregar_usuario.html'))

def agregar_usuario_(request):
    print("request agregar_usuario")

    nombre = request.POST.get('nombre')
    email = request.POST.get('email')
    rol = request.POST.get('rol')
    rut = request.POST.get('rut')

    user = usuario(nombre = nombre, correo=email, rol=rol, rut=rut)
    user.save()

    mensaje = str(nombre), ' agregado correctamente'

    return(render(request, 'agregar_usuario.html', {'mensaje':mensaje}))

def busqueda_user(request):
    busqueda = request.POST.get('busqueda')
    print('\n\t'+str(busqueda)+'\t\n')

    usuarios = usuario.objects.filter(Q(nombre__icontains = busqueda) | Q(rol__icontains = busqueda) | Q(rut__icontains = busqueda))


    
    return(render(request, 'usuarios.html', {'usuarios':usuarios}))
