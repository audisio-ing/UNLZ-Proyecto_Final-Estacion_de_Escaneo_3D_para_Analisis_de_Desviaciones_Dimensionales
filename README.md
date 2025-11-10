# UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales
<p align="center" width="100%">
    <img width="100%" src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Scanner_por_triangulacion_laser-ARG/blob/main/fotos/LOGO%20AZUL%20HORIZONTAL%20-%20fondo%20transparente.png">
</p>
En la Universidad Nacional de Lomas de Zamora, nuestra Facultad de Ingeniería se dedica a la formación de profesionales en diversas ramas de la ingeniería. Este repositorio corresponde al proyecto Final de la carrera de Ingeniería Mecatrónica, desarrollado a lo largo del 2025.

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

| CANT. | MODELO                                         | Descripción                                                 | Precio Unitario<br>ARS | Precio Total<br>ARS | Precio total U$D | Proveedor              | Plazo de Entrega |
| ----- | ---------------------------------------------- | ----------------------------------------------------------- | ---------------------- | ------------------- | ---------------- | ---------------------- | ---------------- |
| 2     | MOTOR PASO A PASO - Nema 17                    | Movimiento de la linea                                      | $26,250.00             | $52,500.00          | $40.08           | it&t                   | UNA SEMANA       |
| 2     | CONTROLADOR - A4988                            | Control de Motores                                          | $4,250.00              | $8,500.00           | $6.49            | it&t                   | UNA SEMANA       |
| 1     | SENSOR TOF VL6180X                             | DETECCION DE PIEZA EN CINTA                                 | $8,122.21              | $8,122.21           | $6.20            | UNITELECTRONICS        | UNA SEMANA       |
| 1     | SENSOR EFECTO HALL - S495A                     | Detecion de rotacion de mecanismo                           | $4,000.00              | $4,000.00           | $3.05            | it&t                   | UNA SEMANA       |
| 1     | CAMARA PS3 EYE                                 | SISTEMA DE ESCANEO                                          | $30,000.00             | $30,000.00          | $22.90           | FGSTORE                | UNA SEMANA       |
| 1     | LASER 5V                                       | SISTEMA DE ESCANEO                                          | $2,023.38              | $2,023.38           | $1.54            | ELECTRONICABYP         | UNA SEMANA       |
| 1     | IMAN NEODIIMO 5mm - LOTEx3                     | HOMING DEL SISTEMA DE ESCANEO                               | $1,000.00              | $1,000.00           | $0.76            | it&t                   | UNA SEMANA       |
| 1     | CAPACITOR - 100uF X 50V                        | Regulacion de voltaje de entrada a controladores a4988      | $185.00                | $185.00             | $0.14            | it&t                   | UNA SEMANA       |
| 1     | CAPACITOR 334AEC - 0.33uF x10                  |                                                             | $1,207.00              | $1,207.00           | $0.92            | Nubbeo                 | UNA SEMANA       |
| 1     | CAPACITOR 104 - 0.1uF x10                      |                                                             | $1,207.00              | $1,207.00           | $0.92            | Nubbeo                 | UNA SEMANA       |
| 2     | RESISTENCIA - 10k OHM x 10                     | Circuito electronico                                        | $7,000.00              | $14,000.00          | $10.69           | it&t                   | UNA SEMANA       |
| 1     | BORNERA 3 pines paso 5mm                       |                                                             | $8,159.00              | $8,159.00           | $6.23            | INFORMATICA SAN ISIDRO | UNA SEMANA       |
| 2     | CABLE DUPONT 20cm x40                          | Conexión entre Componentes y Arduino                        | $2,604.00              | $5,208.00           | $3.98            | Duaitek                | UNA SEMANA       |
| 1     | ARDUINO UNO                                    | Manejo de Motores y Cinta Transportadora                    | $8,605.00              | $8,605.00           | $6.57            | TodoMicro              | UNA SEMANA       |
| 1     | FUENTE 12Vx5A                                  | Alimentación de Motores                                     | $12,944.00             | $12,944.00          | $9.88            | Mundo Led              | UNA SEMANA       |
| 1     | PCB PLACA FIBRA PROTOBOARD SIMPLE FAZ 8cmx12cm | Conexion de controladores de motores paso a paso            | $4,106.33              | $4,106.33           | $3.13            | it&t                   | UNA SEMANA       |
| 1     | 1KG PLA 1.75mm                                 | Impresión de Partes                                         | $19,000.00             | $19,000.00          | $14.50           | printALot              | UNA SEMANA       |
| 1     | PERFIL ALUMINIO 2020 tipo bosch R 415mm        | Escaneo                                                     | $4,163.00              | $4,163.00           | $3.18            | ingia                  | UNA SEMANA       |
| 1     | VARILLA ROSCADA 8x1.25 x 1m                    | Transporte de piezas y escaneo                              | $8,000.00              | $8,000.00           | $6.11            | Ingia                  | UNA SEMANA       |
| 1     | CORREA CERRADA GT2 150mm                       | Escaneo                                                     | $6,396.00              | $6,396.00           | $4.88            | ingia                  | UNA SEMANA       |
| 1     | FILM Polietileno 2mx2m                         | Transporte de piezas                                        | $3,222.00              | $3,222.00           | $2.46            | CerroPlast             | UNA SEMANA       |
| 1     | TUBO TERMOFUSION Ø32mmx4m                      | Transporte de piezas                                        | $12,988.00             | $12,988.00          | $9.91            | SanitariosVarela       | UNA SEMANA       |
| 1     | MADERA AGLOMERADA 25x180x1.8Cm                 | Transporte de piezas                                        | $26,000.00             | $26,000.00          | $19.85           | Easy                   | UNA SEMANA       |
| 1     | fibrafacil 80cm x 180cm x 3mm espesor          | Transporte de piezas y Caja                                 | $22,200.00             | $22,200.00          | $16.95           | Easy                   | UNA SEMANA       |
| 3     | PERFIL CUADRADO DE MADERA 2.3cm x 2.3cm x 3m   | Transporte de piezas y Caja                                 | $8,500.00              | $25,500.00          | $19.47           | Easy                   | UNA SEMANA       |
| 9     | RODAMIENTO 22mm                                | Transporte de piezas y escaneo                              | $4,231.00              | $38,079.00          | $29.07           | ingia                  | UNA SEMANA       |
| 19    | TORNILLO M3 x 25mm                             | Cinta Transportadora, Caja de scanneo y Mecanismo Giratorio | $715.99                | $13,603.81          | $10.38           | FORNIS                 | UNA SEMANA       |
| 26    | TORNILLO M3 x 10 mm                            | Cinta Transportadora, Caja de scanneo y Mecanismo Giratorio | $589.22                | $15,319.72          | $11.69           | FORNIS                 | UNA SEMANA       |
| 1     | TORNILO 8x1,25 x25                             |                                                             | $7,068.00              | $7,068.00           | $5.40            | TIENDA DE TORNILLOS    | UNA SEMANA       |
| 19    | TORNILLO AGUJA T2                              |                                                             | $103.04                | $1,957.76           | $1.49            | FORNIS                 | UNA SEMANA       |
| 43    | TUERCA HEXAGONAL M3                            | Cinta Transportadora y Caja de scanneo                      | $155.30                | $6,677.90           | $5.10            | FORNIS                 | UNA SEMANA       |
| 10    | TUERCA AUTOFRENANTE M8x1.25                    | Transporte de piezas y escaneo                              | $396.83                | $3,968.30           | $3.03            | FORNIS                 | UNA SEMANA       |
| 45    | ARANDELA M4                                    | Cinta Transportadora y Caja de scanneo                      | $18.34                 | $825.30             | $0.63            | FORNIS                 | UNA SEMANA       |
| 3     | ARANDELA M8                                    |                                                             | $38.92                 | $116.76             | $0.09            | FORNIS                 | UNA SEMANA       |
| 1     | ARANDELA GROWER M8                             |                                                             | $17.39                 | $17.39              | $0.01            | FORNIS                 | UNA SEMANA       |
| 4     | ESCUADRA ANGULO - 40mm                         |                                                             | $222.00                | $888.00             | $0.68            | ALLSURHERRAJES         | UNA SEMANA       |
|       |                                                |                                                             | TOTAL                  | $377,757.86         | $288.36          |                        |                  |
|       |                                                |                                                             |                        | ARS                 | USD              |                        |                  |
|       |                                                |                                                             |                        | Valor Dolar         | $1,310.00        |                        |                  |

## Esquematicos
A continuación se presentan los esquemáticos y diagramas de diseño que explican cómo se ensamblan y operan los sistemas del proyecto:

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



