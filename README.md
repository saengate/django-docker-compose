[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/saengate/django-docker-compose)](https://github.com/saengate/django-docker-compose/releases/latest)
[![GitHub contributors](https://img.shields.io/github/contributors/saengate/django-docker-compose)](https://github.com/saengate/django-docker-compose/graphs/contributors)

# Descargar el proyecto

El proyecto usa submodulos, por lo que para descargarlo apropiadamente debes usar:
* `git clone git@github.com:saengate/django-docker-compose.git django-docker-compose`

# Instalación con docker y docker-compose

## Requerimientos

Para poder instalar el proyecto requieres tener instalado

* [`docker`](https://docs.docker.com/engine/install/)
* [`docker-compose`](https://docs.docker.com/compose/install/)

## Instalación

* Crea un archivo con nombre `.env` en la raíz del proyecto.
* Contruye el proyecto:
  * `docker compose build`
* Ejecuta el siguiente comando para levantar el proyecto
  * `docker compose up` puedes usar en las siguientes ocasiones el parametro `--remove-orphans` para evitar que contenedores huerfanos te impidan levantar los contenedores.
* Opcional: Ingresa al contenedor del backend y crea el usuario administrador de django:
  1. `docker compose exec backend bash`: este comando te permite acceder al contenedor `backend` del proyecto. Puedes sustituir `backend` por el nombre de cualquier otro servicio descrito en el `docker-compose.yml`.
  2. `source venv`: Activa el entorno virtual python, solo dentro del contenedor `backend`.
  3. `cmdp -ca`: Crea el usuario administrador, solo dentro del contenedor `backend`.
    El usuario `administrador` creado a partir del comando anterio es el siguiente:
      - usuario:    `admin`
      - contraseña: `admin`

# Desarrollo - Uso diario
## Levantar contenedores

* Puedes usar la opción `-d` para levantar los contenedores en segundo plano
  `docker compose up -d`

* Ingresa al contenedor del backend y levanta el servicio usando `./manage.py runserver 0.0.0.0:7010`. es recomendable hacerlo desde el debbuger de vscode `Python: Django`.
* Ingresa al contenedor del frontend y levanta el servicio usando `npm run start -- --port=80 --spa`. es recomendable hacerlo desde el debbuger de vscode `Service`.

* Usa el comando `stop` para detener los contenedores sin borrarlos o `down` para detenerlos y borrarlos
  - `docker compose stop` (Solo los detiene)
  - `docker compose down` (Los detiene y los borra, útil cuando se han reconstruido los contenedores)

* Si levantas los contenedores con `docker compose up` usar `CTRL + C` bastara para detenerlos.

## Editor

Eres libre de usar el editor que prefieras, por facilidad se agregan configuraciones asociadas a [VSCode](https://code.visualstudio.com/), por lo que si usas este editor el equipo de desarrollo puede coordinarse mejor y ayudarte en las configuraciones iniciales.
Entre plugins más importantes que necesitaras para el desarrollo están los siguientes y se han agregado por defecto en el proyecto, cuando se levante el contenedor instala los `paquetes recomendados`:
  - Docker: [ms-azuretools.vscode-docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
  - Docker Compose: [p1c2u.docker-compose](https://marketplace.visualstudio.com/items?itemName=p1c2u.docker-compose)
  - Remote - Containers: [ms-vscode-remote.remote-containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
  - Remote - SSH: [ms-vscode-remote.remote-ssh](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
  - Remote - SSH: Editing Configuration Files: [ms-vscode-remote.remote-ssh-edit](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh-edit)

Cualquier plugins adicional que ayude al desarrollo previa conversación con el equipo, podemos agregarla a la lista.


## Acceder al contenedor remoto

El desarrollo de aplicaciones es más sencillo si accedes al contenedor, así VSCode podrá ayudarte durante el proceso de desarrollo. Para ello, busca en el lado izquierdo del panel de herramientas de VSCode el `monitor` de acceso remoto (Remote explorer). Si has levantado los contenedores debería aparecer una lista, si no aparece, reinicia vscode.

Una vez veas la lista, busca el contenedor `cforemoto (/cfo_backend)` y has click sobre el icono [attach to container](https://code.visualstudio.com/docs/remote/attach-container#_attach-to-a-docker-container)

En caso de que uses otro editor o simplemente prefieras hacerlo manualmente, te recomendamos considerar las siguientes instrucciones (ejemplo para contenedor Backend):

- `0.0.0.0:7001`: BackEnd - `docker compose exec backend bash -c "source venv && ./manage.py runserver"`
- `0.0.0.0:7002`: BackEnd - `docker compose exec backend bash -c "source venv && ./manage.py shell_plus --notebook"`

Si es la primera vez que haces esto, tendrás que indicarle a VSCode dónde está el intérprete de Python. Para ello te recomendamos seleccionar el intérprete del contenedor en la ruta /opt/venv/bin/python. Además, si VSCode solicita elegir algún _linter_, se recomendamos utilizar __flake8__ (Es el que utilizamos nosotros).


El contenedor __Backend__ tiene por defecto tres configuraciones: 

- Django: Servidor local proporcionado por Django (comando _runserver_)

- Django Notebook: Permite ingresar a la _shell_ de Django desde un cliente de Python Jupiter

- Django Test: Ejecuta la _suite_ de tests de Django.

Todas estas configuraciones se encuentran en el archivo __launch.json__, las cuales pueden ser modificadas a gusto del programador, además de poder añadir alguna nueva que le permite aplicar alguna configuración especial.


Ya con esto tendrás listo tu ambiente de desarrollo en tu editor VSCode. Sin embargo, todo lo relativo al control de versiones con Git te recomendamos gestionarlo desde un terminal independiente, dado que dentro del contenedor no hay configurado ningún acceso a nuestros repositorios remotos.


### Debug mode en VSCode

Accediendo remotamente al contenedor backend con VSCode puedes activar el debug mode.
El proyecto ya tiene [las configuraciones](https://code.visualstudio.com/docs/python/debugging) en el archivo [launch.json](.vscode/launch.json) y puedes obtener más información de como debuggear [aquí](https://code.visualstudio.com/docs/python/debugging#_basic-debugging).


## Acceder a los servicios backend

Además de la configuración de desarrollo, se levantan en los contenedores los servicios principales montados en un ambiente similar al de producción. Para acceder a ellos, se deben utilizar los siguientes puertos:

- `0.0.0.0:7010`: BackEnd   - Django


## Makemigrations, migrate y collectstatic

Normalmente estas acciones se realizan en conjunto, por lo que se ha creado un script que contiene dichas instrucciones y se ejecutan cada vez que se levanta el contenedor con `docker compose up`, sin embargo, también puede ejecutar esta instrucción manualmente (Requiere de una conexióin a la base de datos):
 * `docker compose exec backend django-migrate`

Si prefiere ejecutarlos por separado o necesita aplicar una migración especifica acceda directo al contenedor y ejecute los comandos de `django`.
 * `source venv`
 * `./manage.py migrate`
o puede usar un atajo para ejecutar las instrucciones sin acceder directamente al contenedor:
 * `docker compose exec backend bash -c "source venv && ./manage.py migrate"`

Lo mismo aplica para todos los comandos de `django`.

# Notas

* Este repositorio usa [poetry](https://pypi.org/project/poetry/) para la instalación de sus dependencias.

* Se pueden crear distribución pip siguiendo las instrucciones del siguiente [link](https://randomwalk.in/python/bash/2020/01/19/PoetryPackaging.html)

* Dentro del contenedor existen otros comandos que puede facilitar el trabajo del desarrollo, estos son:

```sh
cmdp -h
```

```sh
-h  | * | --help   muestran los comandos disponibles

-ca | --create-admin            Crea el usuario administrador por defecto de la aplicación
-t  | --translate               Prepara las traducciones en django
-lp | --log-django             Muestra los logs del projecto y uwsgi
```

## Standares
- Para los commits respetamos las siguientes normas: https://chris.beams.io/posts/git-commit/
- Usamos ingles, para los mensajes de commit.
- Se pueden usar tokens como WIP, en el subject de un commit, separando el token con :, por -  ejemplo: WIP: This is a useful commit message
- Para los nombres de ramas también usamos ingles.
- Se asume, que una rama de feature no mezclada, es un feature no terminado.
- El nombre de las ramas va en minúsculas.
- Las palabras se separan con -.
- Las ramas comienzan con alguno de los short lead tokens definidos, por ejemplo: feature/tokens-configuration

## Ramas
feat = Nuevos features
chore = Tareas, que no son visibles al usuario.
bug = Resolución de errores
hotfix = Resolución de errores en producción
