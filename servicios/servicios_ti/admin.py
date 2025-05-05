
from django.contrib import admin
from .models import Usuario, Dispositivo, PuntoVenta, DispositivoPunto, AsignacionServicio, ReporteFalla, Zona, UsuarioMovimiento,RecolectoInventario


# Registra los modelos en el admin
admin.site.register(Usuario)
admin.site.register(Dispositivo)
admin.site.register(PuntoVenta)
admin.site.register(DispositivoPunto)
admin.site.register(AsignacionServicio)
admin.site.register(ReporteFalla)
admin.site.register(Zona)
admin.site.register(UsuarioMovimiento)
admin.site.register(RecolectoInventario)

