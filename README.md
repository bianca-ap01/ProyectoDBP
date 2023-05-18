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

- Flask-Admin
- Flask-Login
- Flask-SQLAlchemy
- Flask-Migrate
- Werkzeug

### Ejecución (script, host, etc)

- Base de datos:

Sistema de gestión: ![https://github.com/bianca-ap01/ProyectoDBP.git](Postgresql)

```
    psql
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

```pip install -r requerimientos.txt
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

No implementado en su totalidad.
