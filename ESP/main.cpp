#include <WiFi.h>
#include <HTTPClient.h>
#include <LiquidCrystal_I2C.h>

// Configuración WiFi
const char* ssid = "Lab. Telematica";
const char* password = "l4bt3l3m4tic@";

// Configuración del caudalímetro
const int flowPin = 4; // Pin conectado al caudalímetro
// Variables para el caudalímetro
volatile uint16_t pulseCount = 0;
float flowRate = 0.0;
unsigned long oldTime = 0;
float totalLiters = 0.0;  // Variable global para el total de litros medidos

// Configuración del relé
const int relayPin = 5;
volatile bool flowDetected = false;
WiFiClientSecure client;
// Prototipos
void IRAM_ATTR pulseCounter();
void measurementTask(void *pvParameters);
void thresholdControlTask(void *pvParameters);

// Conversión de pulsos a volumen
float calculateVolume(int pulses) {
    const float calibrationFactor = 7.5; // Ajustar según el caudalímetro
    return (pulses / calibrationFactor); // Litros
}

// HTTP POST
void sendData(float volume) {
    HTTPClient http;
    http.begin("http://192.168.169.25:8011/insert_flujo_agua"); // Cambia la URL
    http.addHeader("Content-Type", "application/json");

    // Construcción del JSON correctamente formateado
    String payload = "{\"ID_esp\":1,\"Cantidad_agua\":" + String(volume, 2) + "}";
    Serial.println("Payload enviado: " + payload);

    int httpResponseCode = http.POST(payload);
    if (httpResponseCode > 0) {
        Serial.println("Código de respuesta HTTP: " + String(httpResponseCode));
        Serial.println("Respuesta del servidor: " + http.getString());
    } else {
        Serial.println("Error en la solicitud POST: " + http.errorToString(httpResponseCode));
    }
    http.end();
}

void calculateFlowRate() {
  if ((millis() - oldTime) >= 1000) { // Cada segundo
    oldTime = millis();

    // Desactivar interrupciones mientras se lee pulseCount
    noInterrupts();
    uint16_t pulses = pulseCount;
    pulseCount = 0;
    interrupts();

    // Calcular el caudal en L/min
    flowRate = ((float)pulses) / 440;

    // Añadir a los litros totales (flowRate está en L/min, convertir a litros por segundo)
    totalLiters += (flowRate / 60);

    Serial.print("Caudal: ");
    Serial.print(flowRate);
    Serial.print(" L/min, Litros totales: ");
    Serial.println(totalLiters);
  }
}
// HTTP GET PARA LEER ESTADO 
bool getThresholdStatus() {
    HTTPClient http;
    http.begin("http://192.168.169.25:8011/estado_umbral/1"); // Cambia la URL
    int httpResponseCode = http.GET();
    if (httpResponseCode == 200) {
        String response = http.getString();
        http.end();
        return response == "true";
    }
    http.end();
    return false;
}
// Tarea para calcular el caudal
void calculateFlowRateTask(void *pvParameters) {
  while (true) {
    calculateFlowRate();
    vTaskDelay(2000 / portTICK_PERIOD_MS); // Ejecutar cada 1 segundo
  }
}
void enviarLitrosAlServidorTask(void *pvParameters) {
  while (true) {
    sendData(totalLiters);
    vTaskDelay(5000 / portTICK_PERIOD_MS); // Envía los datos cada 60 segundos
  }
}

// Manejo de interrupciones
void IRAM_ATTR pulseCounter() {
    pulseCount++;
    flowDetected = true;
}
// Configuración inicial
void setup() {
    Serial.begin(115200);
    // Configuración de pines
    pinMode(flowPin, INPUT_PULLUP);
    attachInterrupt(flowPin,pulseCounter, RISING);
    pinMode(relayPin, OUTPUT);
    digitalWrite(relayPin, LOW);

    

    // Conexión WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        Serial.println("Tratando de conectar a red Wifi");
        delay(1000);
    }
    Serial.println("Se conectó al Wifi");
    // Configuración de interrupciones
    // Crear tareas
    // xTaskCreate(measurementTask, "Measurement Task", 2048, NULL, 1, NULL);
    //xTaskCreate(thresholdControlTask, "Threshold Control Task", 2048, NULL, 1, NULL);
    xTaskCreate(calculateFlowRateTask, "Calcular Caudal", 2048, NULL, 1, NULL);
    xTaskCreate(enviarLitrosAlServidorTask, "Enviar Litros al Servidor", 8192, NULL, 1, NULL);
    // Deep Sleep inicial
    //ESP.deepSleep(0);
}

void loop() {
    
}

