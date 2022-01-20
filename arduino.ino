#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <Servo.h>
#include <WiFiClient.h>

#define ENA   14          // Enable/speed motors Right
#define ENB   12          // Enable/speed motors Left
#define IN_1  15          // L298N in1 motors Right
#define IN_2  13          // L298N in2 motors Right
#define IN_3  4           // L298N in3 motors Left
#define IN_4  5           // L298N in4 motors Left
#define ARM   2

int speedCar = 0;
int dir=0;

WiFiClient client;
char* ssid = "garg";
char* password = "Gargrewa123";
const uint16_t port = 8001;       // Port used in python code ... 8090 ig
char * host = "192.168.29.119";   //your laptop IP

Servo arm;
int servo_def = 0;        // Default Angle
int servo_throw = 100;    // Throw Angle
int servo_delay = 1000;   // Throw Time


void setup()
{
  Serial.begin(115200);

  arm.attach(ARM);
  arm.write(servo_def);
  
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(IN_3, OUTPUT);
  pinMode(IN_4, OUTPUT);

  digitalWrite(IN_1, LOW);
  digitalWrite(IN_2, LOW);
  analogWrite(ENA, 0);

  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, LOW);
  analogWrite(ENB, 0);

  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("...");
  }

  Serial.print("My IP: ");
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

void Throw()
{
  arm.write(servo_throw);
  delay(servo_delay);
  arm.write(servo_def);
}

void change_dir()
{
  if(dir>0 && dir<=63)          //forward left
  {
    digitalWrite(IN_1, LOW);    //right motor forward
    digitalWrite(IN_2, HIGH);
    //analogWrite(ENA, speedCar);

    digitalWrite(IN_3, LOW);    // left motor forward
    digitalWrite(IN_4, HIGH);
    int x = (speedCar/63)*dir;
    analogWrite(ENB, speedCar-x);
  }
  
  if(dir>63 && dir<=127)        //bakward right
  {
    digitalWrite(IN_1, HIGH);   //right motor backward
    digitalWrite(IN_2, LOW);
   
    digitalWrite(IN_3, HIGH);   //left motor backward
    digitalWrite(IN_4, LOW);
    int x = (speedCar/127)*dir;
    analogWrite(ENB, speedCar-x);
  }
  
  if(dir >127 && dir<=190)      //backward left
  {

    digitalWrite(IN_1, HIGH);   // right motor backward
    digitalWrite(IN_2, LOW);
    int x = (speedCar/190)*dir;
    analogWrite(ENA, speedCar-x);

    digitalWrite(IN_3, HIGH);   // left motor backward
    digitalWrite(IN_4, LOW);
  }

  if(dir>190 && dir<=254)       //forward right
  {
     digitalWrite(IN_1, LOW);   //right motor forward
     digitalWrite(IN_2, HIGH);
     int x = (speedCar/254)*dir;
     analogWrite(ENA, speedCar-x);
    
     digitalWrite(IN_3, LOW);   // left motor forward
     digitalWrite(IN_4, HIGH);
  }
}


int flag1 = 1, flag2 = 1, flag3 = 1, sp = -1, direction = -1;

void loop()
{
  //Countinuously listens for 2 byte from socket server
  while (sp == -1)sp = client.read();
  while (direction == -1)direction = client.read();
  
  if (flag1)
  {
    Serial.println(sp);
    Serial.println(dir);
    flag1 = 0;
  }
  
  dir = direction;
  speedCar= sp;
  
  if(sp < 201)
    change_dir();
  else
    Throw();
    
  sp = -1;
  direction = -1;
}
