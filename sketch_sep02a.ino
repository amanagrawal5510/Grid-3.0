#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>

#define ENA   14          // Enable/speed motors Right        GPIO14(D5)
#define ENB   12          // Enable/speed motors Left         GPIO12(D6)
#define IN_1  15          // L298N in1 motors Right           GPIO15(D8)
#define IN_2  13          // L298N in2 motors Right           GPIO13(D7)
#define IN_3  2           // L298N in3 motors Left            GPIO2(D4)
#define IN_4  0           // L298N in4 motors Left            GPIO0(D3)

int speedCar = 0;

char* ssid = "garg";
char* password = "Gargrewa123";

const uint16_t port = 8080;           // Port used in python code ... 8090 ig
char * host = "192.168.29.119";  //your laptop IP

WiFiClient client;

byte b = -1;  // Command
byte opc = 0; // opcode
byte val = 0; // Value



void setup()
{
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(IN_3, OUTPUT);
  pinMode(IN_4, OUTPUT);
  Serial.begin(115200);

    digitalWrite(IN_1, LOW);
  digitalWrite(IN_2, LOW);
    analogWrite(ENA, 0);

  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, LOW);
       analogWrite(ENB, 0);

  WiFi.begin(ssid, password);
  // Waiting for connection
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("...");
  }

  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

  while (!client.connect(host, port))
  {
    Serial.println("Connection to host failed");
    delay(500);
  }
  Serial.println("Connected to server successful!");
  client.print("Bot 1 connected");
  delay(500);
}

void goAhead() {

  digitalWrite(IN_1, LOW);
  digitalWrite(IN_2, HIGH);
    analogWrite(ENA, speedCar);

  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, HIGH);
       analogWrite(ENB, speedCar);
}

void goBack() {

  digitalWrite(IN_1, HIGH);
  digitalWrite(IN_2, LOW);
        analogWrite(ENA, speedCar);

  digitalWrite(IN_3, HIGH);
  digitalWrite(IN_4, LOW);
        analogWrite(ENB, speedCar);
}

int flag1 = 1, flag2 = 1, flag3 = 1, sp = -1, dir = -1;
void loop()
{
  //  //Countinuously listens for any byte recieved
  //  while(b == 255)
  while (sp == -1)
    sp = client.read();
  while (dir == -1)
    dir = client.read();
  if (flag1) {
    Serial.println(sp);
    Serial.println(dir);
    flag1 = 0;
  }

  if (dir == 0) {
    speedCar = sp ;
    goAhead();
    if (flag3) {
      Serial.println("Moving forward");
      Serial.println(sp);
      Serial.println(dir);
      //    flag3=0;
    }
  }
  if (dir == 63) {
    speedCar = sp;
    goBack();
    if (flag2) {
      Serial.println("Moving backward");
      Serial.println(sp);
      Serial.println(dir);
      //    flag2=0;
    }
  }
  sp = -1;
  dir = -1;
}
