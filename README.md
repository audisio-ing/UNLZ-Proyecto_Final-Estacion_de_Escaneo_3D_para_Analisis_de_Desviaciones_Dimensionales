<h2 align="center" style="font-size: 3em;">F.IU.N.L.Z. Proyecto Final</h2>
<h1 align="center" style="font-size: 3em;">Estacion de Escaneo 3D para Análisis de Desviaciones Dimensionales</h1>

<p align="center" width="100%">
    <img width="100%" src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Scanner_por_triangulacion_laser-ARG/blob/main/fotos/LOGO%20AZUL%20HORIZONTAL%20-%20fondo%20transparente.png">
</p>
Este repositorio corresponde al proyecto Final de la carrera de Ingeniería Mecatrónica, desarrollado a lo largo del 2025 en la Universidad Nacional de Lomas de Zamora, nuestra Facultad de Ingeniería.

# Integrantes
<p>👤 <a href="https://github.com/audisio-ing">Juan Pablo Audisio</a></p>
<p>👤 <a href="https://github.com/IngGarrahan">Alan Garrahan</a></p>
<p>👤 <a href="https://github.com/ValentinReyna">Valentín Julián Reyna</a></p>

El objetivo de este proyecto es buscar una solucion innovadora para el control de calidad, un nuevo enfoque que permita un control detallado pieza por pieza asegurándose de que el producto final cumpla con los estándares requeridos. Garantizar la precisión, consistencia y velocidad en la detección de defectos y variaciones en las piezas.
## Indice

## Descripción

Este proyecto se basa en una línea de control integral equipada con un scanner 3D funcionando con el principio de triangulación láser, con el fin de detección de fallas en procesos productivos con matrices destinadas a producciones en serie. Todo unido a traves de una cinta transportadora y software de control.

Las piezas ingresarán al sistema a través de una cinta transportadora hasta ser frenada por un sensor TOF que la detecta. Una vez en posicion comienza el escaneo. Cuando finaliza obtendremos una nube de puntos representativa de las dimensiones del objeto, a partir de la cual se realizarán comparaciones con el modelo patrón de la misma a fin de determinar posibles fallas y deformaciones en la misma causadas por la matriz, que puedan afectar su funcionamiento.

## Instrucciones de uso
Para utilizar este proyecto, sigue estos pasos:

Paso 1: Descripción del primer paso para poner en marcha el proyecto.

Paso 2: Descripción del segundo paso, etc.

Paso X: Cualquier otro paso relevante que se deba seguir.

## Tecnologías utilizadas

Este proyecto fue desarrollado utilizando una variedad de tecnologías, incluyendo:

**Robótica:**

-Arduino Uno

-Motores paso a paso Nema 17

-Engranajes y poleas

-Laser de barra

**Electrónica:**

-Controladores A4988 de motores paso a paso

-Sensor TOF 

-Sensor Efecto Hall

-Regulador Integrado de voltaje 5v

-Resistencias

-Capacitores

**Programación:**

-Python y Arduino

**Plataformas:** [ROS (Robot Operating System), OpenCV, TensorFlow, etc.]

**Inteligencia Artificial:** [Redes neuronales, visión computacional, algoritmos de machine learning, etc.]

## Listado de componentes

| CANT. | MODELO                                         | DESCRIPCIÓN                                                  |
| ----- | ---------------------------------------------- | ------------------------------------------------------------ |
| 2     | MOTOR PASO A PASO - Nema 17                    | MOVIMIENTO DE LA LINEA                                       |
| 2     | CONTROLADOR - A4988                            | CONTROL DE MOTORES                                           |
| 1     | SENSOR TOF VL6180X                             | DETECCION DE PIEZA EN CINTA                                  |
| 1     | SENSOR EFECTO HALL - S495A                     | DETECCIÓN DE ROTACIÓN DE MECANISMOS                          |
| 1     | CAMARA PS3 EYE                                 | SISTEMA DE ESCANEO                                           |
| 1     | LASER 5V - HLM1230                             | SISTEMA DE ESCANEO                                           |
| 1     | IMAN NEODIIMO 5mm - LOTEx3                     | HOMING DEL SISTEMA DE ESCANEO                                |
| 1     | CAPACITOR - 100uFx50V                          | REGULACIÓN DE VOLTAJE DE ENTRADA A CONTROLADORES A4988       |
| 1     | REGULADOR DE TENSION 5Vx1A - 7805              | REGULACIÓN DE VOLTAJE EN DIVISION DE TENSIÓN                 |
| 1     | CAPACITOR 334AEC - 0.33uF x10                  | REGULACIÓN DE VOLTAJE EN DIVISION DE TENSIÓN                 |
| 1     | CAPACITOR 104 - 0.1uF x10                      | REGULACIÓN DE VOLTAJE EN DIVISION DE TENSIÓN                 |
| 2     | RESISTENCIA - 10k OHM x10                      | CIRCUITO ELÉCTRICO                                           |
| 1     | BORNERA DE 3 PINES PASO 5mm                    | CIRCUITO ELÉCTRICO                                           |
| 2     | CABLE DUPONT 20cm x40                          | CONEXIÓN ENTRE COMPONENTES Y ARDUINO                         |
| 1     | ARDUINO UNO                                    | MANEJO DE MOTORES Y CINTA TRANSPORTADORA                     |
| 1     | FUENTE 12Vx5A                                  | ALIMENTACIÓN DE MOTORES                                      |
| 1     | PCB PLACA FIBRA PROTOBOARD SIMPLE FAZ 8cmx12cm | CIRCUITO ELÉCTRICO                                           |
| 1     | 1KG PLA 1.75mm                                 | IMPRESIÓN DE PARTES                                          |
| 1     | PERFIL ALUMINIO 2020 TIPO BOSCH R 415mm        | ESCANEO                                                      |
| 1     | VARILLA ROSCADA 8x1.25 x1m                     | TRANSPORTE DE PIEZAS Y CAJA Y ESCANEO                        |
| 1     | CORREA CERRADA GT2 150mm                       | ESCANEO                                                      |
| 1     | FILM POLIETILENO 2mx2m                         | TRANSPORTE DE PIEZAS                                         |
| 1     | TUBO TERMOFUSION Ø32mmx4m                      | TRANSPORTE DE PIEZAS                                         |
| 1     | MADERA AGLOMERADA 25x180x1.8Cm                 | TRANSPORTE DE PIEZAS                                         |
| 1     | FIBRAFACIL 80cm x 180cm x 3mm espesor          | TRANSPORTE DE PIEZAS Y CAJA                                  |
| 3     | PERFIL CUADRADO DE MADERA 2.3cm x 2.3cm x 3m   | TRANSPORTE DE PIEZAS Y CAJA                                  |
| 9     | RODAMIENTO 22mm                                | TRANSPORTE DE PIEZAS Y ESCANEO                               |
| 19    | TORNILLO M3 x 25mm                             | CINTA TRANSPORTADORA Y CAJA DE SCANNEO Y MECANISMO GIRATORIO |
| 26    | TORNILLO M3 x 10 mm                            | CINTA TRANSPORTADORA Y CAJA DE SCANNEO Y MECANISMO GIRATORIO |
| 1     | TORNILO 8x1,25 x25                             | CINTA TRANSPORTADORA Y CAJA DE SCANNEO                       |
| 19    | TORNILLO AGUJA T2                              | CINTA TRANSPORTADORA Y CAJA DE SCANNEO                       |
| 43    | TUERCA HEXAGONAL M3                            | CINTA TRANSPORTADORA Y CAJA DE SCANNEO                       |
| 10    | TUERCA AUTOFRENANTE M8x1.25                    | CINTA TRANSPORTADORA Y CAJA DE SCANNEO                       |
| 45    | ARANDELA M4                                    | CINTA TRANSPORTADORA Y CAJA DE SCANNEO                       |
| 3     | ARANDELA M8                                    | CINTA TRANSPORTADORA Y CAJA DE SCANNEO                       |
| 1     | ARANDELA GROWER M8                             | CINTA TRANSPORTADORA Y CAJA DE SCANNEO                       |
| 4     | ESCUADRA ANGULO x 40mm                         | CINTA TRANSPORTADORA Y CAJA DE SCANNEO                       |

## Esquematicos
A continuación se presentan los esquemáticos y diagramas de diseño que explican cómo se ensamblan y operan los sistemas del proyecto:
<img width="13244" height="9355" alt="Image" src="https://github.com/user-attachments/assets/6662ea1c-b2b9-45bd-9ced-6135f363e980" />
<img width="6616" height="4677" alt="Image" src="https://github.com/user-attachments/assets/e3c31136-6ab0-4f31-bc53-0533ac6cd761" />
<img width="13244" height="9355" alt="Image" src="https://github.com/user-attachments/assets/705479f7-7092-40ff-b4d8-b58947d4625a" />

## Fotos / videos
Fotos de detalle del modelo completo:

<img width="1186" height="757" alt="Image" src="https://github.com/user-attachments/assets/71f6aba0-a154-4566-917d-9b140b0019e3" />
<img width="1076" height="349" alt="Image" src="https://github.com/user-attachments/assets/d32559f7-db63-44ba-8a2f-0f309882cbad" />
<img width="1351" height="733" alt="Image" src="https://github.com/user-attachments/assets/282896cd-11f0-4a30-b808-303dae3bc109" />
<img width="1075" height="642" alt="Image" src="https://github.com/user-attachments/assets/e76e9b4c-4a2d-4bfe-8e72-5bbad9504a32" />
<img width="686" height="509" alt="Image" src="https://github.com/user-attachments/assets/d8d6b97d-05f1-4d76-9329-75389ea69314" />
<img width="1021" height="690" alt="Image" src="https://github.com/user-attachments/assets/1efcddf9-8e2e-47e9-899d-4249d0af6158" />
<img width="985" height="623" alt="Image" src="https://github.com/user-attachments/assets/f61ff91f-1e12-4905-afd6-db76f77e392e" />

## Autor
Este proyecto fue realizado por Audisio Juan Pablo, Garrahan Alan, y Reyna Valentin como parte de la carrera de Ingeniería Mecatrónica en la Facultad de Ingeniería de la Universidad Nacional de Lomas de Zamora.

## Carpetas del Proyecto

A continuación se detallan las carpetas que estructuran este repositorio:

CODIGO: Contiene el código fuente utilizado en este proyecto.

MULTIMEDIA: Imágenes y videos del desarrollo y funcionamiento del proyecto.

PLANOS: Esquemáticos y diagramas de los sistemas implementados.

DATASHEET: Hojas de datos y especificaciones de los componentes utilizados.

INFORMES: Archivos relacionados con la planificación y documentación del proyecto, como Gantt, informes en PDF, cronogramas, manuales, etc.



