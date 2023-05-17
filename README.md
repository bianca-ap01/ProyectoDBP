# Proyecto DBP - 2023-1

## Integrantes

- Bladimir Alferez
- Bianca Aguinaga
- Alvaro García
- Mateo Llallire

### Descripción del proyecto

Se trata de una aplicación web en la que se manejarán los datos del Club de Programación Competitiva de la universidad. Se incluye el registro de usuarios interesados, miembros e información sobre el club.

### Objetivos principales

- Crear un login para usuarios que no sean miembros, ni parte de la directiva. En ella se mostrará información para iniciarse en la programación competitiva.
- Crear un login para miembros del club. 
- Crear un login de tipo administrador para los miembros del club que sean parte de la directiva. Se pretende mostrar un display para activar, desactivar y borrar miembros.

#### Misión

Crear una aplicación web interactiva que permita el registro de usuarios, equipos y contests para manejar la información del Club de Programación Competitiva.

#### Visión

Se espera que esta página sea tomada como versión beta de la que se desarrollará próximamente para el club.

### Recursos adicionales empleados (front-end, back-end, base de datos)

Flask==2.2.3
Flask-Admin==1.6.1
flask-babel==3.1.0
Flask-Login==0.6.2
Flask-Mail==0.9.1
Flask-Migrate==4.0.4
Flask-Principal==0.4.0
Flask-SQLAlchemy==3.0.3


### Ejecución (script, host, etc)

Nombre de la base de datos: dbCPC
Para ejecutar, correr el siguiente comando en la terminal habiendo instalado las dependencias en requerimientos.txt `python server.py`

### API, requests and responses

Se emplean requests para solicitar información ingresada en el formulario.

### Manejo de errores

No implementado en su totalidad.
