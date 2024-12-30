#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>



// Configuration des pins et des capteurs
#define DHTTYPE DHT11    // Type de capteur DHT
#define DHTPIN 5         // Pin où le DHT11 est connecté
DHT dht(DHTPIN, DHTTYPE);

// Configuration WiFi
//SSID et mdp
#define WIFI_SSID "HUAWEI_de_piere"          
#define WIFI_PASSWORD "sekilasekila"         

// Adresse IP du serveur Flask chez moi
#define SERVER_IP "http://192.168.43.235:5000"    //cmd: ipconfig (Windows) 






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
}



void loop()
{
  envoyerDonnees();
  delay(10000);  // prend des mesures toutes les 10 secondes
}




void envoyerDonnees()
{
  if (WiFi.status() == WL_CONNECTED) {
    float temperature = dht.readTemperature();  // Lecture de la température
    float humidite = dht.readHumidity();        // Lecture de l'humidité

    if (isnan(temperature) || isnan(humidite)) {
      Serial.println("Erreur de lecture du capteur !");
      return;
    }

    WiFiClient client;
    HTTPClient http;

    // Envoyer la température
    http.begin(client, String(SERVER_IP) + "/Mesure");
    http.addHeader("Content-Type", "application/json");
    String jsonTemp = "{\"CAPTEUR_ID\": 5, \"valeur\":" + String(temperature) + "}";
    int httpCodeTemp = http.POST(jsonTemp);
    if (httpCodeTemp > 0) {
      Serial.printf("Code HTTP POST Température : %d\n", httpCodeTemp);
    }
    http.end();

    // Envoyer l'humidité
    http.begin(client, String(SERVER_IP) + "/Mesure");
    http.addHeader("Content-Type", "application/json");
    String jsonHum = "{\"CAPTEUR_ID\": 6, \"valeur\":" + String(humidite) + "}";
    int httpCodeHum = http.POST(jsonHum);
    if (httpCodeHum > 0) {
      Serial.printf("Code HTTP POST Humidité : %d\n", httpCodeHum);
    }
    http.end();
  }
}

