
from .forms import LoginForm
from django.contrib.auth import logout as auth_logout
from .forms import UsuarioForm
from .models import Zona
from .forms import ZonaForm
from django.shortcuts import get_object_or_404
from .forms import DispositivoForm
from .forms import PuntoVentaForm
from .forms import DispositivoPuntoForm
from .forms import ReporteFallaForm
from django.contrib import messages
from .models import RecolectoInventario
from .forms import RecolectoInventarioForm
from .forms import AsignacionServicioForm
from servicios_ti.models import AsignacionServicio, ReporteFalla
from servicios_ti.models import Dispositivo
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from servicios_ti.models import DispositivoPunto, PuntoVenta, Usuario


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']

            password_usuario = form.cleaned_data['password_usuario']
            try:
                usuario = Usuario.objects.get(nombre_usuario=nombre_usuario, password_usuario=password_usuario)
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre_usuario
                request.session['usuario_rol'] = usuario.rol
                return redirect('menu')
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()
    return render(request, 'servicios_ti/index.html', {'form': form})

def menu_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    rol = request.session.get('usuario_rol')
    return render(request, 'servicios_ti/menu.html', {'rol': rol})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

#--------------------------------------------------------------------------------------------
#creacion usuario y edicion

def crear_usuario(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('lista_usuarios')  # Asegúrate que 'menu' esté configurado en tus urls
    else:
        form = UsuarioForm()

    return render(request, 'crear_usuario.html', {'form': form})

#----------------------------------------------------------------------------------------------
#Gestionar_usuario
def lista_usuarios(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuarios = Usuario.objects.all()
    paginator = Paginator(usuarios, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'lista_usuarios.html', {'page_obj': page_obj})

#------------------------------------------------------------------------------------------------
def editar_usuario(request, usuario_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form})

def eliminar_usuario(request, usuario_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('lista_usuarios')
    return render(request, 'confirmar_eliminar_usuario.html', {'usuario': usuario})
#---------------------------------------------------------------------------------------------------------
#creacion_de zona
def lista_zonas(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    zonas_lista = Zona.objects.all().order_by('numero_zona')
    paginator = Paginator(zonas_lista, 10)  # Muestra 10 zonas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'lista_zonas.html', {'page_obj': page_obj})
#---------------------------------------------------------------------------------------------------------
def crear_zona(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = ZonaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zona creada exitosamente.')
            return redirect('lista_zonas')
    else:
        form = ZonaForm()
    return render(request, 'crear_zona.html', {'form': form})

def editar_zona(request, zona_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    zona = get_object_or_404(Zona, id=zona_id)
    if request.method == 'POST':
        form = ZonaForm(request.POST, instance=zona)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zona actualizada exitosamente.')
            return redirect('lista_zonas')
    else:
        form = ZonaForm(instance=zona)
    return render(request, 'editar_zona.html', {'form': form})

def eliminar_zona(request, zona_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    zona = get_object_or_404(Zona, id=zona_id)
    if request.method == 'POST':
        zona.delete()
        messages.success(request, 'Zona eliminada exitosamente.')
        return redirect('lista_zonas')
    return render(request, 'confirmar_eliminar_zona.html', {'zona': zona})
#----------------------------------------------------------------------------------------------------------
# Lista Dispositivos

def lista_dispositivos(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    dispositivos = Dispositivo.objects.all()

    # Filtros
    serial = request.GET.get('serial')
    imei = request.GET.get('imei')
    tipo = request.GET.get('tipo')
    estado = request.GET.get('estado')

    if serial:
        dispositivos = dispositivos.filter(serial__icontains=serial)
    if imei:
        dispositivos = dispositivos.filter(imei__icontains=imei)
    if tipo:
        dispositivos = dispositivos.filter(tipo=tipo)
    if estado:
        dispositivos = dispositivos.filter(estado=estado)

    # Paginación
    paginator = Paginator(dispositivos, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Valores únicos para filtros desplegables
    tipos = Dispositivo.objects.values_list('tipo', flat=True).distinct()
    estados = Dispositivo.objects.values_list('estado', flat=True).distinct()

    return render(request, 'list_dispositivos.html', {
        'page_obj': page_obj,
        'tipos': tipos,
        'estados': estados,
        'serial': serial or '',
        'imei': imei or '',
        'tipo': tipo or '',
        'estado': estado or ''
    })


#-------------------------------------------------------------------------------------------------------------
def crear_dispositivo(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dispositivo creado exitosamente.')
            return redirect('lista_dispositivos')
    else:
        form = DispositivoForm()
    return render(request, 'crea_dispositivo.html', {'form': form})

def editar_dispositivo(request, dispositivo_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    if request.method == 'POST':
        form = DispositivoForm(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dispositivo actualizado correctamente.')
            return redirect('lista_dispositivos')
    else:
        form = DispositivoForm(instance=dispositivo)
    return render(request, 'edit_dispositivo.html', {'form': form, 'dispositivo': dispositivo})

def eliminar_dispositivo(request, dispositivo_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    if request.method == 'POST':
        dispositivo.delete()
        messages.success(request, 'Dispositivo eliminado correctamente.')
        return redirect('lista_dispositivos')
    return render(request, 'elim_dispositivo.html', {'dispositivo': dispositivo})

#-----------------------------------------------------------------------------------------------------------
#Listar punto de venta

def lista_puntos_venta(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    puntos = PuntoVenta.objects.all()

    numero_punto = request.GET.get('numero_punto')
    if numero_punto:
        puntos = puntos.filter(numero_punto__icontains=numero_punto)

    paginator = Paginator(puntos, 10)  # 10 puntos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'lista_puntos_venta.html', {
        'page_obj': page_obj,
        'numero_punto': numero_punto
    })


def crear_punto_venta(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = PuntoVentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punto de venta creado correctamente.')
            return redirect('lista_puntos_venta')
    else:
        form = PuntoVentaForm()
    return render(request, 'crear_punto_venta.html', {'form': form})

def editar_punto_venta(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    punto = PuntoVenta.objects.get(id=id)
    if request.method == 'POST':
        form = PuntoVentaForm(request.POST, instance=punto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punto de venta actualizado correctamente.')
            return redirect('lista_puntos_venta')
    else:
        form = PuntoVentaForm(instance=punto)
    return render(request, 'editar_punto_venta.html', {'form': form})

def eliminar_punto_venta(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    punto = PuntoVenta.objects.get(id=id)
    if request.method == 'POST':
        punto.delete()
        messages.success(request, 'Punto de venta eliminado correctamente.')
        return redirect('lista_puntos_venta')
    return render(request, 'eliminar_punto_venta.html', {'punto': punto})

#-------------------------------------------------------------------------------------------------------------
#Asignacion de dispositivos

def asignar_dispositivo(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = DispositivoPuntoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Dispositivo asignado exitosamente!')
            return redirect('lista_dispositivos')  # o donde necesites
    else:
        form = DispositivoPuntoForm()

    return render(request, 'asignar_dispositivo.html', {'form': form})
#------------------------------------------------------------------------------------------------------------------
#Asignacion de servicios

def asignar_servicio(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = AsignacionServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio asignado correctamente.')
            return redirect('listar_servicios')

    else:
        form = AsignacionServicioForm()

    return render(request, 'asignar_servicio.html', {'form': form})

#Reporte o cierre del servicio
#-------------------------------------------------------------------------------------------------------------------

def cerrar_servicio(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = ReporteFallaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El servicio ha sido cerrado exitosamente.')
            return redirect('listar_servicios')
    else:
        form = ReporteFallaForm()
    return render(request, 'cerrar_servicio.html', {'form': form})
#-------------------------------------------------------------------------------------------------------------------
#Mostrar servicios
def listar_servicios_estado(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    numero_punto = request.GET.get('numero_punto')
    fecha_report = request.GET.get('fecha_report')

    asignaciones = AsignacionServicio.objects.select_related('punto_venta', 'tecnico')
    servicios = []

    for asignacion in asignaciones:
        reporte = ReporteFalla.objects.filter(asignacion_servicio=asignacion).first()
        estado = 'Abierto'
        if reporte and reporte.estado == 'resuelto':
            estado = 'Cerrado'

        item = {
            'numero_punto': asignacion.punto_venta.numero_punto,
            'id': asignacion.id,
            'punto_venta': asignacion.punto_venta.nombre,
            'tecnico_asignado': f"{asignacion.tecnico}",
            'tipo_falla': asignacion.tipo_falla,
            'fecha_asignacion': asignacion.fecha_asignacion,
            'estado': estado,
            'descripcion': reporte.descripcion_falla if reporte else '',
            'tecnico_resolucion': reporte.tecnico_resolucion if reporte else '',
            'fecha_report': reporte.fecha_reporte if reporte else '',
        }

        if numero_punto and str(asignacion.punto_venta.numero_punto) != numero_punto:
            continue
        if fecha_report and (not reporte or str(reporte.fecha_reporte) != fecha_report):
            continue

        servicios.append(item)

    paginator = Paginator(servicios, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listar_servicios.html', {
        'page_obj': page_obj
    })

#-------------------------------------------------------------------------------------------------------------------
#Recolectar de inventarios recolectados

def recolectar_inventario(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = RecolectoInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_recolecciones')
    else:
        form = RecolectoInventarioForm()
    return render(request, 'recolecto_inventario.html', {'form': form})

#------------------------------------------------------------------------------------------------------------------
#Listar inventarios recogidos
def listar_recolecciones(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    punto_id = request.GET.get('punto')
    puntos = PuntoVenta.objects.all()

    recolectos = RecolectoInventario.objects.all()
    if punto_id:
        recolectos = recolectos.filter(punto_venta_id=punto_id)

    paginator = Paginator(recolectos, 7)  # Mostrar 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'lista_recolecciones.html', {
        'page_obj': page_obj,
        'puntos': puntos,
        'punto_seleccionado': punto_id
    })
#----------------------------------------------------------------------------------------------------------------------
# Dispositivos asignados

def dispositivos_asignados(request):

    if 'usuario_id' not in request.session:
        return redirect('login')

    dispositivos_asignados = DispositivoPunto.objects.select_related(
        'dispositivo', 'punto_venta', 'nombre_responsable'
    )

    # Filtros
    punto_venta_id= request.GET.get('punto_venta') or ''
    tecnico_id  = request.GET.get('tecnico') or ''
    # punto_venta_id = request.GET.get('punto_venta')
    # tecnico_id = request.GET.get('tecnico')

    if punto_venta_id:
        dispositivos_asignados = dispositivos_asignados.filter(punto_venta__id=punto_venta_id)

    if tecnico_id:
        dispositivos_asignados = dispositivos_asignados.filter(nombre_responsable__id=tecnico_id)

    # Paginación
    paginator = Paginator(dispositivos_asignados, 9)  # 9 dispositivos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Para los selects del filtro
    puntos_venta = PuntoVenta.objects.all()
    tecnicos = Usuario.objects.filter(rol__in=['tecnico', 'comunicaciones', 'administrador'])

    return render(request, 'dispositivos_asignados.html', {
        'page_obj': page_obj,
        'puntos_venta': puntos_venta,
        'tecnicos': tecnicos
    })