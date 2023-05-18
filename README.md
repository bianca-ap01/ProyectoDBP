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

### API Endpoints

| Método | Endpoint            | Descripción |
|--------|---------------------|-------------|
| GET    | /members            | Retorna una lista de todos los miembros junto con su información de usuario.|
| POST   | /members            | No implementado en el código proporcionado. |
| GET    | /logout             | Cierra la sesión del usuario actualmente conectado y redirige a la página de inicio. |
| GET    | /profile/edit/      | Retorna la página para editar el perfil del usuario actualmente conectado. |
| POST   | /profile/edit/      | Acepta los datos del formulario para actualizar el perfil del usuario actualmente conectado. |
| GET    | /profile            | Retorna la página de perfil del usuario actualmente conectado. |
| GET    | /lectures           | Retorna una lista de todas las lecturas. |
| GET    | /lectures/<int:id>  | Retorna la página de una lectura específica. |
| GET    | /lectures/<int:id>/edit | Retorna la página para editar una lectura específica. |
| POST   | /lectures/<int:id>/edit | Acepta los datos del formulario para actualizar una lectura específica. |
| GET    | /lectures/new       | Retorna la página para crear una nueva lectura. |
| POST   | /lectures/new       | Acepta los datos del formulario para crear una nueva lectura. |
| GET    | /contests/<_title>  | Retorna la página de un concurso específico. |
| GET    | /contests           | Retorna una lista de todos los concursos. |
| GET    | /contests/new       | Retorna la página para crear un nuevo concurso. |
| POST   | /contests/new       | Acepta los datos del formulario para crear un nuevo concurso. |
| GET    | /problems           | Retorna una lista de todos los problemas. |
| GET    | /problems/new       | Retorna la página para crear un nuevo problema. |
| POST   | /problems/new       | Acepta los datos del formulario para crear un nuevo problema. |
| POST   | /problems/create    | Crea un nuevo problema basado en los datos enviados en formato JSON. |
| GET    | /pendings           | No implementado en el código proporcionado. |
| GET    | /users              | Retorna una lista de todos los usuarios. |
| GET    | /board              | Retorna una lista de todos los miembros del consejo. |
| GET    | /professors         | Retorna una lista de todos los profesores. |
| GET    | /professors/new     | Retorna la página para registrar un nuevo profesor. |
| POST   | /professors/new     | Acepta los datos del formulario para registrar un nuevo profesor. |


### Manejo de errores


200: Caso exitoso
400: Error en el ingreso de datos del formulario
401: Contraseña incorrecta
404: Not Found
500: Error del servidor

