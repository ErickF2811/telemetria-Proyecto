#include <Arduino.h> // Añadimos esta línea
#include <WiFi.h>

const byte pinCaudalimetro = 4; // Pin D4 en la ESP32

volatile uint32_t contadorPulsos = 0;
unsigned long tiempoAnterior = 0;
float factorCalibracion = 7.5; // Ajusta este valor según las especificaciones del SF201
float totalLitros = 0.0; // Variable para almacenar el total de litros

void IRAM_ATTR contadorPulsosISR() {
  contadorPulsos++;
}

void setup() {
  Serial.begin(115200);
   
  pinMode(pinCaudalimetro, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinCaudalimetro), contadorPulsosISR, FALLING);
}

void loop() {
  if ((millis() - tiempoAnterior) > 1000) { // Cada 1 segundo
    detachInterrupt(pinCaudalimetro);

    // Calcula el caudal en L/min
    float caudalLPM = ((float)contadorPulsos / factorCalibracion);

    // Calcula el volumen en litros durante el intervalo de tiempo (1 segundo)
    float litrosEnIntervalo = (caudalLPM / 60.0); // Convertimos de L/min a L/segundo

    // Acumula el volumen total
    totalLitros += litrosEnIntervalo;

    Serial.print("Caudal: ");
    Serial.print(caudalLPM);
    Serial.print(" L/min, Total Litros: ");
    Serial.println(totalLitros);

    contadorPulsos = 0;
    tiempoAnterior = millis();

    attachInterrupt(digitalPinToInterrupt(pinCaudalimetro), contadorPulsosISR, FALLING);
  }
}