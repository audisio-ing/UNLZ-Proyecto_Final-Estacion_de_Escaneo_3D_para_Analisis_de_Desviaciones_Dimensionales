# UNLZ-Proyecto_Final-Scanner_por_triangulacion_laser-ARG
<p align="center" width="100%">
    <img width="100%" src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Scanner_por_triangulacion_laser-ARG/blob/main/fotos/LOGO%20AZUL%20HORIZONTAL%20-%20fondo%20transparente.png">
</p>

## MOTIVACIÓN

Buscamos desarrollar una solución innovadora para el control de calidad, un nuevo enfoque que permita un control detallado pieza por pieza asegurándose de que el producto final cumpla con los estándares requeridos. Garantizar la precisión, consistencia y velocidad en la detección de defectos y variaciones en las piezas.

## DESCRIPCIÓN DE LA PROPUESTA

Una línea de control integral equipada con un scanner 3D funcionando con el principio de triangulación láser, con el fin de detección de fallas en matrices destinadas a producciones en serie. Todo unido a traves de una cinta transportadora y software de control.

Las piezas ingresarán al sistema a través de una cinta transportadora y serán posicionadas dentro de la estación de escaneo 3D. Tras ser escaneadas obtendremos una nube de puntos representativa de las dimensiones del objeto, a partir de la cual se realizarán comparaciones con el modelo patrón de la misma a fin de determinar posibles fallas y deformaciones en la misma causadas por la matriz, que puedan afectar su funcionamiento
<img width="889" height="693" alt="Image" src="https://github.com/user-attachments/assets/699a483f-ee6d-461c-a317-fea6d5491d8e" />
<img width="1058" height="725" alt="Image" src="https://github.com/user-attachments/assets/25d69f92-a21b-4755-ba29-4997b0ef8d05" />
<img width="1045" height="719" alt="Image" src="https://github.com/user-attachments/assets/e5e8e849-fd24-44ea-bada-80cbff33d3da" />
<img width="1076" height="349" alt="Image" src="https://github.com/user-attachments/assets/d32559f7-db63-44ba-8a2f-0f309882cbad" />
<img width="711" height="349" alt="Image" src="https://github.com/user-attachments/assets/bcb61308-42c2-4fdd-91a2-48318b8be97d" />
<img width="1075" height="642" alt="Image" src="https://github.com/user-attachments/assets/e76e9b4c-4a2d-4bfe-8e72-5bbad9504a32" />
<img width="686" height="509" alt="Image" src="https://github.com/user-attachments/assets/d8d6b97d-05f1-4d76-9329-75389ea69314" />
## ALCANCE

Al fin de la cursada se presentará un prototipo funcional del sistema que cumpla de forma eficaz la tarea propuesta, no podemos asegurar un funcionamiento eficiente ya que el mismo dependerá de los componentes que seamos capaces de obtener.

Se presentará un prototipo que cuente con una cinta de transporte funcional capaz de transportar las piezas hasta la estación de escaneo 3D retroalimentada con una cámara y un láser de barra, y luego retirar la pieza de la estación de escaneo.

El sistema contará con tres variantes de piezas funcionales con cualidades únicas para comprobar el funcionamiento del sistema.

La estación de escaneo 3D será capaz de escanear una órbita 360° alrededor de la pieza y devolviendo una nube de puntos de la misma que luego será utilizada para su comparación con la pieza patrón. El porcentaje de similitud con la misma determinará si la matriz fabricada es apta para la implementación en línea de producción

## ESPECIFICACION DE REQUERIMIENTOS
El sistema será capaz de mover una pieza por una línea de producción y ubicarla precisamente en el centro de la zona de escaneo. Luego escaneará la pieza y armará una nube de puntos, la cual luego será utilizada para generar un mallado que le permita identificar al sistema el tipo de pieza y reconocer errores para verificar si cumple con los estándares requeridos.

## DISEÑO FUNCIONAL

El siguiente diagrama de bloques muestra el diseño funcional del sistema a gran escala, los pasos a seguir y el resultado esperado de cada uno:

<img width="1103" height="777" alt="Image" src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Scanner_por_triangulacion_laser-ARG/blob/main/fotos/Diagrama%20de%20Bloques%20fondo.png" />

## CONEXIONES DEL MICROCONTROLADOR

<img width="1103" height="777" alt="Image" src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Scanner_por_triangulacion_laser-ARG/blob/main/fotos/Captura%20de%20pantalla%202025-09-01%20185708.png" />

## COSTO DEL PROTOTIPO, PRESUPUESTOS, PLAZOS DE ENTREGA DE MATERIALES

A continuación se incluye el BOM (Bill of Materials) que detalla los materiales necesarios para la realización del proyecto, junto con sus respectivos valores, tiempos de entrega y proveedores tanto en pesos y dólares, presentando alternativas de cada uno.

| Cantidad | Modelo | Componente | Descripción | Precio Unitario | Precio Total ARS | Precio total USD | Proveedor | Plazo de Entrega |
|----------|--------|------------|-------------|-----------------|------------------|------------------|-----------|------------------|
| 2 | nema 17 | Motor paso a paso | movimiento de la línea | $26,250.00 | $52,500.00 | $40.08 | it&t | Una Semana |
| 2 | a4988 | Controlador | Control de Motores | $4,250.00 | $8,500.00 | $6.49 | it&t | Una Semana |
| 1 | 100uF X 50v | Capacitor | Regulación de voltaje de entrada a controladores a4988 | $185.00 | $185.00 | $0.14 | it&t | Una Semana |
| 1 | x10 10k OHM | Resistencia | Circuito electrónico | $7,000.00 | $7,000.00 | $5.34 | it&t | Una Semana |
| 1 | Ss495a | Sensor efecto hall | Detección de rotación de mecanismo | $4,000.00 | $4,000.00 | $3.06 | it&t | Una Semana |
| 1 | Pcb Placa Fibra Protoboard Simple Faz 8x12 | PCB de prototipado | Conexión de controladores de motores paso a paso | $4,106.33 | $4,106.33 | $3.13 | it&t | Una Semana |
| 1 | lote x3 iman 5mm | Iman neodimio | Inducción sensor efecto hall | $1,000.00 | $1,000.00 | $0.76 | it&t | Una Semana |
| 1 | x10 led 5v | LED | Indicación de funcionamiento | $1,942.00 | $1,942.00 | $1.15 | it&t | Una Semana |
| 1 | display lcd backlight azul 20 x 4 5v | Pantalla LCD | Display de información | $15,000.00 | $15,000.00 | $11.45 | it&t | Una Semana |
| 1 | 1.75mm | 1kg PLA | Impresión de Partes | $19,000.00 | $19,000.00 | $14.50 | printALot | Una Semana |
| 1 | UNO | Arduino | Manejo de Motores Cinta Transportadora | $9000.00 | $9000.00 | $6.9 | TodoMicro | Una Semana |
| 1 | 12v5A | Fuente 12V | Alimentación de Motores | $12,944.00 | $12,944.00 | $9.89 | Mundo Led | Una Semana |
| 2 | Dupont 20cm | Cable x40 | Conexión entre Componentes Arduino | $2,604.00 | $5,208.00 | $3.98 | Duaitek | Una Semana |
| 1 | 830 Puntos | Protoboard | Placa para Componentes | $2,598.00 | $2,812.00 | $1.98 | TodoMicro | Una Semana |
| 1 | 1m varilla roscada | Cinta Transportadora y mecanismo giratorio | Transporte de piezas y escaneo | $8,000.00 | $8,000.00 | - | - | Una Semana |
| 6 | Rodamientos | Cinta Transportadora y mecanismo giratorio | Transporte de piezas y escaneo | $4,231.00 | $25,386.00 | $19.30 | Ingia | Una Semana |
| 1 | perfil aluminio 2020 tipo bosch R 415mm | Mecanismo giratorio | Escaneo | $4,163.00 | - | - | Ingia | Una Semana |
| 1 | Correa cerrada 150mm | Mecanismo giratorio | Escaneo | $6,396.00 | $6,396.00 | $4.86 | Ingia | Una Semana |
| 1 | material determinado de cinta | Cinta Transportadora | Transporte de piezas | - | - | - | - | Una Semana |
| 1 | 50cm tubo plastico | Cinta Transportadora | Transporte de piezas | - | - | - | - | Una Semana |
| 1 | 80cm x 180cm de fibrofacil de 3mm espesor | Caja de escaneo | Transporte de piezas | - | - | - | - | Una Semana |
| 1 | Perfil cuadrado de madera 2.3cm x 2.3 cm | Caja de escaneo | Transporte de piezas y Caja | - | - | - | - | Una Semana |

**Total: $186,747.33 ARS — $142.56 USD**

<img width="1066" height="746" alt="Image" src="https://github.com/user-attachments/assets/bfa12b66-d8bf-4085-973b-f410c8f8500e" />

## CRONOGRAMA DE TRABAJO

A continuación se incluye el diagrama de Gantt a seguir durante el proyecto

<img width="1103" height="777" alt="Image" src="https://github.com/audisio-ing/UNLZ-Proyecto_Final-Scanner_por_triangulacion_laser-ARG/blob/main/fotos/Gantt.png" />

<h3>Funcionalidades a presentar en cada hito</h3>
<p>A continuación se detallan las funcionalidades a presentar en cada hito</p>

<table>
  <tr>
    <th>Hito</th>
    <th>Fecha a cumplir</th>
    <th>Funcionalidades</th>
  </tr>
  <tr>
    <td><strong>Primera entrega</strong></td>
    <td><em>22/09/25</em></td>
    <td>
      Secuencia de escaneo funcional, conexión con Python y visualización de datos.  
      Cinta transportadora funcional.
    </td>
  </tr>
  <tr>
    <td><strong>Segunda entrega</strong></td>
    <td><em>20/10/25</em></td>
    <td>
      Secuencia completa, comparación de nube de puntos.  
      Sensores funcionales.
    </td>
  </tr>
</table>




