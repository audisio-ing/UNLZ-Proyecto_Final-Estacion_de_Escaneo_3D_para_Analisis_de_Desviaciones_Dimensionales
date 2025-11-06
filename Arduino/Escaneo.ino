#include <Adafruit_VL6180X.h>
#include <AccelStepper.h> // NUEVO: Incluir la biblioteca

// Sensor tof
Adafruit_VL6180X vl = Adafruit_VL6180X();

// Pines motores
const int enable = 7;
const int dirPinCinta = 8;
const int stepPinCinta = 9;
const int dirPinScanner = 10;
const int stepPinScanner = 11;

// NUEVO: Crear el objeto AccelStepper para la cinta
// (Modo DRIVER, pin de Step, pin de Dirección)
AccelStepper stepperCinta(AccelStepper::DRIVER, stepPinCinta, dirPinCinta);

// Variables Homing
bool homing = false;
int lastState = -1;
const int sensorPin = A0;

// Variables Cinta
const int pasosPorMuestra = 75;      // MODIFICADO: 75 pasos
// const int velRap = 1;              // YA NO SE USA: AccelStepper maneja la velocidad
const int pasosSalida = 14000;
const int muestrasSensado = 8;
const int pasosExtra = 780;

// Variables Escaneo
const int stepsPerRevMotor = 3200;
const float gearRatio = 40.0 / 24.0;
const int delayEscaneo = 1250;
const int delayPasos = 6;
int muestras = 0;
float pasoCamara = 0.0;

void setup() {
  pinMode(dirPinScanner, OUTPUT);
  pinMode(stepPinScanner, OUTPUT);
  // pinMode(dirPinCinta, OUTPUT);    // No es necesario, AccelStepper lo maneja
  // pinMode(stepPinCinta, OUTPUT);   // No es necesario, AccelStepper lo maneja

  // digitalWrite(dirPinCinta, HIGH); // No es necesario, AccelStepper lo maneja

  pinMode(enable, OUTPUT);
  digitalWrite(enable, LOW);

  Serial.begin(115200);

  // Inicializar sensor
  if (!vl.begin()) {
    Serial.println("Error: no se encontró VL6180X. Verifica conexiones.");
    while (1);
  }

  // NUEVO: Configurar los parámetros de aceleración para la cinta
  stepperCinta.setMaxSpeed(3200.0);
  stepperCinta.setAcceleration(6000.0);
}

// ===============================================================
// NUEVA FUNCIÓN "HELPER" PARA MOVER LA CINTA
// ===============================================================
/**
 * @brief Mueve la cinta un número relativo de pasos y espera a que termine.
 * @param pasosRelativos Pasos a mover. Positivo para avanzar, negativo para retroceder.
 */
void moverCintaBloqueante(long pasosRelativos) {
  // Establecer un nuevo objetivo RELATIVO a la posición actual
  stepperCinta.move(pasosRelativos);

  // Este bucle se ejecutará hasta que el motor llegue al objetivo.
  // Es "bloqueante", lo cual es necesario para tu estructura de código.
  while (stepperCinta.distanceToGo() != 0) {
    stepperCinta.run(); // Ejecuta los pasos necesarios para la aceleración
  }
}

// ===============================================================
// El resto de tu código (Loop, Escaneo, Homing, etc.)
// ===============================================================

void loop() {
  String input;

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
    CintaCentrado(); // MODIFICADO (internamente)
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
    CintaSalida(); // MODIFICADO (internamente)
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
      CintaCentrado(); // MODIFICADO (internamente)
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
      CintaSalida(); // MODIFICADO (internamente)
      Serial.println("Pieza expulsada");
      digitalWrite(enable, HIGH);
    }
  }

  digitalWrite(enable, HIGH);
  Serial.println("Motores Desactivados");
  delay(2000);
}

// ===============================================================
// FUNCIONES DEL SCANNER (SIN MODIFICAR)
// ===============================================================

void Escaneo() {
  bool escaneo = true;
  float pasosVuelta = 0;

  if (escaneo == true) {
    for (int i = 0; i < muestras; i++) {
      float anguloCamara = i * pasoCamara;
      delay(delayEscaneo);
      Serial.println(anguloCamara, 2);
      delay(delayEscaneo);

      if (i < muestras - 1) {
        float pasosMotor = (pasoCamara / 360.0) * stepsPerRevMotor * gearRatio;
        moverMotor(pasosMotor, escaneo);
        pasosVuelta += pasosMotor;
      }
    }
    escaneo = false;
    moverMotor(pasosVuelta, escaneo);
  }
}

void moverMotor(float pasos, bool escaneo) {
  int pasosEnteros = round(pasos);

  if (escaneo == true) {
    digitalWrite(dirPinScanner, HIGH);
    for (int i = 0; i < pasosEnteros; i++) {
      digitalWrite(stepPinScanner, HIGH);
      delay(delayPasos);
      digitalWrite(stepPinScanner, LOW);
      delay(delayPasos);
    }
  }
  else {
    digitalWrite(dirPinScanner, LOW);
    for (int i = 0; i < pasosEnteros; i++) {
      digitalWrite(stepPinScanner, HIGH);
      delay(delayPasos / 3);
      digitalWrite(stepPinScanner, LOW);
      delay(delayPasos / 3);
    }
  }
}

void Homing() {
  digitalWrite(dirPinScanner, LOW);
  lastState = magnetico();

  while (homing == false) {
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
  moverMotor(640, true);
}

int magnetico() {
  int value = analogRead(sensorPin);
  if (value > 700) return 1;
  if (value < 50) return 0;
  return -1;
}

// ===============================================================
// FUNCIONES DE MEDICIÓN Y CINTA (MODIFICADAS)
// ===============================================================

// Funcion para sensar con el VL6180X (SIN MODIFICAR)
int medicion(int n = 5) {
  long suma = 0;
  for (int i = 0; i < n; i++) {
    suma += vl.readRange();
    delay(2); // Pausa entre lecturas
  }
  return suma / n; // Promedio
}

// ===============================================================
// FUNCIONES DE LA CINTA (MODIFICADAS CON ACCELSTEPPER)
// ===============================================================

// Funcion para mover la cinta y centrar la pieza
void CintaCentrado() {
  int pasosCentrado = 0;
  bool enRango = false;

  // Ya no se necesita 'digitalWrite(dirPinCinta, HIGH)'
  // La función 'moverCintaBloqueante' maneja la dirección.

  // --- Parte 1: Avanzar hasta detectar la pieza ---
  while (enRango == false) {
    // Mueve 'pasosPorMuestra' (75) pasos hacia adelante y espera
    moverCintaBloqueante(pasosPorMuestra);

    int distancia = medicion();
    if (distancia < 120) {
      enRango = true;
    }
  }

  // --- Parte 2: Avanzar mientras se detecta la pieza (para medirla) ---
  while (enRango == true) {
    // Mueve 'muestrasSensado' (8) pasos hacia adelante y espera
    moverCintaBloqueante(muestrasSensado);

    pasosCentrado += muestrasSensado; // Acumula los pasos medidos

    int distancia = medicion();
    if (distancia > 120) {
      enRango = false;
    }
  }

  // --- Parte 3: Retroceder para centrar ---
  if (pasosCentrado > 0) {
    // Ya no se necesita 'digitalWrite(dirPinCinta, LOW)'
    
    // Calcula el retroceso total: la mitad de la pieza + un extra
    long retrocesoTotal = (pasosCentrado / 2) + pasosExtra;

    // Mueve el total de pasos en REVERSA (usando un número negativo)
    moverCintaBloqueante(-retrocesoTotal);
  }
}

void CintaSalida() {
  // Ya no se necesita 'digitalWrite(dirPinCinta, HIGH)'

  // Mueve 'pasosSalida' pasos hacia adelante y espera
  moverCintaBloqueante(pasosSalida);
}
