#  Planificación e Investigación del Proyecto
##  Objetivos Específicos

- Diseñar e implementar la arquitectura de un servidor basado en APRS Trackdirect, capaz de recibir y procesar paquetes provenientes de la red APRS-IS y de los módulos tracker del proyecto.

- Configurar y administrar un entorno de servidor seguro que permita el almacenamiento estructurado y la visualización en tiempo real de los datos de geolocalización recibidos.

- Validar la correcta integración del servidor con los dispositivos del sistema, garantizando la recepción, registro y visualización continua de los datos durante la etapa de pruebas y evaluación.
## APRS

### ¿Qué es?

El Automatic Packet Reporting System (APRS) es un sistema de comunicación digital diseñado para radioaficionados que permite transmitir en tiempo real información como posición geográfica, mensajes cortos, telemetría y datos meteorológicos. Fue desarrollado por Bob Bruninga (WB4APR) como una aplicación del protocolo AX.25 sobre radio VHF (Bruninga, 2023; ARRL, 2022).

APRS integra estaciones móviles, repetidoras digitales (digipeaters) y pasarelas a Internet (iGates), conformando una red híbrida de radio e infraestructura IP.


### ¿Para qué sirve? (Aplicaciones)

- Seguimiento de estaciones móviles en tiempo real.  
- Transmisión de telemetría (variables técnicas y ambientales).  
- Mensajería digital entre radioaficionados.  
- Reportes meteorológicos automáticos.  
- Comunicaciones de apoyo en situaciones de emergencia (ARRL, 2022).  


### ¿Qué protocolos de comunicación utiliza?

APRS emplea principalmente:

- AX.25 (protocolo de enlace de datos para radioaficionados).  
- AFSK a 1200 baudios en VHF.  
- Encapsulamiento sobre IP cuando opera mediante la red APRS-IS (Bruninga, 2023).  

### ¿En cuáles bandas de frecuencia opera?

En la Región 2 de la Unión Internacional de Telecomunicaciones (América), APRS opera típicamente en:

- 144.390 MHz dentro de la banda 144–148 MHz del Servicio de Radioaficionados (UIT, 2020).

En Costa Rica, la operación debe ajustarse al Plan Nacional de Atribución de Frecuencias (MICITT, 2023).


### Componentes clave de una red APRS

- Transceptor VHF/UHF  
- TNC (Terminal Node Controller)  
- Receptor GPS  
- Digipeaters  
- iGates  
- Servidores APRS-IS  


# Legislación Costarricense

## Cuadro Nacional de Atribución de Frecuencias (PNAF)

El uso del espectro radioeléctrico en Costa Rica está regulado por el Decreto Ejecutivo N° 44010-MICITT, publicado en el Alcance N° 99 a La Gaceta N° 95 del 30 de mayo de 2023.

Este decreto:

- Actualiza el Plan Nacional de Atribución de Frecuencias.  
- Define la atribución primaria o secundaria de cada banda.  
- Establece condiciones técnicas generales de operación.  
- Armoniza el cuadro nacional con el Reglamento de Radiocomunicaciones de la UIT (MICITT, 2023).  


## Permisos requeridos para operar un sistema LoRa/APRS

### Para APRS (Servicio de Radioaficionados)

- Licencia de radioaficionado vigente.  
- Indicativo oficialmente asignado.  
- Cumplimiento de límites de potencia y clase de emisión.  

### Para LoRa (banda ISM 902–928 MHz)

- Cumplimiento de normativa técnica para dispositivos de corto alcance.  
- Respeto de límites de Potencia Isotrópica Radiada Equivalente (PIRE).  

### Trámites generales

1. Presentación de solicitud formal ante la autoridad competente.  
2. Evaluación técnica.  
3. Pago de derechos administrativos (según aplique).  
4. Emisión de resolución y autorización correspondiente.  

Tiempo estimado:
- Revisión documental: 1–2 semanas.  
- Evaluación técnica: 2–4 semanas.  
- Resolución final: variable según carga administrativa.  


## Clases de Emisión (Modulación)

Las clases de emisión describen el tipo de modulación y la naturaleza de la señal transmitida (UIT, 2020).

- F2D: Frecuencia modulada con transmisión de datos digitales (APRS tradicional).  
- Chirp Spread Spectrum (CSS): Modulación utilizada en sistemas LoRa.  


## Bandas de Frecuencia en Costa Rica para LoRa/APRS

Según el PNAF (MICITT, 2023):

- 144–148 MHz → Servicio de Radioaficionados (APRS VHF).  
- 902–928 MHz → Banda ISM para aplicaciones LoRa de baja potencia.  

La operación debe ajustarse a la atribución oficial y condiciones técnicas vigentes.


## PIRE permitida

- Servicio de Radioaficionados (144–148 MHz): límites definidos por reglamentación nacional.  
- Banda ISM 902–928 MHz: límites específicos para dispositivos de corto alcance establecidos por normativa técnica nacional.  

Los valores exactos deben verificarse en la regulación vigente emitida por la autoridad competente (MICITT, 2023; UIT, 2020).

#Diagrama de Gantt
## 📊 Diagrama de Gantt – Servidor APRS (16 Semanas)

```
Semanas → 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16
--------------------------------------------------------

Investigación APRS-IS        | . █ █ . . . . . . . . . . . . .
Investigación Legislación    | . █ █ . . . . . . . . . . . . .
Diseño Arquitectura          | . . █ █ . . . . . . . . . . . .
Diseño Base de Datos         | . . . █ █ . . . . . . . . . . .
Config. Entorno Servidor     | . . . █ █ █ . . . . . . . . . .
Instalación Trackdirect      | . . . . █ █ █ . . . . . . . . .
Desarrollo Scripts           | . . . . . █ █ █ . . . . . . . .
Entrega Informe Parcial      | . . . . . . . █ . . . . . . . .

Implementación APRS-IS       | . . . . . . . . █ █ . . . . . .
Visualización en Mapa        | . . . . . . . . . █ █ █ . . . .
Pruebas con Trackers         | . . . . . . . . . █ █ █ █ █ . .
Optimización y Seguridad     | . . . . . . . . . . . █ █ █ . .
Pruebas Finales              | . . . . . . . . . . . . . █ █ .
Informe Final                | . . . . . . . . . . . . . . █ █
Presentación Final           | . . . . . . . . . . . . . . █ █
Defensa Proyecto             | . . . . . . . . . . . . . . . █
```
# Bibliografía

ARRL. (2022). APRS Overview and Operating Guide. American Radio Relay League.  

Bruninga, B. (2023). APRS Protocol Reference.  

Ministerio de Ciencia, Innovación, Tecnología y Telecomunicaciones (MICITT). (2023). Decreto Ejecutivo N° 44010-MICITT: Plan Nacional de Atribución de Frecuencias. Alcance N° 99 a La Gaceta N° 95, 30 de mayo de 2023.  

Unión Internacional de Telecomunicaciones (UIT). (2020). Reglamento de Radiocomunicaciones.
