from django import forms

class LoginForm(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de Usuario', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password_usuario = forms.CharField(label='Contraseña', max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#-------------------------------------------------------------------------------------------------------------------------------------------

#creacion usuario

from django import forms
from .models import Usuario

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

from django import forms
from .models import Zona

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

from django import forms
from .models import Dispositivo

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
from django import forms
from .models import PuntoVenta

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

from django import forms
from .models import DispositivoPunto

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
#-----------------------------------------------------------------------------------------------------------------
#Aignacion:de servicios
from django import forms
from .models import AsignacionServicio

class AsignacionServicioForm(forms.ModelForm):
    class Meta:
        model = AsignacionServicio
        fields = '__all__'
        widgets = {
            'punto_venta': forms.Select(attrs={'class': 'form-select'}),
            'tecnico': forms.Select(attrs={'class': 'form-select'}),
            'tipo_falla': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_asignacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
#Reporte o cierre del servicio
from django import forms
from .models import ReporteFalla

class ReporteFallaForm(forms.ModelForm):
    class Meta:
        model = ReporteFalla
        fields = ['asignacion_servicio', 'descripcion_falla', 'fecha_resolucion', 'tecnico_resolucion', 'estado']
        widgets = {
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fecha_resolucion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'asignacion_servicio': forms.Select(attrs={'class': 'form-select'}),
            'tecnico_resolucion': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
#-------------------------------------------------------------------------------------------------------------------
#recolectar inventario

from django import forms
from .models import RecolectoInventario

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

