#!/usr/bin/env bash

function generatePassword() {
    openssl rand -hex 16
}

JICOFO_AUTH_PASSWORD=$(generatePassword)
JVB_AUTH_PASSWORD=$(generatePassword)
JIGASI_XMPP_PASSWORD=$(generatePassword)
JIBRI_RECORDER_PASSWORD=$(generatePassword)
JIBRI_XMPP_PASSWORD=$(generatePassword)
JIGASI_TRANSCRIBER_PASSWORD=$(generatePassword)

echo "################################################################################"
echo "Las contraseñas generadas son (copia y pega estas en tu archivo .env):"
echo "################################################################################"
echo "JICOFO_AUTH_PASSWORD=${JICOFO_AUTH_PASSWORD}"
echo "JVB_AUTH_PASSWORD=${JVB_AUTH_PASSWORD}"
echo "JIGASI_XMPP_PASSWORD=${JIGASI_XMPP_PASSWORD}"
echo "JIBRI_RECORDER_PASSWORD=${JIBRI_RECORDER_PASSWORD}"
echo "JIBRI_XMPP_PASSWORD=${JIBRI_XMPP_PASSWORD}"
echo "JIGASI_TRANSCRIBER_PASSWORD=${JIGASI_TRANSCRIBER_PASSWORD}"
echo "################################################################################"

