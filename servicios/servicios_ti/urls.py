from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('menu/', views.menu_view, name='menu'),
    path('logout/', views.logout_view, name='logout'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('zonas/', views.lista_zonas, name='lista_zonas'),
    path('zonas/crear/', views.crear_zona, name='crear_zona'),
    path('zonas/editar/<int:zona_id>/', views.editar_zona, name='editar_zona'),
    path('zonas/eliminar/<int:zona_id>/', views.eliminar_zona, name='eliminar_zona'),
    path('inventario/', views.lista_dispositivos, name='lista_dispositivos'),
    path('inventario/crear/', views.crear_dispositivo, name='crear_dispositivo'),
    path('inventario/editar/<int:dispositivo_id>/', views.editar_dispositivo, name='editar_dispositivo'),
    path('inventario/eliminar/<int:dispositivo_id>/', views.eliminar_dispositivo, name='eliminar_dispositivo'),
    path('puntos_venta/', views.lista_puntos_venta, name='lista_puntos_venta'),
    path('puntos_venta/crear/', views.crear_punto_venta, name='crear_punto_venta'),
    path('puntos_venta/editar/<int:id>/', views.editar_punto_venta, name='editar_punto_venta'),
    path('puntos_venta/eliminar/<int:id>/', views.eliminar_punto_venta, name='eliminar_punto_venta'),
    path('asignar_dispositivo/', views.asignar_dispositivo, name='asignar_dispositivo'),
    path('asignar-servicio/', views.asignar_servicio, name='asignar_servicio'),
    path('cerrar-servicio/', views.cerrar_servicio, name='cerrar_servicio'),
    path('servicios/', views.listar_servicios_estado, name='listar_servicios'),
    path('lista-recolecciones/', views.listar_recolecciones, name='lista_recolecciones'),
    path('recolectar-inventario/', views.recolectar_inventario, name='recolectar_inventario'),
    path('dispositivos-asignados/', views.dispositivos_asignados, name='dispositivos_asignados'),




]







