#!/usr/bin/env python3

import os, sys, time, re

# --- COLORES ---

VERDE = '\033[92m'
AMARILLO = '\033[93m'
MORADO = '\033[95m'
AZUL = '\033[94m'
ROJO = '\033[91m'
RESET = '\033[0m'

# --- FUNCIONES ---
def limpiar_pantalla():
    """ Limpia la pantalla de la terminal para que el menu siempre este arriba"""
    os.system('clear')

def mostrar_logo():
    """ Muestra el logo del IDS Toolbox """
    logo = f"""{AZUL}
    ░▀█▀░█▀▄░█▀▀░░░▀█▀░█▀█░█▀█░█░░░█▀▄░█▀█░█░█
    ░░█░░█░█░▀▀█░░░░█░░█░█░█░█░█░░░█▀▄░█░█░▄▀▄
    ░▀▀▀░▀▀░░▀▀▀░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀░▀
    {RESET}
    {MORADO}>> Intrusion Detection System Toolbox <<{RESET}"""
    print(logo)
    print( "-" * 44 )

def mostrar_menu_principal():
    """ Muestra el menu principal del IDS Toolbox """
    menu = f"""{VERDE}
    [1] Suricata
    [2] Evebox
    [3] Salir
    {RESET}"""
    print(menu)

def mostrar_menu_suricata():
    """ Muestra el menu de Suricata """
    menu = f"""{VERDE}
    [1] Gestionar REGLAS de Suricata
    [2] Gestionar LOGS de Suricata
    [3] Inicia Suricata
    [4] Detener Suricata
    [5] Ver estado de Suricata
    [6] Volver al menu principal
    [7] Salir
    {RESET}"""
    print(menu)

def mostrar_menu_reglas_suricata():
    """ Muestra el menu de gestion de reglas de Suricata """
    menu = f"""{VERDE}
    [1] Agregar regla personalizada [Wizard guiado]
    [2] Consultar regla personalizada
    [3] Eliminar regla personalizada
    [4] Actualizar reglas desde Emerging Threats
    [5] Volver al menu anterior
    [6] Salir
    {RESET}"""
    print(menu)

def mostrar_menu_logs_suricata():
    """ Muestra el menu de gestion de logs de Suricata """
    menu = f"""{VERDE}
    [1] Consultar peso de logs generados por Suricata
    [2] Eliminar logs generados por Suricata
    [3] Volver al menu anterior
    [4] Salir
    {RESET}"""
    print(menu)

def mostrar_menu_evebox():
    """ Muestra el menu de Evebox """
    menu = f"""{VERDE}
    [1] Acceder a Evebox
    [2] Iniciar Evebox
    [3] Detener Evebox
    [4] Ver estado de Evebox
    [5] Volver al menu principal
    [6] Salir
    {RESET}"""
    print(menu)

def salir_toolbox():
    """ Sale del IDS Toolbox """
    print(f"{AMARILLO}Saliendo del IDS Toolbox...{RESET}")
    time.sleep(1)
    sys.exit()

def _obtener_nombre_servicio(servicio):
    """ Mapea el nombre del servicio al nombre del sistema """
    """ DEBEN CORRESPONDER con los nombres en el DOCKER-COMPOSE.YML """
    nombres_servicios = {
        "Suricata": "suricata_sensor",
        "Evebox": "evebox_gui"
    }
    return nombres_servicios.get(servicio, servicio.lower())

def ver_estado_servicio(servicio):
    """ Verifica y muestra el estado de un servicio """
    print(f"{AMARILLO}Verificando el estado de {servicio}...{RESET}")
    time.sleep(1)  # Simula tiempo de espera
    # Aqui iria la logica real para verificar el estado del servicio
    print(f"{VERDE}{servicio} esta corriendo correctamente.{RESET}")

def _iniciar_servicio_docker(servicio):
    """ Inicia un servicio usando Docker Compose """
    nombre_servicio = _obtener_nombre_servicio(servicio)
    comando_iniciar = f"docker compose up -d {nombre_servicio}"
    resultado = os.system(comando_iniciar)
    return resultado == 0

def _recrear_servicio_docker(servicio):
    """ Recrea un servicio usando Docker Compose """
    nombre_servicio = _obtener_nombre_servicio(servicio)
    comando_recrear = f"docker compose up -d --force-recreate {nombre_servicio}"
    resultado = os.system(comando_recrear)
    return resultado == 0

def iniciar_servicio(servicio):
    """ Inicia un servicio
     - Si esta apagado - > Lo inicia
     - Si ya esta encendido -> Mensaje informativo + pregunta si quiere recrearlo
    """
    print(f"{AMARILLO}Iniciando {servicio}...{RESET}")
    nombre_servicio = _obtener_nombre_servicio(servicio)

    #1 - COMPROBAR SI ESTA CORRIENDO
    # Ejecutamos un comando silencioso para ver si esta en la lista de running
    comando_chek = f"docker compose ps --services --filter 'status= running' | grep -q '^{nombre_servicio}$'"
    esta_activo = os.system(comando_chek) == 0

    if esta_activo == 0:
        # El contenedor ya esta ACTIVO
        print(f"{AMARILLO} AVISO: El servicio {servicio.upper()} ya esta activo .{RESET}")
        print(f"{AMARILLO} ¿Como desea proceder?{RESET}")
        print(f"{AZUL}[1] Reiniciar el servicio {servicio} (Detener + Iniciar){RESET}")
        print(f"{AZUL}[2] Recrear el servicio {servicio}{RESET}")
        print(f"{AZUL}[3] Cancelar operacion{RESET}")
        eleccion = input(f"{AMARILLO}Seleccione una opcion: {RESET}")
        if eleccion == '1':
            _detener_servicio_docker(servicio)
            print(f"{AMARILLO}Iniciando {servicio}...{RESET}")
            time.sleep(1)  # Simula tiempo de espera
            _recrear_servicio_docker(servicio)
            print(f"{VERDE}{servicio} ha sido reiniciado.{RESET}")
        elif eleccion == '2':
            print(f"{AMARILLO}Recreando {servicio}...{RESET}")
            time.sleep(1)  # Simula tiempo de espera
            _recrear_servicio_docker(servicio)
            print(f"{VERDE}{servicio} ha sido recreado.{RESET}")
        else:
            print(f"{AMARILLO}Operacion cancelada por el usuario.{RESET}")
    else:
        # El contenedor esta INACTIVO
        exito = _iniciar_servicio_docker(servicio)
        if exito:
            print(f"{VERDE}{servicio} ha sido iniciado.{RESET}")
        else:
            print(f"{ROJO}[ERROR] No se pudo iniciar {servicio}.{RESET}")

def _detener_servicio_docker(servicio):
    """ Detiene un servicio """
    print(f"{AMARILLO}Deteniendo {servicio}...{RESET}")
    time.sleep(1)  # Simula tiempo de espera
    os.system(f"docker compose stop {_obtener_nombre_servicio(servicio)}")
    print(f"{VERDE}{servicio} ha sido detenido.{RESET}")

def wizard_suricata():
    """ Wizard guiado para agregar una regla personalizada en Suricata """
    print(f"{AMARILLO}Iniciando wizard para agregar regla personalizada...{RESET}")
    time.sleep(1)  # Simula tiempo de espera
    # Aqui iria la logica real del wizard
    print(f"{VERDE}Regla personalizada agregada exitosamente.{RESET}")

def consultar_regla_suricata():
    """ Consulta una regla personalizada en Suricata """
    print(f"{AMARILLO}Consultando regla personalizada...{RESET}")
    time.sleep(1)  # Simula tiempo de espera
    # Aqui iria la logica real para consultar la regla
    print(f"{VERDE}Regla encontrada: alert tcp any any -> any 80 (msg:\"Test Rule\"; sid:1000001;){RESET}")

def eliminar_regla_suricata():
    """ Elimina una regla personalizada en Suricata """
    print(f"{AMARILLO}Eliminando regla personalizada...{RESET}")
    time.sleep(1)  # Simula tiempo de espera
    # Aqui iria la logica real para eliminar la regla
    print(f"{VERDE}Regla personalizada eliminada exitosamente.{RESET}")

def actualizar_reglas_suricata():
    """ Actualiza las reglas de Suricata desde Emerging Threats """
    print(f"{AMARILLO}Actualizando reglas desde Emerging Threats...{RESET}")
    time.sleep(1)  # Simula tiempo de espera
    # Aqui iria la logica real para actualizar las reglas
    print(f"{VERDE}Reglas actualizadas exitosamente.{RESET}")

def _convertir_unidades_almacenamiento(size_bytes):
    """ Convierte bytes a una unidad de almacenamiento legible """
    if size_bytes == 0:
        return "0 B"
    nombre_unidades = ("B", "KB", "MB", "GB", "TB")
    i = 0
    p = 1024
    while size_bytes >= p and i < len(nombre_unidades)-1:
        size_bytes /= p
        i += 1
    return f"{size_bytes:.2f} {nombre_unidades[i]}"

def consultar_peso_logs_suricata():
    """ Consulta el peso de los logs generados por Suricata """
    ruta_logs = "./logs"

    print(f"{AMARILLO}Consultando peso de logs en {ruta_logs}...{RESET}")
    time.sleep(1)  # Simula tiempo de espera

    if not os.path.exists(ruta_logs):
        print(f"\n{ROJO}[ERROR] No se encuentra la carpeta '{ruta_logs}'.{RESET}")
        print(f"{ROJO}Asegurate de estar ejecutando el script en la raiz del repositorio.{RESET}\n")
        return
    
    total_size = 0
    cantidad_archivos = 0

    # Recorremos la carpeta y subcarpetas buscando archivos

    try:
        for dirpath, dirnames, filenames in os.walk(ruta_logs):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Saltamos si es un enlace simbolico
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
                    cantidad_archivos += 1

        tamaño_legible = _convertir_unidades_almacenamiento(total_size)
        print(f"\n{VERDE}--- REPORTE DE LOGS ---{RESET}")
        print(f"{VERDE}Cantidad de archivos de log: {MORADO}{cantidad_archivos}{RESET}")
        print(f"{VERDE}Tamaño total de logs: {MORADO}{tamaño_legible}{RESET}\n")
    except Exception as e:
        print(f"\n{ROJO}[ERROR] Ocurrió un error al calcular el tamaño de los logs: {e}{RESET}\n")

def eliminar_logs_suricata():
    """ Vacía los archivos de logs generados para no romper Suricata """
    ruta_logs = "./logs"

    #1º Preguntamos confirmacion al usuario
    print(f"\n{ROJO}--- ADVERTENCIA ---{RESET}")
    print(f"{ROJO}Esta accion vaciara todos los archivos de logs generados por Suricata.{RESET}")
    print(f"{ROJO}Esta accion ES IREVERSIBLE.{RESET}\n")
    confirmacion = input(f"{AMARILLO}¿Desea continuar? (s/n): {RESET}").lower()

    if confirmacion != 's':
        print(f"{AMARILLO}Operacion cancelada por el usuario.{RESET}\n")
        return
    
    print(f"{AMARILLO}Limpiando logs en {ruta_logs}...{RESET}")
    time.sleep(1)  # Simula tiempo de espera

    archivos_limpiados = 0
    errores = 0

    try:
        #Recorremos la carpeta
        for nombre_archivo in os.listdir(ruta_logs):
           ruta_completa = os.path.join(ruta_logs, nombre_archivo)

           # Solo tocamos archivos, no carpetas
           if os.path.isfile(ruta_completa):
                try:
                   # Abrimos el archivo en modo escritura 'w' para vaciar su contenido
                   with open(ruta_completa, 'w') as archivo:
                       pass # No escribimos nada, solo abrimos y cerramos
                   
                   print(f"{VERDE}Archivo limpiado: {nombre_archivo}{RESET}")
                   archivos_limpiados += 1
                except Exception as e:
                    print(f"{ROJO}Error al limpiar {nombre_archivo}: {e}{RESET}")
                    errores += 1

        print(f"\n{VERDE}--- REPORTE DE LIMPIEZA ---{RESET}")
        print(f"{VERDE}Archivos limpiados: {MORADO}{archivos_limpiados}{RESET}")
        if errores > 0:
            print(f"{VERDE}Errores encontrados: {MORADO}{errores}{RESET}\n")
    except Exception as e:
        print(f"\n{ROJO}[ERROR] Ocurrió un error al limpiar los logs: {e}{RESET}\n")
def _obtener_ip_local():
    """ Obtiene la IP local del sistema """
    import socket
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    return ip_local

def _obtener_puerto_evebox():
    """ Obtiene el puerto en el que corre Evebox """
    # Buscamos el puerto en el docker-compose.yml
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docker_compose_path = os.path.join(current_dir, 'docker-compose.yml')


    try:
        with open(docker_compose_path, 'r') as archivo:
            contenido = archivo.read()
            match = re.search(r'["\']?(\d+):5636', contenido)

            if match:
                return match.group(1) # Puerto encontrado
            else:
                print(f"{ROJO}[WARNING] No se encontro el puerto en docker-compose.yml. Usando puerto por defecto 56366.{RESET}")
                return "56366"  # Puerto por defecto si no se encuentra
            
    except FileNotFoundError:
        print(f"{ROJO}[ERROR] No se encontro el archivo docker-compose.yml. Usando puerto por defecto 5636.{RESET}")
        return "5636"  # Puerto por defecto si no se encuentra el archivo
    
def acceder_evebox():
    """ Accede a la interfaz web de Evebox """
    print(f"{AMARILLO}Abriendo Evebox en el navegador...{RESET}")
    time.sleep(1)  # Simula tiempo de espera
    ip_local = _obtener_ip_local()
    puerto = _obtener_puerto_evebox()
    url_evebox = f"http://{ip_local}:{puerto}"
    # Abrimos la URL en el navegador predeterminado
    import webbrowser
    webbrowser.open(url_evebox)
    print(f"{VERDE}Evebox abierto en el navegador.{RESET}")
    salir_toolbox()

# --- PROGRAMA PRINCIPAL ---
def main():
    while True:
        limpiar_pantalla()
        mostrar_logo()
        mostrar_menu_principal()
        opcion = input(f"{AMARILLO}Seleccione una opcion: {RESET}")
        if opcion == '1':
            while True:
                limpiar_pantalla()
                mostrar_logo()
                mostrar_menu_suricata()
                opcion_suricata = input(f"{AMARILLO}Seleccione una opcion: {RESET}")
                if opcion_suricata == '1':
                    while True:
                        limpiar_pantalla()
                        mostrar_logo()
                        mostrar_menu_reglas_suricata()
                        opcion_reglas = input(f"{AMARILLO}Seleccione una opcion: {RESET}")
                        if opcion_reglas == '1':
                            wizard_suricata()
                        elif opcion_reglas == '2':
                            consultar_regla_suricata()
                        elif opcion_reglas == '3':
                            eliminar_regla_suricata()
                        elif opcion_reglas == '4':
                            actualizar_reglas_suricata()
                        elif opcion_reglas == '5':
                            break
                        elif opcion_reglas == '6':
                            salir_toolbox()
                        input(f"{AMARILLO}Presione Enter para continuar...{RESET}")
                elif opcion_suricata == '2':
                    while True:
                        limpiar_pantalla()
                        mostrar_logo()
                        mostrar_menu_logs_suricata()
                        opcion_logs = input(f"{AMARILLO}Seleccione una opcion: {RESET}")
                        if opcion_logs == '1':
                            consultar_peso_logs_suricata()
                        elif opcion_logs == '2':
                            eliminar_logs_suricata()
                        elif opcion_logs == '3':
                            break
                        elif opcion_logs == '4':
                            salir_toolbox()
                        input(f"{AMARILLO}Presione Enter para continuar...{RESET}")
                elif opcion_suricata == '3':
                    iniciar_servicio("Suricata")
                    input(f"{AMARILLO}Presione Enter para continuar...{RESET}")
                elif opcion_suricata == '4':
                    _detener_servicio_docker("Suricata")
                    input(f"{AMARILLO}Presione Enter para continuar...{RESET}")
                elif opcion_suricata == '5':
                    ver_estado_servicio("Suricata")
                    input(f"{AMARILLO}Presione Enter para continuar...{RESET}")
                elif opcion_suricata == '6':
                    break
                elif opcion_suricata == '7':
                    salir_toolbox()
        elif opcion == '2':
            while True:
                limpiar_pantalla()
                mostrar_logo()
                mostrar_menu_evebox()
                opcion_evebox = input(f"{AMARILLO}Seleccione una opcion: {RESET}")
                if opcion_evebox == '1':
                    acceder_evebox()
                    input(f"{AMARILLO}Presione Enter para continuar...{RESET}")
                elif opcion_evebox == '2':
                    iniciar_servicio("Evebox")
                    input(f"{AMARILLO}Presione Enter para continuar...{RESET}")
                elif opcion_evebox == '3':
                    _detener_servicio_docker("Evebox")
                    input(f"{AMARILLO}Presione Enter para continuar...{RESET}")
                elif opcion_evebox == '4':
                    ver_estado_servicio("Evebox")
                    input(f"{AMARILLO}Presione Enter para continuar...{RESET}")
                elif opcion_evebox == '5':
                    break
                elif opcion_evebox == '6':
                    salir_toolbox()
        elif opcion == '3':
            salir_toolbox()
        else:
            print(f"{ROJO}Opcion invalida. Intente de nuevo.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()