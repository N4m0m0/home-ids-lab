<div align="center">

<img alt="Instalacion y configuracion de Suricata IDS + Evebox" src="https://github.com/user-attachments/assets/efcbe915-1779-4cfa-b390-69c8b00d953a" width="500" />



🛡️ Home IDS Lab: Detección de Intrusiones Automatizada

Un sistema de detección de intrusiones (IDS) contenerizado, basado en Suricata y Evebox, con gestión de reglas automatizada mediante Python (Infrastructure as Code).
</div>
📋 Resumen del Proyecto

Este repositorio contiene la infraestructura necesaria para desplegar un IDS completo en cuestión de minutos. El objetivo es monitorear el tráfico de una red doméstica/laboratorio mediante Port Mirroring, analizarlo con Suricata y visualizar alertas en Evebox.

A diferencia de una instalación manual estándar, este proyecto implementa IaC (Infraestructura como Código):

  - Despliegue: Todo encapsulado en Docker Compose.

  - Gestión: Script de Python (ids-toolbox.py) para gestionar reglas y supresiones desde un archivo YAML limpio, evitando la edición manual de archivos de configuración complejos.

🏗️ Arquitectura

El sistema está diseñado para funcionar en un servidor con dos interfaces de red (Gestión + Sniffing).
Fragmento de código

graph TD
    Internet((Internet)) --> Router
    Router --> Switch
    Switch -- Port Mirroring --> Server[Servidor IDS]
    
    subgraph "Docker Host"
        Server --> NIC1[Int. Gestión]
        Server --> NIC2[Int. Escucha]
        NIC2 --> |Tráfico RAW| Suricata[🐳 Suricata]
        Suricata --> |JSON Logs| Evebox[🐳 Evebox]
        Evebox --> |HTTP| Dashboard[🖥️ Dashboard Web]
    end

✨ Características Principales

-   Despliegue Rápido: docker compose up y listo.

-   Persistencia: Logs y configuraciones separados en volúmenes.

-   Gestión de Falsos Positivos: Sistema propio mediante rules_db.yaml para suprimir alertas ruidosas sin tocar los archivos .config de Suricata.

-   Auto-Reload: El script de operaciones recarga las reglas en caliente sin detener el servicio.

🚀 Instalación y Despliegue

Requisitos Previos

  - Linux Server (Ubuntu/Debian recomendado).

  - Docker y Docker Compose.

  - Una interfaz de red dedicada a la escucha (Promiscuous mode/Port Mirroring).

1. Clonar el repositorio
Bash

  git clone https://github.com/N4m0m0/home-ids-lab-public.git
  cd home-ids-lab-public

2. Configurar el entorno

Crea el archivo .env basado en el ejemplo y define tu interfaz de escucha (la que recibe el tráfico espejo):
Bash

cp .env.example .env
nano .env
# Cambiar: SURICATA_INTERFACE=eth1 (o tu interfaz real)

3. Descargar reglas iniciales
Bash

  # Primer arranque para generar carpetas
  docker compose up -d
  # Descargar reglas de Emerging Threats
  docker exec -it suricata_sensor suricata-update

⚙️ Uso y Gestión (Workflow)
Añadir Supresiones (Ignorar alertas)

En lugar de editar archivos complejos, edita rules_db.yaml:
YAML

categories:
  - name: "Falsos Positivos Spotify"
    rules:
      - sid: 2013056
        target: 192.168.1.55
        track: by_src
        description: "Ignorar tráfico UDP ruidoso de Spotify en móvil"

Luego, aplica los cambios y recarga Suricata automáticamente:
Bash

python3 IDS-ToolBox.py
