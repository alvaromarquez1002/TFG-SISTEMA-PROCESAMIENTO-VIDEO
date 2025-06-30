# Configuración del Despliegue de Jitsi Meet

Este directorio contiene los archivos que representan el estado final de la configuración de la infraestructura de Jitsi Meet para este TFG.

## Repositorio Base

El despliegue se basa en el proyecto oficial `docker-jitsi-meet`.
- **Enlace al repositorio original:** [https://github.com/jitsi/docker-jitsi-meet](https://github.com/jitsi/docker-jitsi-meet)

## Descripción de Archivos

* `env.example`: Plantilla de la configuración final y funcional. Utiliza un dominio público y está configurado para obtener un certificado SSL válido de Let's Encrypt. Activa todos los servicios necesarios, incluyendo el acceso para invitados, la grabación (Jibri) y el servidor TURN.

* `docker-compose.yml`: Versión del fichero de composición que incluye la definición del servicio `turn` y los volúmenes necesarios para compartir los certificados SSL con dicho servicio.

* `jibri.yml`: Versión del fichero de Jibri que incluye la directiva `privileged: true`, necesaria para solucionar problemas de renderizado de vídeo en entornos Docker.

* `gen-passwords.sh`: Script original del proyecto para generar las contraseñas de los servicios.