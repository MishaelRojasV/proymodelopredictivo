from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Tabla de "Paciente"
class Paciente(models.Model):
    idPaciente = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
    nombres = models.CharField(max_length=100)
    apPaterno = models.CharField(max_length=100)
    apMaterno = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    celular = models.CharField(max_length=9,blank=False, null=False)
    genero = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    eliminado = models.BooleanField(default= False)

    def __str__(self):
        return f'{self.nombres} {self.apPaterno} {self.apMaterno}'
    
# Tabla de "Medico"
class Medico(models.Model):
    idMedico = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apPaterno = models.CharField(max_length=100)
    apMaterno = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    celular = models.CharField(max_length=9,blank=True, null=True)
    genero = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    eliminado = models.BooleanField(default= False) 

    def __str__(self):
        return f'{self.nombres} {self.apPaterno} {self.apMaterno}'
    
# Tabla de "Diagnostico"
class Diagnostico(models.Model):
    idDiagnostico = models.AutoField(primary_key=True)
    idPaciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    hipertension = models.BooleanField(default= False)
    cardiopatia = models.BooleanField(default= False)
    nivelGlucosa = models.FloatField(validators=[MinValueValidator(30.0), MaxValueValidator(300.0)])
    icm = models.FloatField(validators=[MinValueValidator(10.0), MaxValueValidator(100.0)])
    estadoFumador = models.CharField(max_length=200)
    tipoTrabajo = models.CharField(max_length=200)
    prediccion = models.BooleanField(default= False, null=True, blank=True)
    fechaRegistro = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.idDiagnostico}'
    
