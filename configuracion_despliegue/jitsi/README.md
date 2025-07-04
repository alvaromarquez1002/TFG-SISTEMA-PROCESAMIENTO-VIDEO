# Configuración de Despliegue para Jitsi Meet

Esta carpeta contiene los archivos de configuración clave, validados y utilizados para el despliegue del sistema de captura de vídeo de este TFG. La configuración se basa en el proyecto oficial **[docker-jitsi-meet](https://github.com/jitsi/docker-jitsi-meet)**.

Este despliegue actúa como la fuente de datos para el proyecto principal **[TFG: Sistema de Procesamiento de Vídeo Distribuido](https://github.com/alvaromarquez1002/TFG-SISTEMA-PROCESAMIENTO-VIDEO)**.

## Descripción de Ficheros

A continuación se detalla el propósito de cada fichero en este directorio:

* **`docker-compose.yml`**:
    * Es el fichero principal de orquestación del proyecto `docker-jitsi-meet`. Define los servicios esenciales para una conferencia funcional: `webapp` (la interfaz web), `prosody` (servidor de autenticación XMPP), `jicofo` (gestión de las conferencias) y `jvb` (Jitsi Videobridge, el enrutador de vídeo).

* **`jibri.yml`**:
    * Es un fichero de Docker Compose adicional y complementario. Su función es añadir el servicio `jibri` (Jitsi Broadcasting Recording Infrastructure) a la pila de contenedores. Jibri es el componente que actúa como un participante "invisible" en una conferencia para poder grabarla y guardarla como un archivo `.mp4`.

* **`env.example`**:
    * Este es el fichero de plantilla más importante para la configuración. Debe ser copiado a un nuevo fichero llamado `.env` (que será ignorado por Git) antes de iniciar el despliegugue. Contiene todas las variables de entorno necesarias para personalizar la instancia, entre las que destacan:
        * `PUBLIC_URL`: El dominio público que apuntará a tu instancia de Jitsi.
        * `LETSENCRYPT_EMAIL`: Tu correo electrónico para la generación de certificados SSL con Let's Encrypt.
        * `ENABLE_LETSENCRYPT=1`: La variable que activa la generación automática de certificados SSL.
        * `JIBRI_XMPP_PASSWORD` y `JIBRI_RECORDER_PASSWORD`: Las contraseñas para los usuarios internos de Jibri.

* **`gen-passwords.sh`**:
    * Es un script de utilidad proporcionado por el proyecto `docker-jitsi-meet`. Su función es generar automáticamente todas las contraseñas internas que los servicios de Jitsi necesitan para comunicarse entre sí y las añade al fichero `.env`. Si no se añaden automaticamente el usuario debe copiar y pegarlas manualmente.

* **`.gitkeep`**:
    * Es un fichero vacío que se utiliza como una convención para asegurar que Git versiona este directorio aunque estuviera vacío.

## Resumen del Proceso de Despliegue

Aunque la guía completa con todos los prerrequisitos (configuración de red, módulos del kernel, etc.) se encuentra en el `README.md` principal del proyecto y en el manual, a continuación se resumen los pasos clave para desplegar Jitsi utilizando esta configuración:

1.  **Clonar el Repositorio Oficial:** Primero, se clona el repositorio de `docker-jitsi-meet`.
    ```bash
    git clone [https://github.com/jitsi/docker-jitsi-meet.git](https://github.com/jitsi/docker-jitsi-meet.git)
    cd docker-jitsi-meet
    ```

2.  **Copiar Ficheros de Configuración:** Se copian los ficheros de este directorio a la raíz del repositorio recién clonado.

3.  **Crear Directorios Persistentes:** Se crea la estructura de directorios en `~/.jitsi-meet-cfg/` donde se guardarán los datos y configuraciones persistentes.

4.  **Configurar el Entorno:** Se crea el fichero `.env` a partir de la plantilla `env.example` y se rellenan las variables necesarias.

5.  **Generar Contraseñas:** Se ejecuta el script `./gen-passwords.sh`.

6.  **Levantar los Servicios:** Finalmente, se inicia la pila completa, lo que levanta la infraestructura que permite que se realice la meet.

Para un desglose detallado de todos los pasos y requisitos, por favor, consulta la documentación principal de este TFG.