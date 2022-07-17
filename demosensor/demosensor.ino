#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>


float temperature;
float humidity;

char server[] = "<Your Local IP>";
IPAddress ip(192, 168, 0, 177);

char ssid[] = "LoanDien"; // ten Wifi
char pass[] = "26122003"; // pass Wifi


//char ssid[] = "@tummm.19t"; // ten Wifi
//char pass[] = "04072000"; // pass Wifi


long last = 0;

void ConnectWiFi()
{
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connect WIFI!!!");
}

void dataSensor()
{
  temperature = (random(10, 30))/ 1.0;
  humidity = (random(50, 90))/ 1.0;
}

void setup()
{
  Serial.begin(9600);
  ConnectWiFi();
}
//------------------------------------------------------------------------------

/* Infinite Loop */
void loop()
{
  if (WiFi.status() == WL_CONNECTED) // kierm tra wifi con ket noi k
  {
    //    if (millis() - last > 500) // 500ms = 0.5s // cu moi 0.5s update 1 lan
    //    {
    //      dataSensor();
    //      Send_Data_PHP(String(temperature), String(humidity));
    //      last = millis();
    //    }


    dataSensor();
    Send_Data_PHP(String(temperature), String(humidity));
    last = millis();
    delay(2000);
  }
}

void Send_Data_PHP(String temperature, String humidity)
{
  HTTPClient http;
  WiFiClient client1;
  
  String c1 = "http://192.168.55.110/demosensor/data1.php?temperature=";
  c1 += String(temperature);
  String c3 = "&humidity=";
  c1 += String(c3);
  c1 += String(humidity);
  Serial.println(c1);
  
  http.begin(client1, c1); // params có webClient Client
  //http.begin(client1,"http://toannv10291.000webhostapp.com/ESPinsertdatabase.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  String httpRequestData = "temperature=" + String(temperature) + "&humidity=" + String(humidity) + "";
  Serial.println(httpRequestData);
  int httpResponseCode = http.POST(httpRequestData);
  //Serial.println(httpResponseCode);

  if (httpResponseCode == 200)
  {
    Serial.print("Send Data Thành Công:");
    Serial.println(httpRequestData);
    delay(200);
  }
  else
  {
    Serial.println("Không gửi dữ liệu được!!!");
  }
  http.end();
  //=================================================================================
}
