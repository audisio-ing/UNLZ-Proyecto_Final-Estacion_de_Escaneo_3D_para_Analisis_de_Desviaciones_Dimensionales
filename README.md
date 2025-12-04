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
  - **2.1** [Diagrama de Bloques](#diagrama-de-bloques)
  - **2.2** [Secuencia de Escaneo](#secuencia-de-escaneo)
- **3.0** [Marco Teórico](#marco-teórico)
  - **3.1** [Sensor ToF](#sensor-time-of-flight)
  - **3.2** [Sensor Efeto Hall](#sensor-efecto-hall)
  - **3.3** [Motor Paso a Paso](#motor-paso-a-paso)
- **4.0** [Escaneo 3D](#escaneo-3d)
   - **4.1** [Triangulación Laser](#triangulación-laser)
   - **4.1** [Nube de Puntos](#nube-de-puntos)
- **5.0** [Tecnologías y Recursos](#tecnologías-y-recursos)
    - **5.1** [Software y Programación](#software-y-programación)
    - **5.2** [Librerias de Python](#librerias-de-python)
    - **5.3** [Hardware y Electrónica](#hardware-y-electrónica)
- **6.0** [Listado de Componentes](#listado-de-componentes)
- **7.0** [Diseños y Esquemáticos](#diseños-y-esquemáticos)
  - **7.1** [Diseño Mecánico](#diseño-mecánico)
  - **7.2** [Diseño Electrónico](#diseño-electrónico) 
- **8.0** [Interfaz de Usuario y Funcionamiento](#interfaz-de-usuario-y-funcionamiento)
    - **8.1** [Setup Cámara](#setup-cámara)
    - **8.2** [Escaneo](#escaneo)
    - **8.3** [Comparación](#comparación)
- **9.0** [Escaneos Obtenidos](#escaneos-obtenidos)
- **10.0** [Algoritmo de Comparación](#algoritmo-de-comparación)
- **11.0** [Errores Cometidos y Lecciones Aprendidas](#errores-cometidos-y-lecciones-aprendidas)
- **12.0** [Futuras Mejoras y Propuestas](#futuras-mejoras-y-propuestas)
- **13.0** [Galería del Proyecto](#galería-del-proyecto)

<br>
<h1 align="center">Introducción</h1>

Este repositorio corresponde al Proyecto Final de la carrera de Ingeniería Mecatrónica, desarrollado a lo largo del 2025 en la Universidad Nacional de Lomas de Zamora, Facultad de Ingeniería.

El objetivo principal es buscar una solución innovadora para el control de calidad. Proponemos un nuevo enfoque que permite un control detallado, pieza por pieza. Esto asegura que el producto final cumpla con los estándares requeridos. El sistema garantiza precisión, consistencia y velocidad en la detección de defectos y variaciones causadas por las matrices de producción.

<p align="center">
  <img src="https://github.com/user-attachments/assets/71f6aba0-a154-4566-917d-9b140b0019e3" alt="Vista General" width="800"/>
  <br>
  <em>Vista general de la estación de escaneo</em>
</p>

<br>
<h1 align="center">Descripción del Sistema</h1>

Este proyecto consiste en una línea de control integral. Está equipada con un scanner 3D que funciona bajo el principio de triangulación láser. Su fin es la detección de fallas en procesos productivos con matrices destinadas a producciones en serie. Todo el sistema está unido a través de una cinta transportadora y un software de control central.

### Diagrama de Bloques

A continuación se presenta un diagrama de bloques que detalla el circuito de funcionamiento del prototipo:

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Diagrama%20de%20Bloques.png" alt="Diagrama de Bloques" width="100%"/>
  <br>
  <em>Diagrama de Bloques</em>
</p>

### Secuencia de Escaneo

Procederemos a explicar cada paso del escaneo acompañado de animaciones didácticas:

1. **Homing:** Previo al escaneo, se realiza el Homing para conocer la posición del escáner y así evitar colisiones, para esto se utiliza el Sensor de efecto Hall

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Animaciones/Homing.gif" alt="Homing del escáner" width="50%"/>
  <br>
  <em>Homing del escáner</em>
</p>

2.  **Ingreso:** Las piezas ingresan al sistema a través de la cinta transportadora.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Animaciones/Cinta.gif" alt="Ingreso" width="50%"/>
  <br>
  <em>La pieza ingresa al sistema</em>
</p>

3.  **Detección:** Un sensor TOF detecta la pieza y la centra en el escáner.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Animaciones/Centrado.gif" alt="Centrado de la pieza" width="50%"/>
  <br>
  <em>Centrado de la pieza</em>
</p>

4.  **Escaneo:** Una vez en posición, comienza el proceso de escaneo.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Animaciones/Escaneo%20Interior.gif" alt="Escaneo" width="50%"/>
  <br>
  <em>Proceso de escaneo</em>
</p>

5. **Expulsión:** Al finalizar el escaneo, se expulsa la pieza del sistema.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Animaciones/Salida.gif" alt="Expulsión de la pieza" width="50%"/>
  <br>
  <em>Se expulsa la pieza</em>
</p>

6.  **Procesamiento:** Se obtiene una nube de puntos representativa de las dimensiones del objeto.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Nube%20de%20puntos%20de%20escaneo.jpg" alt="GUI Escaneo Finalizado" width="45%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Escaneo%20Completado.jpg" alt="GUI Nube de puntos obtenida" width="45%"/>
  <br>
  <em>GUI Escaneo finalizado y nube de puntos obtenida</em>
</p>

7.  **Análisis:** Se realizan comparaciones con el modelo patrón para determinar fallas o deformaciones.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Escaneo%20Aprobado.jpg" alt="GUI Comparación Aprobado" width="45%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Resultado%20Comparacion.png" alt="GUI Comparación Desaprobado" width="45%"/>
  <br>
  <em>GUI Comparación</em>
</p>

<br>
<h1 align="center">Marco teórico</h1>

## Sensor Time Of Flight
La tecnología Time-of-Flight (ToF) o "Tiempo de Vuelo" es un método de medición de distancia basado en la velocidad de la luz. Un sensor ToF mide el tiempo absoluto de tránsito de un pulso de luz desde que es emitido hasta que regresa al detector.

El funcionamiento se desglosa en las siguientes etapas:

- **Emisión:** El sensor emite pulsos de luz infrarroja , invisible al ojo humano.

- **Reflexión:** La luz impacta sobre la superficie del objeto objetivo y se refleja.

- **Detección:** Sensor receptor sensa el instante exacto de llegada de la luz reflejada. 

El Emisor de luz infrarroja cuenta con una apertura de 25°, lo que significa que el haz se abre conicamente. Esto permite tener una zona de sensado, en la que se detecta paso a paso la posicion de la pieza y permite un centrado preciso de la cinta.

## Sensor Efecto Hall
El sensor de efecto Hall es un dispositivo electrónico de estado sólido utilizado para la detección de campos magnéticos. Se utiliza para realizar la secuencia de "Homing" del mecanismo de escaneo. 
A diferencia de los interruptores mecánicos tradicionales que requieren contacto físico, el sensor Hall funciona detectando la presencia de un imán permanente montado en un extremo del mecanismo.

El proceso ocurre en tres pasos:

- **Reposo:** Cuando el imán está lejos, el sensor mantiene su salida en un estado lógico inactivo (por ejemplo, HIGH o 5V).

- **Aproximación**: A medida que el mecanismo mueve el imán hacia el sensor, el campo magnético atraviesa el elemento sensible interno del sensor.

- **Conmutación:** Cuando la intensidad del campo magnético supera un umbral, el sensor cambia instantáneamente su salida al estado activo (LOW o 0V).

Estos cambios de estado nos permiten conocer el lugar en el espacio en el que se encuentra el mecanismo

## Motor Paso a Paso

El motor paso a paso es un convertidor electromecánico digital-analógico que transforma impulsos eléctricos discretos en movimientos mecánicos angulares precisos. A diferencia de los motores de corriente continua convencionales que giran libremente al aplicarles voltaje, el motor paso a paso rota en incrementos angulares fijos conocidos como "pasos".

Dado que las salidas lógicas del microcontrolador carecen de la capacidad de corriente necesaria para excitar las bobinas del motor, se requiere una etapa de potencia intermedia. Para este proyecto se seleccionó el controlador A4988.

Este controlador cumple dos funciones criticas. Por un lado nos permite regular la corriente que fluye hacia las bobinas del motor mediante un potenciometro, permitiendo ajustar el valor apropiado para que el motor no se salte pasos y pierda referencia. Y por otro lado este controlador nos permite realizar Microstepping, para posicionar el rotor en ubicaciones intermedias entre los polos magnéticos y permitirnos tener una resolucion angular de 0.1125° por paso. No solo nos da una presicion mucho mayor, sino que reduce el ruido de funcionamiento.

<br>
<h1 align="center">Escaneo 3D</h1>

El escaneo 3D es el proceso de analizar un objeto del mundo real para recolectar datos sobre su forma y construir modelos digitales tridimensionales. Los métodos de escaneo se dividen generalmente en dos categorías: pasivos y activos.

- **Métodos Pasivos:** Utilizan la luz ambiental existente para capturar la forma, como la estereoscopía (usar dos cámaras) o la "forma a partir de silueta". Estos métodos suelen enfrentar dificultades con superficies de textura uniforme, ya que les cuesta identificar el mismo punto en el espacio en múltiples vistas.

- **Métodos Activos:** Superan este problema emitiendo su propia fuente de iluminación controlada. Nuestro proyecto se enmarca en esta categoría. Al proyectar un patrón de luz conocido (en este caso, una línea láser) y observar su interacción con el objeto, se puede determinar la geometría de la superficie de manera robusta.

### Triangulación laser
La triangulación láser es el principio fundamental de la estación de escaneo. Se basa en una configuración geométrica precisa que involucra un conjunto cámara-proyector láser y un motor que los hace girar sobre un eje. En este sistema, el proyector no emite un simple punto, sino una "hendidura" o plano de luz.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Triangulacion.png" alt="Distribución del escáner para Triangulación Láser" width="50%"/>
  <br>
  <em>Distribución del escáner para Triangulación Láser</em>
</p>


El concepto de funcionamiento es el siguiente:

1. **El Plano Láser:** El proyector láser emite una hoja de luz plana. Normalmente la posición y orientación de este plano en el espacio tridimensional en este tipo de escáneres 3D se determina mediante la realización de una calibración. Pero en este caso el sistema se diseñó desde cero, conociendo su posición y no requiriendo de una calibración.

2. **El Rayo de la Cámara:** La cámara, modelada como un sistema "pinhole" (estenopeico), observa la escena. Cuando el plano láser incide sobre la superficie del objeto, crea una línea de luz visible y la cámara registra este perfil en un conjunto de píxeles específicos en su sensor.Cada píxel que detecta esta línea de luz es definida como un "rayo" (una línea recta en el espacio 3D) que viaja desde el centro de proyección de la cámara, a través del píxel, y hacia el objeto.

3. **Triangulación (Intersección Rayo-Plano):** Dado que se conoce la geometría del sistema, para cada píxel iluminado por el láser, se tienen dos elementos geométricos definidos: El plano de luz emitido por el láser, y el rayo de visión definido por el píxel en la cámara. La posición 3D exacta del punto en la superficie del objeto se calcula encontrando la intersección única entre este rayo y el plano. Este cálculo geométrico es lo que da nombre a la "triangulación".


### Nube de puntos

El principio de triangulación permite capturar un perfil 2D del objeto. Para construir un modelo 3D completo, se requiere un movimiento relativo entre el escáner y el objeto.

En la configuración de este proyecto, el conjunto de cámara y láser gira 360 grados alrededor de la pieza, mientras la pieza permanece estática. El proceso de adquisición de datos sigue estos pasos:

1. **Captura de Perfil:** En una posición angular fija, el láser ilumina la pieza y la cámara captura una imagen del perfil de luz.

2. **Cálculo de Puntos 3D:** Mediante el procesamiento de la imagen para detectar la línea láser y la aplicación del método de triangulación (intersección rayo-plano), se calcula la nube de puntos 3D que componen este perfil.

3. **Rotación:** El sistema cama-láser gira un ángulo conocido y pequeño.

4. **Repetición**: Se repiten los pasos 1 y 2 para la nueva posición angular, generando un nuevo perfil de puntos 3D.

5. **Fusión:** Este proceso se repite para una rotación completa de 360 grados. Dado que se conoce la posición del centro de giro y el ángulo de cada paso, todos los perfiles capturados se pueden transformar a un sistema de coordenadas global común. La "fusión" de todos estos perfiles individuales da como resultado la nube de puntos 3D completa que representa la geometría total del objeto.

<br>
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
| **Proteus** | Diseño de circuitos electrónicos. |

## Librerias de Python

| Librería | Descripción |
| :--- | :--- |
| **OpenCV** | Manejo de Cámara, captura de frames y detección del Láser. |
| **NumPy** | Procesamiento matemático de matrices y la nube de puntos. |
| **Pillow** | Procesamiento y manipulación básica de imágenes. |
| **PyVista** | Visualización 3D interactiva y renderizado de la nube de puntos. |
| **SciPy** | Algoritmos científicos para cálculos complejos y filtrado, Chamfer Distance. |
| **PySerial** | Comunicación serial para el control del Arduino. |
| **PyInstaller** | Empaquetado del programa en un archivo ejecutable. |
| **Tkinter** | Diseño de interfaz visual de usuario (GUI). |

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

<br>
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

<br>
<h1 align="center">Diseños y Esquemáticos</h1>

## Diseño Mecánico

Se presentan los esquemáticos y planos de vista explosionada de los diferentes mecanismos que componen al prototipo.

<p align="center">
  <img src="https://github.com/user-attachments/assets/6662ea1c-b2b9-45bd-9ced-6135f363e980" alt="Vista explosionada del mecanismo del Escáner" width="80%"/>
  <br>
  <em>Vista explosionada del mecanismo del Escáner</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e3c31136-6ab0-4f31-bc53-0533ac6cd761" alt="Vista explosionada de la Caja Contenedora" width="80%"/>
  <br>
  <em>Vista explosionada de la Caja Contenedora</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/705479f7-7092-40ff-b4d8-b58947d4625a" alt="Vista explosionada del mecanismo de la Cinta Transportadora" width="80%"/>
  <br>
  <em>Vista explosionada del mecanismo de la Cinta Transportadora</em>
</p>

## Diseño Electrónico

A continuación se presentan los planos que contienen el detalle del diseño electrónico del sistema.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Circuito.jpg" alt="Circuito Electrónico" width="80%"/>
  <br>
  <em>Circuito Electrónico</em>
</p>

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Conexión%20Arduino.jpg" alt="Conexión con Microcontrolador Arduino Uno" width="80%"/>
  <br>
  <em>Conexión con Microcontrolador Arduino Uno</em>
</p>

<br>
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

Al presionar el botón <b>"Comenzar escaneo"</b> Python informará a Arduino el inicio de la secuencia, durante el proceso de escaneo el usuario observará una barra de estado indicando la etapa actual del escaneo junto con una transmisión en vivo de la cámara. Cuando la pieza se encuentre en posición y comience el escaneo, aparecerá una barra de carga que indicará la muestra actual, muestras restantes y un tiempo estimado de finalización.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Escaneando.jpg" alt="GUI Comparación" width="45%"/>
  <br>
  <em>GUI Durante el escaneo</em>
</p>

Una vez finalizado el escaneo y habiendo expulsado la pieza, la interfaz cambiará haciendo saber al usuario que el escaneo ha finalizado y mostrando una ventana que le permitirá visualizar la nube de puntos obtenida.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Nube%20de%20puntos%20de%20escaneo.jpg" alt="GUI Escaneo Finalizado" width="45%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Escaneo%20Completado.jpg" alt="GUI Nube de puntos obtenida" width="45%"/>
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

Ahora sí procedemos con la comparación, la interfaz nos mostrará una ventana donde podremos elegir el archivo del escaneo dentro de nuestra PC, una vez seleccionada comenzará el proceso de la comparación.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Comparación%20Proceso.png" alt="GUI Comparación Proceso" width="45%"/>
  <br>
  <em>GUI Proceso de Comparación</em>
</p>

Una vez finalizado, nos aparecerá una pantalla indicando si la pieza se encuentra <b>Aprobada</b> ( el porcentaje de similitud es mayor al umbral seleccionado) o <b>Desaprobada</b> ( el porcentaje de similitud es menor al umbral seleccionado). 

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Escaneo%20Aprobado.jpg" alt="GUI Comparación Aprobado" width="45%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Escaneo%20Desaprobado.png" alt="GUI Comparación Desaprobado" width="45%"/>
  <br>
  <em>GUI Comparación Aprobada y Desaprobada</em>
</p>

También se nos mostrará una ventana aparte conteniendo el modelo Escaneado y el modelo Patrón superpuesto en negro, el color del Escaneado cambiará dependiendo de las zonas donde se encuentren defectos, las cuales se mostrarán en rojo.

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/GUI/Resultado%20Comparacion.png" alt="GUI Resultado Comparación" width="45%"/>
  <br>
  <em>GUI Resultado Comparación</em>
</p>

<br>
<h1 align="center">Escaneos Obtenidos</h1>

A continuación se muestran los resultados obtenidos del escaneo de las diferentes piezas planteadas, todos los escaneos fueron realizados con 100 muestras.


<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/Pieza%20A.gif" alt="Pieza A" width="30%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/Pieza%20B.gif" alt="Pieza B" width="30%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/Pieza%20C.gif" alt="Pieza C" width="30%"/>
  <br>
  <em>Piezas a Escanear</em>
</p>
<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/Patron%20A.gif" alt="Patrón A" width="30%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/Patron%20B.gif" alt="Patrón B" width="30%"/>
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Escaneos/Patron%20C.gif" alt="Patrón C" width="30%"/>
  <br>
  <em>Piezas Escaneadas</em>
</p>

<br>
<h1 align="center">Algoritmo de Comparación</h1>

Para lograr una comparación efectiva, optamos por la métrica <i>"Chamfer distance"</i> tambien conocida como <i>Distancia de Chaflán</i>. El cuál se utiliza para evaluar la similitud entre dos nubes de puntos. Esta se define como la suma de la distancia de cada punto de una <b>Nube A</b> con el punto más cercano de una <b>Nube B</b>, más la distancia de cada punto de la <b>Nube B</b> con el punto más cercano de la <b>Nube A</b>.

Para llevarla a cabo, primero se obtiene una media de ambas nubes de puntos para lograr centrarlas en el espacio en el eje X e Y. Luego se evalua la Distancia Chamfer utilizando el elemento <i>KDTree</i> de la libería <i>SciPy</i>. Este proceso se repite mientras la Nube de puntos comparada es rotada 45° en el eje Z utilizando una matríz de transformación. En el ángulo donde la distancia chamfer es la menor (Es decir la similitud entre ambas nubes es mayor) se vuelve a iterar la rotación, esta vez con un ángulo menor (45° / 2). Este proceso se repite 5 veces iterando con ángulos cada vez menores hasta lograr hallar la mayor similitud de la pieza.

Finalmente, la Distancia Chamfer se normaliza respecto a la diagonal del límite que contiene ambas nubes, convirtiéndose en un porcentaje de similitud mediante la función exponencial: <b>Similitud = e<sup>−(d/umbral)</sup> × 100</b>, donde <b>d</b> es la distancia Chamfer y el umbral se define como un porcentaje de la diagonal. Esto permite obtener valores entre 0% (nubes completamente diferentes) y 100% (nubes idénticas), de manera independiente a la escala del objeto.

<br>
<h1 align="center">Errores Cometidos y Lecciones Aprendidas</h1>

A la hora de realizar el proyecto, nos encontramos con varias problematicas, las cuales pasaremos a desarrollar a continuacion, incluyendo la manera que encontramos para solucionarlos.

**Cinta Transportadora**

  + La cinta patinaba, para lo cual:
    - Se le agregó un pedazo de tela a la base de las piezas.
    - Se utilizó el motor en 1/16 de paso para que el movimiento fuera más fluido, junto con una aceleración y desaceleración.
    
  + El sensor TOF no dejaba en el centro de la cinta a la pieza, debido a que funcionaba leyendo la cantidad de pasos que daba el motor:
    - Se modificó la secuencia, junto con el dieciseisavo de paso, para que fucionara más lentamente cuando la pieza fuera sensada y más rapido el resto del tiempo.
   
  + La pieza se corria transversalmente debido a que la cinta se iba hacia un lado:
    - Se alinearon los cilindros para que quedaran paralelos y la cinta corriera de manera centrada.

  + La cinta como conjunto quedó descentrada longitudinalmente debido a la falta de rigiez del fibrafacil:
    - Se consiguió a prueba y error, encontrar la cantidad de pasos extra que debía volver la pieza para quedar centrada.
  
  + No había manera de poner la pieza centrada a mano:
    - Se diseñó un centrado que apoya en los portarodamientos, el cual indica el sentido de la pieza.

**Caja de Escaneo**

  + El cable de la cámara tiraba y generaba que el motor se salteara pasos:
    - Se diseño una guía interna y externa.

**Cámara**
 
  + Era dificil alinear la cámara, la cual afectaba al escaneo:
    - Se diseño una guía tanto para la cámara como para el laser, de manera que se movieran conjuntamente.

**Escaneo**

  + El escaneo no era representativo de la pieza:
    - Se creó un archivo de escalamiento, con el cual, a traves de prueba y error, se encontraron los parametros para corregir la distorsión. 

<h1 align="center">Futuras Mejoras y Propuestas</h1>

**Cinta Transportadora**

  + Utilizar una cinta transportadora pre-armada, ya que requiere de un nivel de precisión extremadamente dificil de conseguir con una construcción manual.
  + Trabajar con sensores en los motores para el centrado de la pieza; o con un tipo distinto de sensor al del TOF.

**Caja de Escaneo**

  + Utilizar una caja de escaneo de un material más resitente, tanto para darle más rigidez y que soporte mejor los componentes, como para que la unión de la cinta con la caja sea mejor y quede mejor centrada.

**Mecanismo giratorio**
  + Implementacion de Anillo colector para evitar el enriedo de cables
  + Utilizacion de Poleas metalicas
  + Reemplazo de varilla roscada por una varilla mecanizada que se adapte mejor a las necesidades del mecanismo
  + Implementar un encencoder en el motor paso a paso que lo controla, deshaciendonos del uso del sensor de efecto hall.

**Escaneo**
  
  + Utilizar una cámara y sensor de mejor calidad, para una mayor precisión y resolución.
  + Trabajar con otro sistema de calibración que sea más preciso y genérico.

<h1 align="center">Conclusiones</h1>
En conclusión, el desarrollo de este prototipo funcional ha permitido validar la arquitectura del sistema con una inversión inicial reducida. Si bien esta fase experimental utiliza componentes económicos que representan solo una fracción del costo ideal, los resultados obtenidos en cuanto a repetibilidad y precisión son notables. Esto confirma la viabilidad técnica del proyecto y sienta las bases sólidas para el desarrollo de la versión final que, mediante la integración de componentes de grado profesional, potenciará aún más las capacidades metrológicas del sistema.

<h1 align="center">Galería del Proyecto</h1>

Imágenes detalladas del prototipo y sus componentes en funcionamiento.

<table>
  <tr>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/d32559f7-db63-44ba-8a2f-0f309882cbad" width="100%" />
    </td>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/282896cd-11f0-4a30-b808-303dae3bc109" width="100%" />
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/e76e9b4c-4a2d-4bfe-8e72-5bbad9504a32" width="100%" />
    </td>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/d8d6b97d-05f1-4d76-9329-75389ea69314" width="100%" />
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/1efcddf9-8e2e-47e9-899d-4249d0af6158" width="100%" />
    </td>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/f61ff91f-1e12-4905-afd6-db76f77e392e" width="100%" />
    </td>
  </tr>
</table>

---

<p align="center">
  <img src="https://github.com/JonatanBogadoUNLZ/PPS-Jonatan-Bogado/blob/9952aac097aca83a1aadfc26679fc7ec57369d82/LOGO%20AZUL%20HORIZONTAL%20-%20fondo%20transparente.png" width="45%"/>
</p>

<p align="center">
  <em><b>Proyecto realizado por Audisio Juan Pablo, Garrahan Alan y Reyna Valentin.</b></em>
  <br>
  <em>Ingeniería Mecatrónica</em>
  <br>
  <em>Facultad de Ingeniería - Universidad Nacional de Lomas de Zamora.</em>
</p>
