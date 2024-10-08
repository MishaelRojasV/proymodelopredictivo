from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from seguridadapp.models import Paciente, Medico, Diagnostico
from datetime import date


#-------------------------------------- Formulario para Crear Uusario-------------------------------------
class CrearUserForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Nombres (opcional)', required=False)
    last_name = forms.CharField(label='Apellidos (opcional)', required=False)
    email = forms.EmailField(label='Correo Electrónico (opcional)', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_active']
        help_texts = {
            'is_active': ('Indica si este usuario debe ser tratado como activo. Desactive esto en lugar de eliminar cuentas.'),
            'is_superuser': ('Designa que este usuario tiene todos los permisos sin asignarlos explícitamente.'),
        }

    def __init__(self, *args, **kwargs):
        super(CrearUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
#-------------------------------Formulario para Editar Uusario----------------------------------
class EditarUserForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_active']
        help_texts = {
            'is_active': ('Indica si este usuario debe ser tratado como activo. Desactive esto en lugar de eliminar cuentas.'),
            'is_superuser': ('Designa que este usuario tiene todos los permisos sin asignarlos explícitamente.'),
        }

#-------------------------------Formulario para Editar Paciente----------------------------------
class EditarPacienteForm(forms.ModelForm):    
    class Meta:
        model = Paciente
        fields = ['nombres','apPaterno','apMaterno','email','celular','genero','fecha_nacimiento']

    def __init__(self, *args, **kwargs):
        super(EditarPacienteForm, self).__init__(*args, **kwargs)
        self.fields['genero'].disabled = True
        self.fields['fecha_nacimiento'].disabled = True

#-------------------------------Formulario para Crear Medico----------------------------------
class CrearMedicoForm(forms.ModelForm):    
    GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]

    genero = forms.ChoiceField(choices=GENERO_CHOICES)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Medico
        fields = ['nombres','apPaterno','apMaterno','email','celular','genero','fecha_nacimiento', 'user']

    def __init__(self, *args, **kwargs):
        super(CrearMedicoForm, self).__init__(*args, **kwargs)
        # Filtrar usuarios que no estén ya asociados ni a un médico ni a un paciente
        usuarios_ocupados_medicos = Medico.objects.values_list('user', flat=True)
        usuarios_ocupados_pacientes = Paciente.objects.values_list('user', flat=True)
        usuarios_ocupados = list(usuarios_ocupados_medicos) + list(usuarios_ocupados_pacientes)
        self.fields['user'].queryset = User.objects.exclude(id__in=usuarios_ocupados)

#-------------------------------Formulario para Editar Medico----------------------------------
class EditarMedicoForm(forms.ModelForm):    
    class Meta:
        model = Medico
        fields = ['nombres','apPaterno','apMaterno','email','celular','genero','fecha_nacimiento', 'user']

    def __init__(self, *args, **kwargs):
        super(EditarMedicoForm, self).__init__(*args, **kwargs)
        self.fields['genero'].disabled = True
        self.fields['fecha_nacimiento'].disabled = True
        self.fields['user'].disabled = True

#-------------------------------Formulario para Diagnostico 01----------------------------------
class DiagnosticoForm(forms.ModelForm):
    GENERO_CHOICES = [
        ('0', 'Femenino'),
        ('1', 'Masculino'),
    ]

    ESTADO_FUMADOR_CHOICES = [
        ('0', 'No opina'),
        ('1', 'Anteriormente fumó'),
        ('2', 'Nunca fumó'),
        ('3', 'Fuma'),
    ]

    TIPO_TRABAJO_CHOICES = [
        ('0', 'Trabajador para el gobierno'),
        ('1', 'Nunca trabajó'),
        ('2', 'Trabajador privado'),
        ('3', 'Trabajador por cuenta propia'),
    ]

    Genero = forms.ChoiceField(choices=GENERO_CHOICES)
    EstadoFumador = forms.ChoiceField(choices=ESTADO_FUMADOR_CHOICES)
    TipoTrabajo = forms.ChoiceField(choices=TIPO_TRABAJO_CHOICES)
    fechaRegistro = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Diagnostico
        fields = ['Genero', 'Edad', 'Hipertension', 'Cardiopatia', 'Nivel_GlucosaPromedio', 'ICM', 'EstadoFumador', 'TipoTrabajo']

    def __init__(self, *args, **kwargs):
        paciente = kwargs.pop('paciente', None)
        super(DiagnosticoForm, self).__init__(*args, **kwargs)
        
        if paciente:
            # Jalar el género del paciente
            self.fields['Genero'].initial = '1' if paciente.genero == 'M' else '0'
            
            # Calcular la edad según la fecha de nacimiento
            today = date.today()
            born = paciente.fecha_nacimiento
            self.fields['Edad'].initial = today.year - born.year - ((today.month, today.day) < (born.month, born.day))