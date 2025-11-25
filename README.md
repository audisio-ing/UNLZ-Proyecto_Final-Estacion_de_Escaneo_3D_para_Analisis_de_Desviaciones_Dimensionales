<h2 align="center">F.IU.N.L.Z. Proyecto Final</h2>
<h1 align="center" style="font-size: 3em;">Estacion de Escaneo 3D para Análisis de Desviaciones Dimensionales</h1>

<p align="center">
  <img src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Estacion_de_Escaneo_3D_para_Analisis_de_Desviaciones_Dimensionales/blob/main/Imagenes/Animaciones/Paneo.gif" alt="Demostración" width="300"/>
  <br>
  <em>Vista general</em>
</p>

# Team Members
<p>👤 <a href="https://github.com/audisio-ing">Juan Pablo Audisio</a></p>
<p>👤 <a href="https://github.com/IngGarrahan">Alan Garrahan</a></p>
<p>👤 <a href="https://github.com/ValentinReyna">Valentín Julián Reyna</a></p>

# Index
- **1.0** [🔗 Introducción 🔗](#-introducción-)
- **2.0** [📲 Descripción del Sistema 📲](#-descripción-del-sistema-)
- **3.0** [💻 Tecnologías y Recursos 💻](#-tecnologías-y-recursos-)
    - **3.1** [Software y Programación](#software-y-programación-)
    - **3.2** [Hardware y Electrónica](#hardware-y-electrónica-)
- **4.0** [🔩 Listado de Componentes 🔩](#-listado-de-componentes-)
- **5.0** [💡 Diseños y Esquemáticos 💡](#-diseños-y-esquemáticos-)
- **6.0** [📲 Instrucciones de Uso 📲](#-instrucciones-de-uso-)
- **7.0** [📊 Escaneos 📊](#-escaneos-)
- **8.0** [📷 Galería del Proyecto 📷](#-galería-del-proyecto-)
- **9.0** [📂 Estructura del Repositorio 📂](#-estructura-del-repositorio-)

<h1 align="center">🔗 Introducción 🔗</h1>

Este repositorio corresponde al Proyecto Final de la carrera de Ingeniería Mecatrónica, desarrollado a lo largo del 2025 en la Universidad Nacional de Lomas de Zamora, Facultad de Ingeniería.

El objetivo principal es buscar una solución innovadora para el control de calidad. Proponemos un nuevo enfoque que permite un control detallado, pieza por pieza. Esto asegura que el producto final cumpla con los estándares requeridos. El sistema garantiza precisión, consistencia y velocidad en la detección de defectos y variaciones causadas por las matrices de producción.

<p align="center">
  <img src="https://github.com/user-attachments/assets/71f6aba0-a154-4566-917d-9b140b0019e3" alt="Vista General" width="800"/>
  <br>
  <em>Vista general de la estación de escaneo</em>
</p>

<h1 align="center">📲 Descripción del Sistema 📲</h1>

Este proyecto consiste en una línea de control integral. Está equipada con un scanner 3D que funciona bajo el principio de triangulación láser. Su fin es la detección de fallas en procesos productivos con matrices destinadas a producciones en serie. Todo el sistema está unido a través de una cinta transportadora y un software de control central.

### Funcionamiento del Proceso

1.  **Ingreso:** Las piezas ingresan al sistema a través de la cinta transportadora.
2.  **Detección:** Un sensor TOF detecta la pieza y detiene la marcha en la posición correcta.
3.  **Escaneo:** Una vez en posición, comienza el proceso de escaneo láser.
4.  **Procesamiento:** Se obtiene una nube de puntos representativa de las dimensiones del objeto.
5.  **Análisis:** Se realizan comparaciones con el modelo patrón para determinar fallas o deformaciones.

<h1 align="center">💻 Tecnologías y Recursos 💻</h1>

## Software y Programación ♕

| Tecnología | Descripción |
| :--- | :--- |
| **Python** | Lenguaje principal para el procesamiento de datos, lógica de control y visión computacional. |
| **Arduino IDE** | Utilizado para programar el microcontrolador que maneja los motores y sensores físicos. |
| **ROS** | (Robot Operating System) Implementado para la gestión de nodos y comunicación del robot. |
| **OpenCV** | Librería de visión artificial utilizada para el procesamiento de las capturas del láser. |
| **TensorFlow / AI** | Redes neuronales y algoritmos de machine learning para el análisis de patrones. |

## Hardware y Electrónica ⚡

| Componente | Uso en el proyecto |
| :--- | :--- |
| **Arduino Uno** | Cerebro del control físico (motores y sensores). |
| **Nema 17** | Motores paso a paso para el movimiento de la cinta y el escáner. |
| **Driver A4988** | Controladores para el manejo preciso de los motores paso a paso. |
| **Láser de Barra** | Fuente de luz para realizar la triangulación sobre la pieza. |
| **Sensor TOF** | Sensor de tiempo de vuelo para detectar la presencia y distancia de las piezas. |

<h1 align="center">🔩 Listado de Componentes 🔩</h1>

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

<h1 align="center">💡 Diseños y Esquemáticos 💡</h1>

Se presentan los esquemáticos y diagramas de diseño que explican el ensamblaje y la operación de los sistemas.

<p align="center">
  <img src="https://github.com/user-attachments/assets/6662ea1c-b2b9-45bd-9ced-6135f363e980" alt="Plano 1" width="800"/>
  <br>
  <em>Plano General del Dispositivo</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e3c31136-6ab0-4f31-bc53-0533ac6cd761" alt="Circuito" width="800"/>
  <br>
  <em>Esquemático de Conexiones Electrónicas</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/705479f7-7092-40ff-b4d8-b58947d4625a" alt="Plano 2" width="800"/>
  <br>
  <em>Detalle de mecanismos</em>
</p>

<h1 align="center">📲 Instrucciones de Uso 📲</h1>

Para poner en marcha el sistema, siga los siguientes pasos detallados:

### Paso 1: Inicialización
Descripción del primer paso para poner en marcha el proyecto (rellenar aquí).

### Paso 2: Calibración
Descripción del segundo paso, calibración de sensores o cámara (rellenar aquí).

### Paso 3: Ejecución
Cualquier otro paso relevante que se deba seguir para iniciar el escaneo.

<h1 align="center">📊 Escaneos 📊</h1>

En esta sección se presentan los resultados obtenidos tras el proceso de digitalización. Las siguientes imágenes muestran la nube de puntos generada y las comparaciones dimensionales realizadas por el software.

<p align="center">
  <img src="URL_DE_TU_IMAGEN_1" alt="Escaneo 1" width="30%"/>
  <img src="URL_DE_TU_IMAGEN_2" alt="Escaneo 2" width="30%"/>
  <img src="URL_DE_TU_IMAGEN_3" alt="Escaneo 3" width="30%"/>
</p>
<p align="center">
  <img src="URL_DE_TU_IMAGEN_4" alt="Escaneo 4" width="30%"/>
  <img src="URL_DE_TU_IMAGEN_5" alt="Escaneo 5" width="30%"/>
  <img src="URL_DE_TU_IMAGEN_6" alt="Escaneo 6" width="30%"/>
</p>
<p align="center">
  <em>Resultados visuales del proceso de escaneo y análisis</em>
</p>

<h1 align="center">📷 Galería del Proyecto 📷</h1>

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

<h1 align="center">📂 Estructura del Repositorio 📂</h1>

A continuación se detallan las carpetas que estructuran este repositorio:

* **CODIGO:** Contiene el código fuente utilizado (Python/Arduino).
* **MULTIMEDIA:** Imágenes y videos del desarrollo y funcionamiento.
* **PLANOS:** Esquemáticos y diagramas de los sistemas implementados.
* **DATASHEET:** Hojas de datos y especificaciones de componentes.
* **INFORMES:** Documentación, Gantt, informes PDF y manuales.

---
<p align="center">
  <em>Proyecto realizado por Audisio Juan Pablo, Garrahan Alan y Reyna Valentin.</em>
  <br>
  <em>Facultad de Ingeniería - Universidad Nacional de Lomas de Zamora.</em>
</p>
