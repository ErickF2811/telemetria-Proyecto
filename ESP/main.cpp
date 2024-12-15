#include <ESP8266WiFi.h>
#include <HTTPClient.h>
#include <FreeRTOS.h>
#include <liquidcrystal_i2c.h>

// Configuración WiFi
const char* ssid = "Econtel_Ecuador";
const char* password = "Platon31053105";

// Configuración del caudalímetro
const int flowPin = D2; // Pin conectado al caudalímetro
volatile int pulseCount = 0;

// Configuración del relé
const int relayPin = D1;

// SERVIDOR NTP 
const char* ntpServer = "1.south-america.pool.ntp.org";
// Variables compartidas
volatile bool flowDetected = false;

// Prototipos
void IRAM_ATTR pulseCounter();
void measurementTask(void *pvParameters);
void thresholdControlTask(void *pvParameters);

// Conversión de pulsos a volumen
float calculateVolume(int pulses) {
    const float calibrationFactor = 7.5; // Ajustar según el caudalímetro
    return (pulses / calibrationFactor); // Litros
}
// Función para obtener la hora local
void printLocalTime()
{
  struct tm timeinfo;
  int retryCount = 0;
  while (!getLocalTime(&timeinfo) && retryCount < 5) {  // Reintentar hasta 5 veces
    Serial.println("Failed to obtain time, retrying...");
    delay(2000);
    retryCount++;
  }
  if(retryCount == 5) {
    Serial.println("Could not obtain time after several attempts");
    return;
  }
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
}
// MOSTRAR EN LCD 16X2
void mostrarEnLCD() {
  lcd.clear();
  // Mostrar Litros Diarios en la primera línea LCD
  lcd.setCursor(0, 0);
  lcd.print("Litros Diarios: " + String(totalLiters));
  delay(2000); // Esperar 2 segundos
  lcd.clear();
}

// HTTP POST
void sendData(float volume) {
    HTTPClient http;
    http.begin("http://192.168.1.100:8080/insert_flujo_agua"); // Cambia la URL
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"volume\":" + String(volume) + "}";
    int httpResponseCode = http.POST(payload);
    http.end();
}

// HTTP GET PARA LEER ESTADO 
bool getThresholdStatus() {
    HTTPClient http;
    http.begin("http://192.168.1.100:8080/estado_umbral/1"); // Cambia la URL
    int httpResponseCode = http.GET();
    if (httpResponseCode == 200) {
        String response = http.getString();
        http.end();
        return response == "true";
    }
    http.end();
    return false;
}

// Configuración inicial
void setup() {
    // Configuración de pines
    pinMode(flowPin, INPUT_PULLUP);
    pinMode(relayPin, OUTPUT);
    digitalWrite(relayPin, LOW);

    // Configuración de interrupciones
    attachInterrupt(digitalPinToInterrupt(flowPin), pulseCounter, RISING);

    // Conexión WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
    }

    // Crear tareas
    xTaskCreate(measurementTask, "Measurement Task", 2048, NULL, 1, NULL);
    xTaskCreate(thresholdControlTask, "Threshold Control Task", 2048, NULL, 1, NULL);

    // Deep Sleep inicial
    ESP.deepSleep(0);
}

void loop() {
    // Empty, manejado por RTOS
}

// Tarea de medición
void measurementTask(void *pvParameters) {
    while (true) {
        if (flowDetected) {
            detachInterrupt(digitalPinToInterrupt(flowPin));

            // Medir pulsos por un periodo
            int pulses = pulseCount;
            pulseCount = 0;
            flowDetected = false;

            // Obtener volumen
            float volume = calculateVolume(pulses);

            // Enviar datos por HTTP POST
            sendData(volume);

            attachInterrupt(digitalPinToInterrupt(flowPin), pulseCounter, RISING);

            // Entrar a Deep Sleep
            ESP.deepSleep(0);
        }
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

// Tarea de control de umbral
void thresholdControlTask(void *pvParameters) {
    while (true) {
        bool thresholdReached = getThresholdStatus();
        digitalWrite(relayPin, thresholdReached ? LOW : HIGH);

        // Esperar antes de deep sleep
        if (!flowDetected) {
            ESP.deepSleep(60000000); // 1 minuto
        }
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}

// Manejo de interrupciones
void IRAM_ATTR pulseCounter() {
    pulseCount++;
    flowDetected = true;
}
