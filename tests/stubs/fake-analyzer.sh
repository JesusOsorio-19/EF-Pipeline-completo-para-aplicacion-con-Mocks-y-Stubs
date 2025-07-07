#!/bin/bash

# Stub para simular /usr/bin/external-analyzer 
# Acepta parametros y devuelve diferentes códigos de salida

if [ $# -eq 0 ]: then
    echo "Error: No se proporcionaron archivos de datos." >&2
    exit 1
fi

DATA_FILE="$1"

# Simula diferentes escenarios basados en el nombre del archivo
case "$DATA_FILE" in
    *"error"*)
        echo "Error de análisis" >&2
        exit 1
        ;;
    *"system_error"*)
        echo "Error del sistema" >&2
        exit 2
        ;;
    *"valid"*)
        echo "Análisis exitoso"
        exit 0
        ;;
    *)
        echo "Análisis completado" >&2    
        exit 0  
        ;;  
esac

