#include <Adafruit_VL6180X.h> 

// Sensor tof
Adafruit_VL6180X vl = Adafruit_VL6180X();

// Pines motores
const int enable = 7;
const int dirPinCinta = 8;
const int stepPinCinta = 9;
const int dirPinScanner = 10;
const int stepPinScanner = 11;

// Variables Homing
bool homing = false;                  // Indica si se hizo el homing
int lastState = -1;                   // Ultimo estado del sensor
const int sensorPin = A0;             // Sensor magnético

// Variables Cinta
const int pasosPorMuestra = 50;       // Cada cuantos pasos toma una muestra
const int velRap = 1;                 // Velocidad de desplazamiento de la cinta
const int pasosSalida = 14000;        // Pasos de la cinta para expulsar la pieza
const int muestrasSensado = 8;        // Intervalo de pasos para sensar en el centrado
const int pasosExtra = 825;           // Pasos extra para centrar correctamente la pieza

// Variables Escaneo
const int stepsPerRevMotor = 3200;    // 200 * 16 (1/16 microstepping)
const float gearRatio = 40.0 / 24.0;  // Relación de engranajes
const int delayEscaneo = 1250;        // Tiempo entre mediciones
const int delayPasos = 6;             // Tiempo entre pasos en microsegundos
int muestras = 0;                     // N° de muestras en 360°, ingresado por el usuario
float pasoCamara = 0.0;               // Grados a moverse entre cada muestra

void setup() {
  pinMode(dirPinScanner, OUTPUT);
  pinMode(stepPinScanner, OUTPUT);
  pinMode(dirPinCinta, OUTPUT);
  pinMode(stepPinCinta, OUTPUT);

  digitalWrite(dirPinCinta, HIGH);  // Sentido de avance

  pinMode(enable, OUTPUT);          // Enable motores
  digitalWrite(enable, LOW);        // LOW para activarlos

  Serial.begin(115200);

  // Inicializar sensor
  if (!vl.begin()) {
    Serial.println("Error: no se encontró VL6180X. Verifica conexiones.");
    while (1);
  }
}

void loop() {
  String input; // Recibe el input

  digitalWrite(enable, HIGH);

  // Modos de funcionamiento
  Serial.println("¿Modo automático? (y/n)");
  while (Serial.available() == 0) { delay(10); }
  input = Serial.readStringUntil('\n');
  input.trim();

  if (input == "y" || input == "Y") {
    Serial.println("Modo automático activado.");

    digitalWrite(enable, LOW);

    Serial.println("Realizando homing...");
    Homing();
    Serial.println("Homing completado");

    Serial.println("Avanzando pieza...");
    CintaCentrado();
    Serial.println("Pieza en posición");

    Serial.println("¿Cuántas muestras desea tomar?");
    while (Serial.available() == 0) { delay(10); }
    input = Serial.readStringUntil('\n');
    input.trim();
    muestras = input.toInt();

    pasoCamara = 360.0 / muestras;
    Serial.println("Iniciando escaneo...");
    Escaneo();
    Serial.println("Escaneo finalizado");

    Serial.println("Expulsando pieza...");
    CintaSalida();
    Serial.println("Pieza expulsada");

    digitalWrite(enable, HIGH);

    Serial.println("Motores desactivados");
  } 
  else {
    // Modo Manual
    Serial.println("¿Realizar homing? (y/n)");
    while (Serial.available() == 0) { delay(10); }
    input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "y" || input == "Y") {
      digitalWrite(enable, LOW);
      
      Serial.println("Realizando homing...");
      Homing();
      Serial.println("Homing completado.");

      digitalWrite(enable, HIGH);
    }

    Serial.println("¿Centrar pieza? (y/n)");
    while (Serial.available() == 0) { delay(10); }
    input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "y" || input == "Y") {
      digitalWrite(enable, LOW);

      Serial.println("Avanzando pieza...");
      CintaCentrado();
      Serial.println("Pieza en posición");

      digitalWrite(enable, HIGH);
    }

    Serial.println("¿Escanear pieza? (y/n)");
    while (Serial.available() == 0) { delay(10); }
    input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "y" || input == "Y") {
      Serial.println("¿Cuántas muestras desea tomar?");
      while (Serial.available() == 0) { delay(10); }
      input = Serial.readStringUntil('\n');
      input.trim();
      muestras = input.toInt();

      pasoCamara = 360.0 / muestras;

      digitalWrite(enable, LOW);

      Serial.println("Iniciando escaneo...");
      Escaneo();
      Serial.println("Escaneo finalizado");

      digitalWrite(enable, HIGH);
    }


    Serial.println("¿Expulsar pieza? (y/n)");
    while (Serial.available() == 0) { delay(10); }
    input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "y" || input == "Y") {
      digitalWrite(enable, LOW);

      Serial.println("Expulsando pieza...");
      CintaSalida();
      Serial.println("Pieza expulsada");

      digitalWrite(enable, HIGH);
    }
  }

  digitalWrite(enable, HIGH);
  Serial.println("Motores Desactivados");
  
  delay(2000);
}


void Escaneo() {
  bool escaneo = true; // Indica a la funcion moverMotor el sentido de giro
  float pasosVuelta = 0; //Almacena la cantidad de pasos que luego retrocedera

  if(escaneo==true){ // Determina si escanear o no
    
    for (int i=0; i < muestras; i++) { // Escaneo
      float anguloCamara = i * pasoCamara;

      delay(delayEscaneo); // Para evitar vibraciones en el escaneo

      Serial.println(anguloCamara, 2); // Enviar angulo actual, 2 decimales

      delay(delayEscaneo); // Esperar mientras Python escanea

      if (i < muestras - 1) { // Rotacion
        float pasosMotor = (pasoCamara / 360.0) * stepsPerRevMotor * gearRatio;
        moverMotor(pasosMotor, escaneo);
        
        pasosVuelta += pasosMotor; // Angulo que luego retrocedera el motor
      }
    }

    // Vuelta a 0, retrocediendo el total de angulos
    escaneo = false;
    moverMotor(pasosVuelta, escaneo);
  }
}

// Funcion para mover motor, recibe los pasos a mover y el sentido
void moverMotor(float pasos,bool escaneo) {
  int pasosEnteros = round(pasos);

  if(escaneo == true){
    digitalWrite(dirPinScanner, HIGH); // Sentido antihorario

    for (int i = 0; i < pasosEnteros; i++) {
      digitalWrite(stepPinScanner, HIGH);
      delay(delayPasos);
      digitalWrite(stepPinScanner, LOW);
      delay(delayPasos);
    }
  }
  else{
    digitalWrite(dirPinScanner, LOW); // Sentido horario

    // Movimiento más rapido para regreso
    for (int i = 0; i < pasosEnteros; i++) {
      digitalWrite(stepPinScanner, HIGH);
      delay(delayPasos / 3); 
      digitalWrite(stepPinScanner, LOW);
      delay(delayPasos / 3);
    }
  }
}

// Funcion para sensar con el VL6180X
int medicion(int n = 5) {
  long suma = 0;
  for (int i = 0; i < n; i++) {
    suma += vl.readRange();
    delay(2); // Pausa entre lecturas
  }
  return suma / n; // Promedio
}

// Funcion para mover la cinta y centrar la pieza
void CintaCentrado() {
  int pasosCentrado = 0;
  int contadorPasos = 0;
  bool enRango = false;

  digitalWrite(dirPinCinta, HIGH); // Sentido de avance

  while(enRango == false){
    digitalWrite(stepPinCinta, HIGH);
    delay(velRap);
    digitalWrite(stepPinCinta, LOW);
    delay(velRap);
    contadorPasos++;

    if (contadorPasos >= pasosPorMuestra) {
      contadorPasos = 0;
      int distancia = medicion();

      if(distancia < 120){
        enRango = true;
      }
    }
  }

  while(enRango == true){
    for(int i = 0; i < muestrasSensado; i++){
      digitalWrite(stepPinCinta, HIGH);
      delay(velRap);
      digitalWrite(stepPinCinta, LOW);
      delay(velRap);

      pasosCentrado++;
    }

    int distancia = medicion();

    if(distancia > 120){
      enRango = false;
    }
  }

  if(pasosCentrado > 0){
    digitalWrite(dirPinCinta, LOW); // Sentido Retroceso

    for (int i = 0; i < (pasosCentrado/2); i++) {
      digitalWrite(stepPinCinta, HIGH);
      delay(velRap);
      digitalWrite(stepPinCinta, LOW);
      delay(velRap);
    }
    
    for (int i = 0; i < pasosExtra; i++) {
      digitalWrite(stepPinCinta, HIGH);
      delay(velRap);
      digitalWrite(stepPinCinta, LOW);
      delay(velRap);
    }
  }
}

void CintaSalida(){
  digitalWrite(dirPinCinta, HIGH); // Sentido de avance
  for (int i = 0; i < int(pasosSalida); i++) {
      digitalWrite(stepPinCinta, HIGH);
      delay(velRap);
      digitalWrite(stepPinCinta, LOW);
      delay(velRap);
  }
}

void Homing() {
  digitalWrite(dirPinScanner, LOW); 
  lastState = magnetico();

  while(homing == false){
    // Mover el motor
    digitalWrite(stepPinScanner, HIGH);
    delay(delayPasos);
    digitalWrite(stepPinScanner, LOW);
    delay(delayPasos);

    int currentState = magnetico();

    if (currentState != lastState && currentState != -1) {
      homing = true;
    }
  }

  delay(1000);
  moverMotor(640, true);  // Mueve la camara unos pasos en el sentido contrario para despejar la cinta
}

// Leer sensor magnético
int magnetico(){
  int value = analogRead(sensorPin);
  if (value > 700) return 1;   // polo +
  if (value < 50) return 0;    // polo -
  return -1;                   
}
