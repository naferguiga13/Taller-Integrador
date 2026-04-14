#  Configuración de Servidor: VirtualBox + Ubuntu Server + Webmin + Servidor APRS

![VirtualBox](https://img.shields.io/badge/VirtualBox-Instalado-blue?logo=virtualbox)
![Ubuntu Server](https://img.shields.io/badge/Ubuntu%20Server-24.04%20LTS-orange?logo=ubuntu)
![Webmin](https://img.shields.io/badge/Webmin-Administración-green)
![APRS](https://img.shields.io/badge/APRS-Server-red)



#  1. Creación del Entorno Virtual

##  Máquina virtual

* Nombre: `Ubuntu Server`
* Tipo: Linux
* Versión: Ubuntu (64-bit)

##  Recursos

| Recurso | Valor                |
| ------- | -------------------- |
| RAM     | 2 GB mínimo          |
| CPU     | 2 núcleos            |
| Disco   | 20 GB (VDI dinámico) |

---

##  2. Configuración de Red

```bash
NAT ❌ → Adaptador puente (Bridge Adapter) ✅
```

✔️ Permite acceso desde el host y conexión con otros dispositivos (como el iGate)

---

#  3. Instalación de Ubuntu Server

Durante la instalación:

* Idioma y teclado
* Red automática (DHCP)
* Uso completo del disco
* Creación de usuario

###  Activar SSH

```bash
Install OpenSSH server
```

---

##  4. Verificar IP del servidor

```bash
ip a
```

Ejemplo:

```bash
192.168.0.33
```

---

#  5. Instalación de Webmin

##  Actualizar sistema

```bash
sudo apt update
sudo apt upgrade -y
```

##  Dependencias

```bash
sudo apt install -y wget apt-transport-https software-properties-common
```

##  Descargar e instalar

```bash
wget https://www.webmin.com/download/deb/webmin-current.deb
sudo apt install -y ./webmin-current.deb
```

Si hay errores:

```bash
sudo apt --fix-broken install -y
```

##  Abrir puerto

```bash
sudo ufw allow 10000
```

##  Acceso

```
https://IP_DEL_SERVIDOR:10000
```

---

#  6. Instalación de APRS (aprsc)

##  Requisitos Previos

* Ubuntu Server funcionando
* Webmin instalado
* Conexión a internet
* Usuario con sudo

---

##  1. Actualizar e instalar dependencias

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential libc6-dev libssl-dev zlib1g-dev git libevent-dev
```

---

##  2. Clonar repositorio

```bash
cd ~
git clone https://github.com/hessu/aprsc.git
cd aprsc/src
```

---

##  3. Corregir compatibilidad con GCC

```bash
nano hlog.c
```

Buscar:

```c
pthread_setname_np(name);
```

Reemplazar por:

```c
pthread_setname_np(pthread_self(), name);
```

---

##  4. Compilar e instalar

```bash
./configure
make
sudo make install
```

 Instalación en:

```
/opt/aprsc/
```

---

##  5. Crear usuario y directorios

```bash
sudo useradd -r -s /bin/false aprsc
sudo mkdir -p /opt/aprsc/logs
sudo mkdir -p /opt/aprsc/data
sudo chown -R aprsc:aprsc /opt/aprsc
sudo chmod 644 /opt/aprsc/etc/aprsc.conf
```

---

#  7. Configuración de aprsc

##  Editar configuración

```bash
sudo nano /opt/aprsc/etc/aprsc.conf
```

### Configuración:

```conf
ServerId        TI3TEC-10
PassCode        -1

MyAdmin         "Equipo10, TEC"
MyEmail         tucorreo@estudiantec.cr

RunDir          /opt/aprsc/data

Listen "Full feed"              fullfeed  tcp  ::  10152
Listen "Client-Defined Filters" igate     tcp  ::  14580
Listen "UDP submit"             udpsubmit udp  ::  8080

HTTPStatus 0.0.0.0 14501
```

 Eliminar:

```
MagicBadness 42.7
```

---

#  8. Configuración como servicio (systemd)

##  Crear servicio

```bash
sudo nano /etc/systemd/system/aprsc.service
```

### Contenido:

```ini
[Unit]
Description=aprsc APRS-IS Server
After=network.target

[Service]
Type=simple
ExecStart=/opt/aprsc/sbin/aprsc -u aprsc -c /opt/aprsc/etc/aprsc.conf -r /opt/aprsc/logs
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

##  Activar servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable aprsc
sudo systemctl start aprsc
```

---

#  9. Verificación

##  Estado del servicio

```bash
sudo systemctl status aprsc
```

---

##  Puertos activos

```bash
ss -tlnp | grep -E "10152|14580"
```

---

##  Monitoreo HTTP

```
http://IP_DEL_SERVIDOR:14501/status.json
```

---

##  Logs en tiempo real

```bash
sudo journalctl -f -u aprsc
```

---
# 10. Instalación y Configuración de trackdirect

## Instalación Paso a Paso

### 1. Clonar el repositorio de trackdirect

```bash
cd ~
git clone https://github.com/qvarforth/trackdirect.git
cd trackdirect
```

### 2. Instalar PostgreSQL

```bash
sudo apt install -y postgresql postgresql-client-common postgresql-client
```

### 3. Instalar otras dependencias del sistema

```bash
sudo apt install -y sudo git libpq-dev libevent-dev libmagickwand-dev imagemagick inkscape
```

### 4. Instalar Python3 y paquetes requeridos

```bash
sudo apt install -y python3 python3-dev python3-pip python-is-python3 python3-full python3-psycopg2 python3-setuptools python3-autobahn python3-twisted python3-jsmin python3-psutil
```

### 5. Instalar PHP y paquetes requeridos

```bash
sudo apt install -y php libapache2-mod-php php-dom php-pgsql php-imagick php-dev php-pear php-gd
```

### 6. Instalar librería APRS de Python

```bash
cd /opt
sudo git clone https://github.com/rossengeorgiev/aprs-python
cd aprs-python
sudo python3 setup.py install
```

### 7. Instalar la función heatmap

Descargar y descomprimir:

```bash
cd /opt
sudo wget http://jjguy.com/heatmap/heatmap-2.2.1.tar.gz
sudo tar xzf heatmap-2.2.1.tar.gz
cd heatmap-2.2.1
```

Corregir error de compatibilidad con Python3 en `setup.py`:

```bash
sudo nano setup.py
```

Buscar la línea:
```python
print 'On Windows, skipping build_ext.'
```
Cambiarla por:
```python
print('On Windows, skipping build_ext.')
```

Corregir error en `__init__.py`:

```bash
sudo nano /usr/local/lib/python3.12/dist-packages/heatmap/__init__.py
```

Buscar la línea:
```python
except Exception, e:
```
Cambiarla por:
```python
except Exception as e:
```

Instalar:

```bash
sudo python3 setup.py install
```

---

## Configuración

### 1. Copiar trackdirect a /opt

```bash
cd ~
sudo cp -r trackdirect /opt/trackdirect
```

### 2. Configurar la base de datos PostgreSQL

Crear usuario y base de datos:

```bash
sudo -u postgres psql -c "CREATE USER trackdirect WITH PASSWORD 'trackdirect';"
sudo -u postgres psql -c "CREATE DATABASE trackdirect OWNER trackdirect;"
```

Crear las tablas:

```bash
cd /opt/trackdirect/server/scripts
sudo -u postgres ./db_setup.sh trackdirect 5432 /opt/trackdirect/misc/database/tables/
```

### 3. Configurar Apache

Crear directorios y copiar archivos:

```bash
sudo mkdir -p /var/www/trackdirect/config
sudo cp -r /opt/trackdirect/htdocs /var/www/trackdirect
sudo cp /opt/trackdirect/config/trackdirect.ini /var/www/trackdirect/config
```

Asignar permisos:

```bash
sudo chmod 777 /var/www/trackdirect/htdocs/public/symbols
sudo chmod 777 /var/www/trackdirect/htdocs/public/heatmaps
sudo chown -R www-data:www-data /var/www
```

Editar la configuración de Apache:

```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

Reemplazar el contenido por:

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/trackdirect/htdocs/public
    ErrorLog ${APACHE_LOG_DIR}/aprs-error.log
    CustomLog ${APACHE_LOG_DIR}/aprs-access.log combined
    <Directory "/var/www/trackdirect/htdocs/public">
        Options Indexes MultiViews SymLinksIfOwnerMatch
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

Activar módulo rewrite y reiniciar Apache:

```bash
sudo a2enmod rewrite
sudo service apache2 restart
```

### 4. Editar el archivo de configuración de trackdirect

```bash
sudo nano /var/www/trackdirect/config/trackdirect.ini
```

Modificar los siguientes parámetros:

**Sección `[website]`:**
```ini
title="APRS Track Direct"
owner_name="Equipo10"
owner_email="tucorreo@estudiantec.cr"
```

**Sección `[database]`:**
```ini
host="127.0.0.1"
database="trackdirect"
username="trackdirect"
password="trackdirect"
port="5432"
```

**Sección de conexión con aprsc:**
```ini
aprs_host1="127.0.0.1"
aprs_port1="14580"
aprs_source_id1="1"
```

---

##  Iniciar los Servicios de trackdirect

### Manualmente

```bash
cd ~/trackdirect/server/scripts
bash wsserver.sh trackdirect.ini &
bash collector.sh trackdirect.ini 0 &
bash remover.sh trackdirect.ini &
```

### Automáticamente con crontab

```bash
crontab -e
```

Agregar al final del archivo:

```
* * * * * ~/trackdirect/server/scripts/wsserver.sh trackdirect.ini 2>&1 &
* * * * * ~/trackdirect/server/scripts/collector.sh trackdirect.ini 0 2>&1 &
* * * * * ~/trackdirect/server/scripts/remover.sh trackdirect.ini 2>&1 &
*/30 * * * * ~/trackdirect/server/scripts/ogn_devices_install.sh trackdirect 5432 2>&1 &
```

---

## Verificación

### Acceder al mapa

Abrir en el navegador:
```
http://192.168.0.23
```

Debe aparecer el mapa de Costa Rica con el título "Maintained by Equipo10".

### Verificar paquetes recibidos

```bash
sudo -u postgres psql -d trackdirect -c "SELECT COUNT(*) FROM packet;"
```

### Buscar un tracker específico

```
http://192.168.0.23/?call=TI0TEC1-7
```

---



