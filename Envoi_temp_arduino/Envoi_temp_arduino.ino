#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// Configuration des pins et des capteurs
#define DHTPIN 5         // Pin où le DHT11 est connecté
#define DHTTYPE DHT11    // Type de capteur DHT
DHT dht(DHTPIN, DHTTYPE);

// Configuration WiFi
#define WIFI_SSID "HUAWEI_de_piere"          // Remplacez par votre SSID
#define WIFI_PASSWORD "sekilasekila"  // Remplacez par votre mot de passe

// Adresse IP du serveur Flask
#define SERVER_IP "http://192.168.43.235:5000"  // Remplacez par l'adresse IP de votre serveur

void setup() {
  // Initialisation série et DHT
  Serial.begin(115200);
  dht.begin();

  // Connexion au WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.println("Connexion au WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnecté au WiFi !");
  Serial.print("Adresse IP : ");
  Serial.println(WiFi.localIP());

  // Tester GET
  testGET();

  // Tester POST avec une valeur simulée
  testPOST();
}

void loop() {
  // Envoyer la température toutes les 10 secondes
  envoyerTemperature();
  delay(10000);  // Attendre 10 secondes avant la prochaine mesure
}

// Fonction pour tester une requête GET
void testGET() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    http.begin(client, String(SERVER_IP) + "/test");  // URL pour GET
    int httpCode = http.GET();

    if (httpCode > 0) {
      Serial.printf("Code HTTP GET : %d\n", httpCode);
      String payload = http.getString();
      Serial.println("Réponse du serveur : " + payload);
    } else {
      Serial.printf("Erreur lors de la requête GET : %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }
}

// Fonction pour tester une requête POST
void testPOST() {
  if (WiFi.status() == WL_CONNECTED) {
    float temperature = 25.0;  // Température simulée pour le test
    WiFiClient client;
    HTTPClient http;

    http.begin(client, String(SERVER_IP) + "/test");  // URL pour POST
    http.addHeader("Content-Type", "application/json");

    // Créer une chaîne JSON
    String jsonData = "{\"temperature\":" + String(temperature) + "}";
    int httpCode = http.POST(jsonData);

    if (httpCode > 0) {
      Serial.printf("Code HTTP POST : %d\n", httpCode);
      String payload = http.getString();
      Serial.println("Réponse du serveur : " + payload);
    } else {
      Serial.printf("Erreur lors de la requête POST : %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }
}

// Fonction pour envoyer la température réelle
void envoyerTemperature() {
  if (WiFi.status() == WL_CONNECTED) {
    float temperature = dht.readTemperature();  // Lecture de la température

    if (isnan(temperature)) {
      Serial.println("Erreur de lecture du capteur !");
      return;
    }

    WiFiClient client;
    HTTPClient http;

    http.begin(client, String(SERVER_IP) + "/test");  // URL pour POST
    http.addHeader("Content-Type", "application/json");

    // Créer une chaîne JSON avec la température
    String jsonData = "{\"temperature\":" + String(temperature) + "}";
    int httpCode = http.POST(jsonData);

    if (httpCode > 0) {
      Serial.printf("Code HTTP POST : %d\n", httpCode);
      String payload = http.getString();
      Serial.println("Réponse du serveur : " + payload);
    } else {
      Serial.printf("Erreur lors de la requête POST : %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }
}
