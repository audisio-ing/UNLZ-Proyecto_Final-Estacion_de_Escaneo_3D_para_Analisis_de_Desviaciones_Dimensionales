<h2 align="center">F.I.U.N.L.Z. Proyecto Final</h2>
<h1 align="center" style="font-size: 3em;">Estacion de Escaneo 3D para Análisis de Desviaciones Dimensionales</h1>

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Animaciones/Paneo.gif" alt="Demostración" width="100%"/>
  <br>
  <em>Render del prototipo</em>
</p>

# Integrantes
<p>👤 <a href="https://github.com/audisio-ing">Juan Pablo Audisio</a></p>
<p>👤 <a href="https://github.com/IngGarrahan">Alan Garrahan</a></p>
<p>👤 <a href="https://github.com/ValentinReyna">Valentín Julián Reyna</a></p>

# Indice
- **1.0** [Introducción](#introducción)
- **2.0** [Descripción del Sistema](#descripción-del-sistema)
- **3.0** [Tecnologías y Recursos](#tecnologías-y-recursos)
    - **3.1** [Software y Programación](#software-y-programación)
    - **3.2** [Librerias de Python](#librerias-de-python)
    - **3.3** [Hardware y Electrónica](#hardware-y-electrónica)
- **4.0** [Listado de Componentes](#listado-de-componentes)
- **5.0** [Diseños y Esquemáticos](#diseños-y-esquemáticos)
- **6.0** [Interfaz de Usuario y Funcionamiento](#interfaz-de-usuario-y-funcionamiento)
    - **6.1** [Setup Cámara](#setup-cámara)
    - **6.2** [Escaneo](#escaneo)
    - **6.3** [Comparación](#comparación)
- **7.0** [Escaneos Obtenidos](#escaneos-obtenidos)
- **8.0** [Algoritmo de Comparación](#algoritmo-de-comparación)
- **9.0** [Errores Cometidos y Lecciones Aprendidas](#errores-cometidos-y-lecciones-aprendidas)
- **10.0** [Futuras Mejoras y Propuestas](#futuras-mejoras-y-propuestas)
- **11.0** [Galería del Proyecto](#galería-del-proyecto)
- **12.0** [Estructura del Repositorio](#estructura-del-repositorio)

<h1 align="center">Introducción</h1>

Este repositorio corresponde al Proyecto Final de la carrera de Ingeniería Mecatrónica, desarrollado a lo largo del 2025 en la Universidad Nacional de Lomas de Zamora, Facultad de Ingeniería.

El objetivo principal es buscar una solución innovadora para el control de calidad. Proponemos un nuevo enfoque que permite un control detallado, pieza por pieza. Esto asegura que el producto final cumpla con los estándares requeridos. El sistema garantiza precisión, consistencia y velocidad en la detección de defectos y variaciones causadas por las matrices de producción.

<p align="center">
  <img src="https://github.com/user-attachments/assets/71f6aba0-a154-4566-917d-9b140b0019e3" alt="Vista General" width="800"/>
  <br>
  <em>Vista general de la estación de escaneo</em>
</p>

<h1 align="center">Descripción del Sistema</h1>

Este proyecto consiste en una línea de control integral. Está equipada con un scanner 3D que funciona bajo el principio de triangulación láser. Su fin es la detección de fallas en procesos productivos con matrices destinadas a producciones en serie. Todo el sistema está unido a través de una cinta transportadora y un software de control central.

### Funcionamiento del Proceso

1.  **Ingreso:** Las piezas ingresan al sistema a través de la cinta transportadora.
2.  **Detección:** Un sensor TOF detecta la pieza y la centra en el escáner.
3.  **Escaneo:** Una vez en posición, comienza el proceso de escaneo.
4.  **Procesamiento:** Se obtiene una nube de puntos representativa de las dimensiones del objeto.
5.  **Análisis:** Se realizan comparaciones con el modelo patrón para determinar fallas o deformaciones.

<h1 align="center">Tecnologías y Recursos</h1>

A continuación se detalla en listas las diferentes tecnologías y recursos utilizados para llevar a cabo el proyecto.

## Software y Programación

| Tecnología | Descripción |
| :--- | :--- |
| **Python** | Lenguaje principal utilizado para visión computacional, procesamiento y visualización de datos. |
| **Arduino IDE** | Utilizado para la programación del microcontrolador que maneja los motores y sensores físicos. |
| **Autodesk Fusion 360** | Diseño de componentes mecánicos y piezas a escanear. |
| **OBS Studio** | Utilizado como intermediario, permite ajustar controles de la cámara no posibles en python. |
| **CL-Eye Test** | Software utilizado para la conexión con la Cámara y drivers específicos. |
| **Blender** | Renders del prototipo utilizados para visualización. |

## Librerias de Python

| Librería | Descripción |
| :--- | :--- |
| **OpenCV** | Manejo de Cámara, captura de frames y detección del Láser |
| **NumPy** | Procesamiento matemático de matrices y la nube de puntos |
| **Pillow** | Procesamiento y manipulación básica de imágenes |
| **PyVista** | Visualización 3D interactiva y renderizado de la nube de puntos |
| **SciPy** | Algoritmos científicos para cálculos complejos y filtrado |
| **PySerial** | Comunicación serial para el control del Arduino |
| **PyInstaller** | Empaquetado del programa en un archivo ejecutable |
| **Tkinter** | Diseño de interfaz visual de usuario (GUI) |


## Hardware y Electrónica

| Componente | Uso en el proyecto |
| :--- | :--- |
| **Arduino Uno** | Cerebro del control físico (motores y sensores). |
| **Cámara PS3 Eye** | Cámara utilizada para el escaneo y triangulación. |
| **Motor Stepper Nema 17** | Motores paso a paso para el movimiento de la cinta y el escáner. |
| **Driver A4988** | Controladores para el manejo preciso de los motores paso a paso. |
| **Láser de Barra** | Fuente de luz para realizar la triangulación sobre la pieza. |
| **Sensor TOF** | Sensor de tiempo de vuelo para realizar el centrado de la pieza sobre la cinta. |
| **Sensor de efecto Hall** | Utilizado para realizar el homing del escáner. |

<h1 align="center">Listado de Componentes</h1>

A continuación se detalla el BOM (Bill of Materials) del proyecto:

| CANT. | MODELO | DESCRIPCIÓN |
| :--- | :--- | :--- |
| 2 | MOTOR PASO A PASO - Nema 17 | MOVIMIENTO DE LA LINEA |
| 2 | CONTROLADOR - A4988 | CONTROL DE MOTORES |
| 1 | SENSOR TOF VL6180X | DETECCIÓN DE PIEZA EN CINTA |
| 1 | SENSOR EFECTO HALL - S495A | DETECCIÓN DE ROTACIÓN DE MECANISMOS |
| 1 | CAMARA PS3 EYE | SISTEMA DE ESCANEO |
| 1 | LASER 5V - HLM1230 | SISTEMA DE ESCANEO |
| 1 | IMAN NEODIMIO 5mm - LOTEx3 | HOMING DEL SISTEMA DE ESCANEO |
| 1 | CAPACITOR - 100uFx50V | REGULACIÓN DE VOLTAJE (A4988) |
| 1 | REGULADOR 5Vx1A - 7805 | REGULACIÓN DE VOLTAJE |
| 1 | ARDUINO UNO | MANEJO DE MOTORES Y CINTA |
| 1 | FUENTE 12Vx5A | ALIMENTACIÓN DE MOTORES |
| 1 | PERFIL ALUMINIO 2020 | ESTRUCTURA DE ESCANEO |
| 1 | VARILLA ROSCADA 8x1.25 | TRANSPORTE Y ESCANEO |
| - | VARIOS (Tornillos, Tuercas, Maderas) | ESTRUCTURA Y ENSAMBLAJE |

<h1 align="center">Diseños y Esquemáticos</h1>

Se presentan los esquemáticos y planos de vista explosionada de los diferentes mecanismos que componen al prototipo

<p align="center">
  <img src="https://github.com/user-attachments/assets/6662ea1c-b2b9-45bd-9ced-6135f363e980" alt="Plano 1" width="800"/>
  <br>
  <em>Vista explosionada del mecanismo del Escáner</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e3c31136-6ab0-4f31-bc53-0533ac6cd761" alt="Circuito" width="800"/>
  <br>
  <em>Vista explosionada de la Caja Contenedora</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/705479f7-7092-40ff-b4d8-b58947d4625a" alt="Plano 2" width="800"/>
  <br>
  <em>Vista explosionada del mecanismo de la Cinta Transportadora</em>
</p>

<h1 align="center">Interfaz de Usuario y Funcionamiento</h1>

Para utilizar el prototipo es necesario ejecutar el software dedicado, este guiará al usuario a traves del proceso mediante una interfaz de usuario, dando información relevante del estado actual y posibles errores.
La misma se divide en 3 etapas principales:

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Menu.png" alt="Menu GUI" width="800"/>
  <br>
  <em>Menu Inicial de la GUI</em>
</p>

# Etapas:

## Setup Cámara
Previo a realizar un escaneo es necesario ejecutar el Setup de la cámara, este nos permitirá seleccionar el índice de cámara dentro de la PC, el valor de treshold para la detección del láser y el puerto <b>COM</b> del Arduino

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Setup%20Cámara.png" alt="GUI Setup Cámara" width="500"/>
  <br>
  <em>GUI Setup Cámara</em>
</p>

## Escaneo
Una vez configurado los parámetros iniciales se procede a la segunda etapa, el escaneo. Se abrirá una ventana nueva con 2 opciones: <b>"Comenzar escaneo"</b> y un engranaje que nos llevará a la configuración, permitiendonos seleccionar el número de muestras a tomar (50 por defecto).


<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Escaneo.png" alt="GUI Escaneo" width="45%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Configuración%20Escaneo.png" alt="GUI Configuración Escaneo" width="45%"/>
  <br>
  <em>GUI Escaneo y Configuración de muestras</em>
</p>

Al presionar el botón <b>"Comenzar escaneo"</b> Python informará a Arduino el inicio de la secuencia, durante el proceso de escaneo el usuario observará una barra de estado indicando la etapa actual del escaneo junto con una transmisión en vivo de la cámara.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Setup%20Cámara.png" alt="GUI Previa al escaneo" width="500"/>
  <br>
  <em>GUI Previa al escaneo</em>
</p>

Cuando la pieza se encuentre en posición y comience el escaneo, aparecerá una barra de carga que indicará la muestra actual, muestras restantes y un tiempo estimado de finalización.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Setup%20Cámara.png" alt="GUI Durante el escaneo" width="500"/>
  <br>
  <em>GUI Durante el escaneo</em>
</p>

Una vez finalizado el escaneo y habiendo expulsado la pieza, la interfaz cambiará haciendo saber al usuario que el escaneo ha finalizado y mostrando una ventana que le permitirá visualizar la nube de puntos obtenida.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Escaneo.png" alt="GUI Escaneo Finalizado" width="45%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Configuración%20Escaneo.png" alt="GUI Nube de puntos obtenida" width="45%"/>
  <br>
  <em>GUI Escaneo finalizado y nube de puntos obtenida</em>
</p>

## Comparación
   
Ahora que ya obtuvimos una nube de puntos a escala de la pieza, procedemos a la tercera etapa, ejecutar el programa de comparación. Al iniciar nos encontraremos con una interfaz muy similar al programa de escaneo, un botón de Comparación y un icono de engranaje para realizar configuraciones.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Comparación.png" alt="GUI Comparación" width="45%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Configuración%20Comparación.png" alt="GUI Configuración Comparación" width="45%"/>
  <br>
  <em>GUI Comparación y configuración</em>
</p>

Previo a realizar la comparación es necesario dirigirse a la pestaña de ajustes, donde el usuario deberá seleccionar la ruta de destino de los 3 escaneos que usará como patrones en la comparación, y tambien ingresar un porcentaje de similitud mínimo que indicará si la pieza es aceptada o rechazada.

Ahora sí procedemos con la comparación, 

<h1 align="center">Escaneos Obtenidos</h1>

A continuación se muestran los resultados obtenidos del escaneo de las diferentes piezas planteadas, todos los escaneos fueron realizados con 100 muestras.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/A.gif" alt="Escaneo A" width="30%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/B.gif" alt="Escaneo B" width="30%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/B.gif" alt="Escaneo C" width="30%"/>
</p>
<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/Patron%20A.gif" alt="Patrón A" width="30%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/Patron%20B.gif" alt="Patrón B" width="30%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/Patron%20C.gif" alt="Patrón C" width="30%"/>
</p>
<p align="center">
  <em>Resultados visuales del proceso de escaneo y análisis</em>
</p>

<h1 align="center">Algoritmo de Comparación</h1>

Para lograr una comparación

<h1 align="center">Errores Cometidos y Lecciones Aprendidas</h1>

A la hora de realizar el proyecto, nos encontramos con varias problematicas, las cuales pasaremos a desarrollar a continuacion, incluyendo la manera que encontramos para solucionarlos.

En primer lugar: la cinta transoprtadora o, mejor dicho, el centrado de la pieza. Tuvimos varios problemas, primero, de qué material hacer la cinta. Empezamos utilizando un film, pero nos encontramos con el problema de que la pieza patinaba y al sensor funcionar contando al cantida de pasos que daba el motor para centrar la pieza, no la dejaba en el lugar correcto. Debido a esto, decidimos ponerle un material con mucha fricción a la base de las piezas. Esto no quitó del todo el problema, por lo cual tambien le sumamos el utilziar el motor en 1/16 de paso, para que el movimiento fuera más continuo, sin perder velocidad, dado que veniamos queriendo que la cinta avnzara una gran cantidad de pasos para que no tomara mucho tiempo.
Una vez resuelto este tema, la cinta seguia sin quedar del todo centrada, por lo cual pasamos a analizar qué le pasaba a la cinta mientras avanza, con lo cual pduimos detectar que se iba hacia un lado, moviendo a su paso a la pieza. Esto nos llevó a acomodar los clindros qeu sostienen la cinta para que aueden lo más paralelas posibles, para que asi avance derecha la cinta. Esto solo se logro con prueba y error, debido a la precariedad del la construcción de la cinta, dada la limitada accesibilidad a mejores herramientas y materiales. A su vez, se cambió el material de la cinta por ule y se cortó de manera que quedara lo más regular posible. Finalmente, para asegurar por completo el centrado de la pieza, se diseñ´un centrador que ca montado sobre los porta rdamientos, el cual s u vez esta hecho de maenra que indica en que setndo debe ir la pieza.




<h1 align="center">Futuras Mejoras y Propuestas</h1>

cinta: , sin embargo, si la estructura de la cinta hubiera sido m{as rigida y hubeiramos podido asegrar una mejor paralelidad entre los cilindros, esot no hubeira sido un problema.

<h1 align="center">Galería del Proyecto</h1>

Imágenes detalladas del prototipo y sus componentes en funcionamiento.

<p align="center">
  <img src="https://github.com/user-attachments/assets/d32559f7-db63-44ba-8a2f-0f309882cbad" width="45%"/>
  <img src="https://github.com/user-attachments/assets/282896cd-11f0-4a30-b808-303dae3bc109" width="45%"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/e76e9b4c-4a2d-4bfe-8e72-5bbad9504a32" width="45%"/>
  <img src="https://github.com/user-attachments/assets/d8d6b97d-05f1-4d76-9329-75389ea69314" width="45%"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/1efcddf9-8e2e-47e9-899d-4249d0af6158" width="45%"/>
  <img src="https://github.com/user-attachments/assets/f61ff91f-1e12-4905-afd6-db76f77e392e" width="45%"/>
</p>

<h1 align="center">Estructura del Repositorio</h1>

A continuación se detallan las carpetas que estructuran este repositorio:

* **CODIGO:** Contiene el código fuente utilizado (Python/Arduino).
* **MULTIMEDIA:** Imágenes y videos del desarrollo y funcionamiento.
* **PLANOS:** Esquemáticos y diagramas de los sistemas implementados.
* **DATASHEET:** Hojas de datos y especificaciones de componentes.
* **INFORMES:** Documentación, Gantt, informes PDF y manuales.

---
<p align="center">
  <em><b>Proyecto realizado por Audisio Juan Pablo, Garrahan Alan y Reyna Valentin.</b>b></em>
  <br>
  <em>Ingeniería Mecatrónica</em>
  <br>
  <em>Facultad de Ingeniería - Universidad Nacional de Lomas de Zamora.</em>
</p>
