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
int maxAttempts = 20;  // Augmentez le nombre d'essais
while (WiFi.status() != WL_CONNECTED && maxAttempts-- > 0) {
  delay(500);
  Serial.print(".");
}
if (WiFi.status() == WL_CONNECTED) {
  Serial.println("\nConnecté au WiFi !");
  Serial.print("Adresse IP : ");
  Serial.println(WiFi.localIP());
} else {
  Serial.println("Impossible de se connecter au WiFi !");
  return;
}
}

void loop() {
  // Envoyer la température toutes les 10 secondes
  envoyerTemperature();
  delay(10000);  // Attendre 10 secondes avant la prochaine mesure
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

    String endpoint = String(SERVER_IP) + "/Mesure";  // Endpoint Flask pour ajouter une mesure
    http.begin(client, endpoint);
    http.addHeader("Content-Type", "application/json");

    // Créer une chaîne JSON avec la température
    String jsonData = "{\"CAPTEUR_ID\": 5, \"valeur\":" + String(temperature) + "}";
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
