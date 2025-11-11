#include <Adafruit_VL6180X.h>
#include <AccelStepper.h>

// Sensor tof
Adafruit_VL6180X vl = Adafruit_VL6180X();

// Pines motores
const int enable = 7;
const int dirPinCinta = 8;
const int stepPinCinta = 9;
const int dirPinScanner = 10;
const int stepPinScanner = 11;

// AccelStepper para la cinta
AccelStepper stepperCinta(AccelStepper::DRIVER, stepPinCinta, dirPinCinta);
// AccelStepper para el scanner
AccelStepper stepperScanner(AccelStepper::DRIVER, stepPinScanner, dirPinScanner);

// Variables Homing
bool homing = false;
int lastState = -1;
const int sensorPin = A0;

// Variables Cinta
const int pasosPorMuestra = 75;
const int pasosSalida = 14000;
const int muestrasSensado = 8;
const int pasosExtra = 780;

// Variables Escaneo
const int stepsPerRevMotor = 3200;
const float gearRatio = 40.0 / 24.0;
const int delayEscaneo = 1000;
int muestras = 0;
float pasoCamara = 0.0;
const float velLenta = 500.0;
const float velRapida = 1000.0;
const float acelScanner = 1000.0;

void setup() {
   pinMode(enable, OUTPUT);
   digitalWrite(enable, LOW);

   Serial.begin(115200);

   // Inicializar sensor
   if (!vl.begin()) {
      Serial.println("Error: no se encontró VL6180X. Verifica conexiones.");
      while (1);
   }

   // Parámetros de aceleración para la cinta
   stepperCinta.setMaxSpeed(3200.0);
   stepperCinta.setAcceleration(6000.0);

   // Parámetros de aceleración para el scanner
   stepperScanner.setMaxSpeed(velLenta); 
   stepperScanner.setAcceleration(acelScanner);
}

/**
  * @brief Mueve la cinta un número relativo de pasos y espera a que termine.
  * @param pasosRelativos Pasos a mover. Positivo para avanzar, negativo para retroceder.
  */
void moverCintaBloqueante(long pasosRelativos) {
   stepperCinta.move(pasosRelativos);
   while (stepperCinta.distanceToGo() != 0) {
      stepperCinta.run(); 
   }
}

void loop() {
   String input;

   digitalWrite(enable, HIGH);

   delay(1000);

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
      
      digitalWrite(enable, HIGH);

      Serial.println("¿Cuántas muestras desea tomar?");
      while (Serial.available() == 0) { delay(10); }
      input = Serial.readStringUntil('\n');
      input.trim();
      muestras = input.toInt();

      digitalWrite(enable, LOW);

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

// Funcion de escaneo
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
      // Mueve de vuelta al inicio, desenrieda el cable
      moverMotor(pasosVuelta, escaneo);
   }
}

// Funcion para mover el motor del escaner
void moverMotor(float pasos, bool escaneo) {
   int pasosEnteros = round(pasos);

   if (escaneo == true) {
    // Mover hacia adelante (escanear)
    // Velocidad Lenta
      stepperScanner.setMaxSpeed(velLenta);
      stepperScanner.move(pasosEnteros);
   }
   else {
    // Mover hacia atrás (retorno)
    // Velocidad Rapida
      stepperScanner.setMaxSpeed(velRapida);
      stepperScanner.move(-pasosEnteros); // Movimiento negativo para retroceder
   }

  // Bucle bloqueante: espera a que el motor termine de moverse
  while (stepperScanner.distanceToGo() != 0) {
    stepperScanner.run();
  }
}

// Funcion de homing del motor del escaner
void Homing() {

   // Velocidad y aceleración para el homing
   stepperScanner.setMaxSpeed(velLenta);
   stepperScanner.setAcceleration(acelScanner);

   // Mueve hacia atrás (negativo) una distancia muy grande
   stepperScanner.move(-1000000); 

   lastState = magnetico();

   while (homing == false) {
    // Mueve el motor
      stepperScanner.run(); 

      int currentState = magnetico();
      if (currentState != lastState && currentState != -1) {
         homing = true;
      }
   }

  // 1. Detener el motor (inicia la desaceleración)
  stepperScanner.stop();
  
  // 2. Ejecutar la rampa de desaceleración hasta parar
  while(stepperScanner.distanceToGo() != 0) {
    stepperScanner.run();
  }

  // 3. Establecer esta posición como el cero absoluto
   stepperScanner.setCurrentPosition(0);

   delay(1000);

  // 4. Mover 700 pasos hacia adelante desde el cero
   moverMotor(700, true);
}

// Funcion para sensar con el sensor magnetico
int magnetico() {
   int value = analogRead(sensorPin);
   if (value > 700) return 1;
   if (value < 50) return 0;
   return -1;
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

   stepperCinta.setMaxSpeed(3200.0);
   stepperCinta.setAcceleration(6000.0);

   int pasosCentrado = 0;
   bool enRango = false;

   // 1- Avanzar hasta detectar la pieza
   while (enRango == false) {
      moverCintaBloqueante(pasosPorMuestra);

      int distancia = medicion();
      if (distancia < 120) {
         enRango = true;
      }
   }

   // 2- Avanzar mientras se detecta la pieza
   while (enRango == true) {
      moverCintaBloqueante(muestrasSensado);

      pasosCentrado += muestrasSensado; // Acumula los pasos medidos

      int distancia = medicion();
      if (distancia > 120) {
         enRango = false;
      }
   }

   // 3- Retroceder para centrar
   if (pasosCentrado > 0) {
      // Calcula el retroceso total (la mitad de la pieza + un extra)
      long retrocesoTotal = (pasosCentrado / 2) + pasosExtra;

      // Mueve el total de pasos en sentido contrario
      moverCintaBloqueante(-retrocesoTotal);
   }
}

// Funcion para expulsar la pieza
void CintaSalida() {
   // Parámetros de aceleración para la cinta
   stepperCinta.setMaxSpeed(3200.0 / 2);
   stepperCinta.setAcceleration(6000.0 / 2);

   moverCintaBloqueante(pasosSalida);
}
