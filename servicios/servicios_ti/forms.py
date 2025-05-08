from django import forms
from .models import RecolectoInventario
from .models import AsignacionServicio
from .models import DispositivoPunto
from .models import Dispositivo
from .models import Usuario, ReporteFalla
from .models import Zona
from .models import PuntoVenta
#----------------------------------------------------------------------------------------------------------
class LoginForm(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de Usuario', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password_usuario = forms.CharField(label='Contraseña', max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#-------------------------------------------------------------------------------------------------------------------------------------------

#creacion usuario
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'apellido', 'email', 'password_usuario', 'rol']
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'password_usuario': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

#-----------------------------------------------------------------------------------------------------------
#creacion de zona
class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ['numero_zona', 'nombre_admin_zona', 'apellido_admin_zona', 'telefono', 'orientacion']
        widgets = {
            'numero_zona': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_admin_zona': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_admin_zona': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'orientacion': forms.Select(attrs={'class': 'form-select'}),
        }
#--------------------------------------------------------------------------------------------------------------
# Dispositivos
class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = '__all__'
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'serial': forms.TextInput(attrs={'class': 'form-control'}),
            'imei': forms.TextInput(attrs={'class': 'form-control'}),
            'operador': forms.Select(attrs={'class': 'form-control'}),
            'numero_sincard': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
#-----------------------------------------------------------------------------------------------------------
#punto de venta
class PuntoVentaForm(forms.ModelForm):
    class Meta:
        model = PuntoVenta
        fields = '__all__'
        widgets = {
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'zona': forms.Select(attrs={'class': 'form-control'}),
        }

#------------------------------------------------------------------------------------------------------------
#Asignacinacion de dispositivo
class DispositivoPuntoForm(forms.ModelForm):
    class Meta:
        model = DispositivoPunto
        fields = ['dispositivo', 'punto_venta', 'fecha_instalacion', 'nombre_responsable', 'estado']
        widgets = {
            'fecha_instalacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dispositivo': forms.Select(attrs={'class': 'form-select'}),
            'punto_venta': forms.Select(attrs={'class': 'form-select'}),
            'nombre_responsable': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dispositivos_asignados = DispositivoPunto.objects.values_list('dispositivo_id', flat=True)
        self.fields['dispositivo'].queryset = Dispositivo.objects.exclude(id__in=dispositivos_asignados)
        self.fields['punto_venta'].label_from_instance = lambda \
            obj: f"{obj.numero_punto} - {obj.nombre} - {obj.direccion}"


#-----------------------------------------------------------------------------------------------------------------
#Asignacion:de servicios
class AsignacionServicioForm(forms.ModelForm):
    punto_venta = forms.ModelChoiceField(
        queryset=PuntoVenta.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Punto de Venta',
        empty_label="Seleccione un punto",
    )

    class Meta:
        model = AsignacionServicio
        fields = '__all__'
        widgets = {
            'tecnico': forms.Select(attrs={'class': 'form-select'}),
            'tipo_falla': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_asignacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cambiar las etiquetas visibles del campo punto_venta
        self.fields['punto_venta'].label_from_instance = lambda obj: f"{obj.numero_punto} - {obj.nombre} - {obj.direccion}"
#--------------------------------------------------------------------------------------------------------
#Reporte o cierre del servicio
class ReporteFallaForm(forms.ModelForm):
    asignacion_servicio = forms.ModelChoiceField(
        queryset=AsignacionServicio.objects.filter(estado='pendiente'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Asignación de Servicio",
        empty_label="Seleccione una asignación",
    )

    class Meta:
        model = ReporteFalla
        fields = ['asignacion_servicio', 'descripcion_falla', 'fecha_resolucion', 'tecnico_resolucion', 'estado']
        widgets = {
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fecha_resolucion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tecnico_resolucion': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asignacion_servicio'].label_from_instance = lambda obj: (
            f"N# {obj.id} | {obj.punto_venta.numero_punto} - {obj.punto_venta.nombre} - {obj.punto_venta.direccion} | "
            f"{obj.tecnico} - {obj.tipo_falla} - {obj.fecha_asignacion} - {obj.estado}"
        )
#-------------------------------------------------------------------------------------------------------------------
#recolectar inventario
class RecolectoInventarioForm(forms.ModelForm):

    class Meta:
        model = RecolectoInventario
        fields = ['empleadotic', 'punto_venta', 'tipo_dispositivo', 'serial', 'imei', 'numerosimcard', 'operador']
        widgets = {
            'empleadotic': forms.Select(attrs={'class': 'form-select'}),
            'punto_venta': forms.Select(attrs={'class': 'form-select'}),
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-select'}),
            'serial': forms.TextInput(attrs={'class': 'form-control'}),
            'imei': forms.TextInput(attrs={'class': 'form-control'}),
            'numerosimcard': forms.TextInput(attrs={'class': 'form-control'}),
            'operador': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cambiar las etiquetas visibles del campo punto_venta
        self.fields['punto_venta'].label_from_instance = lambda obj: f"{obj.numero_punto} - {obj.nombre} - {obj.direccion}"
