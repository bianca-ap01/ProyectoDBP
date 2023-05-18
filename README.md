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
- Crear un login de tipo administrador para los miembros del club que sean parte de la directiva. Se pretende mostrar un display para activar, desactivar y borrar miembros, equipos, entre otros modelos.

#### Misión

Crear una aplicación web interactiva que permita el registro de usuarios, equipos y contests para manejar la información del Club de Programación Competitiva.

#### Visión

Se espera que esta página sea tomada como versión beta de la que se desarrollará próximamente para el club.

### Recursos adicionales empleados (front-end, back-end, base de datos)

- Flask-Admin: 
- Flask-Login: empleado para manejar las sesiones de los usuarios. Se usan funciones que indican las rutas a las que puede acceder un usuario
- Werkzeug: se emplea para encriptar las contraseñas de los usuarios

### Ejecución (script, host, etc)

- Base de datos:

Sistema de gestión: Postgresql

```
    psql
    > CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    > create database "dbCPC";
    > \c dbCPC
```

- Script:

1. Clonar el repositorio:
    - SSH:  `git clone git@github.com:bianca-ap01/ProyectoDBP.git`
    - HTTPS: `git clone https://github.com/bianca-ap01/ProyectoDBP.git`

2. Crear y activar un ambiente virtual

```
    python -m venv env
    source env/bin/activate
```

3. Installar las dependencias en el ambiente virtual

```
    pip install -r requerimientos.txt
```

4. Correr la aplicación

```
    python server.py
```

- Creación de tablas

```
    export FLASK_APP=server.py
    flask shell
    > db.create_all()
    > db.session.commit()
    > exit
```

### API, requests and responses

Se emplean requests para solicitar información ingresada en el formulario.

Por implementar:

Codeforces API: Codeforces es una de las pataformas más grandes de programación competitiva que tiene su propio API, el cual proporciona a la app la oportunidad de validar el usuario ingresado, conectar a problemas ya existentes, etc.

### Manejo de errores


200: Caso exitoso
400: Error en el ingreso de datos del formulario
401: Contraseña incorrecta
404: Not Found
500: Error del servidor

