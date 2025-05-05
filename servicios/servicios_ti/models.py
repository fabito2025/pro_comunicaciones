
# Create your models here.

from django.db import models
from django.conf import settings
from django.db.models import Q

class Usuario(models.Model):
    ROLES = [
        ('administrador', 'Administrador'),
        ('tecnico', 'Técnico'),
        ('comunicaciones', 'Comunicaciones')
    ]

    # Campos adicionales
    nombre_usuario= models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rol = models.CharField(max_length=50, choices=ROLES)
    password_usuario = models.CharField(max_length=20)
    email = models.EmailField('correo electrónico', unique=True)
    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['username', 'nombre_completo', 'rol']

    def __str__(self):
        return f"{self.nombre_usuario} {self.apellido} {self.rol}"


class Dispositivo(models.Model):
    TIPOS = [
        ('router', 'Router'),
        ('mikrotik', 'Mikrotik'),
        ('switch', 'Switch'),
        ('radio', 'Radio')
    ]
    OPERADOR = [
        ('tigo', 'Tigo'),
        ('claro', 'Claro'),
        ('movistar', 'Movistar'),
        ('no', 'No')
    ]
    ESTADO = [
        ('SIN_ASIGNAR', 'SIN_ASIGNAR'),
        ('ASIGNADO', 'ASIGNADO'),

    ]
    tipo = models.CharField(max_length=100, choices=TIPOS)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serial = models.CharField(max_length=100,unique=True)
    imei = models.CharField(max_length=15, unique=True, null=True, blank=True)
    operador = models.CharField(max_length=100, choices=OPERADOR)
    numero_sincard = models.CharField(max_length=15,null=True, blank=True, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=100, choices= ESTADO)

    def __str__(self):
        return f"{self.tipo} - {self.imei} - {self.serial} - {self.estado}"

class Zona(models.Model):
    ORIENTACION = [
        ('ciudad', 'Ciudad'),
        ('poblaciones', 'Poblaciones'),
    ]

    numero_zona = models.PositiveIntegerField(unique=True)
    nombre_admin_zona = models.CharField(max_length=255)
    apellido_admin_zona = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    orientacion = models.CharField(max_length=20, choices=ORIENTACION)


    def __str__(self):
        return f"Zona {self.numero_zona} - {self.nombre_admin_zona} - {self.apellido_admin_zona} - {self.telefono}"


class PuntoVenta(models.Model):
    objects = None
    MODALIDAD = [
        ('local', 'Local'),
        ('compumovil', 'Compumovil'),
    ]
    numero_punto = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    modalidad = models.CharField(max_length=25, choices=MODALIDAD)
    rango_valor = models.PositiveIntegerField()
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)  # Relación nueva con Zona


    def __str__(self):
        return f"{self.numero_punto} - {self.nombre} {self.direccion} {self.modalidad} {self.rango_valor} {self.zona}"


class DispositivoPunto(models.Model):
    ESTADO = [
        ('SIN_ASIGNAR', 'SIN_ASIGNAR'),
        ('ASIGNADO', 'ASIGNADO'),

    ]
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    punto_venta = models.ForeignKey(PuntoVenta, on_delete=models.CASCADE)
    fecha_instalacion = models.DateField()
    nombre_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to=Q(rol='tecnico') | Q(rol='comunicaciones') | Q(rol='administrador')
    )
    estado = models.CharField(max_length=100, choices=ESTADO,null=False)

    def __str__(self):
        return f"{self.dispositivo} en {self.punto_venta} {self.fecha_instalacion } {self.nombre_responsable} {self.estado}"


class AsignacionServicio(models.Model):
    ESTADO = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
    ]

    TIPOFALLA = [
        ('cable partido', 'Cable partido'),
        ('perdida de conexion', 'Pérdida de conexión'),
        ('antena caida', 'Antena caída'),
        ('instalacion de antena', 'Instalación de antena'),
        ('reubicacion de caja', 'Reubicación de caja'),
        ('desmonte dispositivos', 'Desmonte dispositivos'),
        ('inventario', 'Inventario')
    ]
    punto_venta = models.ForeignKey(PuntoVenta, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to=Q(rol='tecnico') | Q(rol='comunicaciones') | Q(rol='administrador')
    )
    tipo_falla = models.CharField(max_length=255, choices=TIPOFALLA)
    telefono = models.CharField(max_length=15)
    fecha_asignacion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO, default='pendiente')

    def __str__(self):
        return f"Asignación a {self.tecnico} para {self.punto_venta} {self.tipo_falla} estado: {self.estado}"



class ReporteFalla(models.Model):
    asignacion_servicio = models.ForeignKey(AsignacionServicio, on_delete=models.CASCADE)
    descripcion_falla = models.TextField()
    fecha_reporte = models.DateField(auto_now_add=True)
    fecha_resolucion = models.DateField(null=True, blank=True)
    tecnico_resolucion = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to=Q(rol='tecnico') | Q(rol='comunicaciones') | Q(rol='administrador')
    )
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('resuelto', 'Resuelto')], default='pendiente')

    def __str__(self):
        return f"Falla reportada: {self.asignacion_servicio } {self.tecnico_resolucion} {self.estado} {self.descripcion_falla[:30]}..."


class UsuarioMovimiento(models.Model):
    tabla = models.CharField(max_length=100)
    accion = models.CharField(max_length=10)
    fila_id = models.IntegerField(null=True, blank=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    datos_antiguos = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    usuario_app = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimientos'
    )

    def __str__(self):
        return f"{self.tabla} - {self.accion} - ID {self.fila_id} - {self.fecha_movimiento.strftime('%Y-%m-%d %H:%M:%S')}"


class RecolectoInventario(models.Model):
    TIPO_DISPOSITIVO = [
        ('router', 'Router'),
        ('mikrotik', 'Mikrotik'),
        ('switch', 'Switch'),
        ('radio', 'Radio'),
        ('otro', 'Otro'),
    ]

    OPERADOR = [
        ('tigo', 'Tigo'),
        ('claro', 'Claro'),
        ('movistar', 'Movistar'),
        ('no', 'No'),
    ]

    empleadotic = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to=Q(rol='tecnico') | Q(rol='comunicaciones') | Q(rol='administrador'),
        verbose_name="Empleado TIC"
    )
    punto_venta = models.ForeignKey(PuntoVenta, on_delete=models.CASCADE)

    tipo_dispositivo = models.CharField(max_length=50, choices=TIPO_DISPOSITIVO, null=True, blank=True)
    serial = models.CharField(max_length=100, null=True, blank=True)
    imei = models.CharField(max_length=15, null=True, blank=True)
    numerosimcard = models.CharField(max_length=15, null=True, blank=True)
    operador = models.CharField(max_length=20, choices=OPERADOR, null=True, blank=True)
    fecha_recoleccion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.punto_venta} - {self.tipo_dispositivo} - Serial: {self.serial}, IMEI: {self.imei}, SIM: {self.numerosimcard}, Operador: {self.operador}, Técnico: {self.empleadotic}, Técnico: {self.fecha_recoleccion}"