# proymodelopredictivo
Sistema Web en Django para mostrar el modelo predictivo implementado

Pasos

1. Instalan el Django 
        pip install django

2. Instalan Dependencias 
        pip install -r requirements.txt

3. Cambian de nombre el archivo .env-example por .env

4. Configuran segun su base de datos(Usen PhpMyadmin o Mysql Workbench)

5. Ejecutan las Migraciones 
        python manage.py makemigrations
        python manage.py migrate

6. Crean un superusuario
    python manage.py createsuperuser

7. Listo