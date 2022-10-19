#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"
#include <iostream>
#include <cstdlib>
#include <Arduino_LSM6DSOX.h>
#include <Servo.h> 




#define SEALEVELPRESSURE_HPA (1014)
int Mili = 0;
int MISSION_TIME = 0;
String PL_STATE = "";
String SW_STATE = "";
String Packet;
int count=0;

Adafruit_BMP3XX bmp;

// Declare the Servo pin 
int servoPin = 16; 
// Create a servo object 
Servo Servo1; 





void setup() {

  // buzzer, led, and file
  pinMode(22, OUTPUT);
  pinMode(20, OUTPUT);
  Serial1.begin(9600);
  Serial1.print("new ");
  Serial1.println("test.csv"); // change for official
  Serial1.print("append ");
  Serial1.print("test.csv"); // change for official
  Serial1.write(13);

// We need to attach the servo to the used pin number 
   Servo1.attach(servoPin); 

  if (!IMU.begin()) {
    Serial1.println("Failed to initialize IMU!");
 }
bmp.begin_I2C(); 

  // Set up oversampling and filter initialization;
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);
}




void loop() {

// timer
Mili = millis();
MISSION_TIME = Mili/1000;


// BMP388 setup
  if (! bmp.performReading()) {
    Serial1.println("Failed to perform reading");
  }



// IMU
  float x, y, z;

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x,y,z);
  }

  if (IMU.temperatureAvailable()){
    int temperature_deg = 0;
    IMU.readTemperature(temperature_deg);}

 float x2, y2, z2;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x2, y2, z2);
  }



// voltage
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue * (5.0 / 1023.0);



// formating and receiving data/states
  while ((bmp.readAltitude(SEALEVELPRESSURE_HPA)<= 400) and (SW_STATE != "DESCENDING")){
    PL_STATE = "N";
    
    if (bmp.readAltitude(SEALEVELPRESSURE_HPA)< 5) {
      SW_STATE = "AWAITING_LAUNCH";
      digitalWrite(22, HIGH);  // turn the LED on (HIGH is the voltage level)
      delay(3000);                      // wait for three seconds
      digitalWrite(22, LOW);   // turn the LED off by making the voltage LOW
      delay(3000);  
      }
      
    if ((bmp.readAltitude(SEALEVELPRESSURE_HPA) > 5) and (bmp.readAltitude(SEALEVELPRESSURE_HPA) < 400)){
      SW_STATE = "ASCENDING";
      digitalWrite(22, HIGH);
      delay(1500);              // wait for one and a half seconds
      digitalWrite(22, LOW);   // turn the LED off by making the voltage LOW
      delay(1500);  
      }
      
    if (bmp.readAltitude(SEALEVELPRESSURE_HPA) >= 400){
      SW_STATE = "DESCENDING";      
      digitalWrite(22, HIGH);
      delay(2000);             // wait for two seconds
      digitalWrite(22, LOW);   // turn the LED off by making the voltage LOW
      delay(2000);
      // Make servo go to 120 degrees 
      Servo1.write(0);
      delay(1000)
      Servo1.write(120); 
      delay(1000)
      Servo1.write(0);
      delay(1000)
      Servo1.write(120);  
    }
      
    // 1005,MISSION_TIME,PACKET_COUNT,SW_STATE,PL_STATE,ALTITUDE,TEMP,VOLTAGE,GYRO_R,GYRO_P,GYRO_Y;
    count++;
    Packet = String(1005) + String(",") + String(count) + String(",") + String(SW_STATE) + String(",") + String(PL_STATE) + String(",") + String(bmp.readAltitude(SEALEVELPRESSURE_HPA)) + String(",") + String(bmp.temperature) + String(",") + String(voltage) + String(",") + String(x) + String(",") + String(y) + String(",") + String(z);

    
    Serial1.print(Packet);
    }

SW_STATE = "DESCENDING"; //in case we need it

 while (SW_STATE = "DESCENDING") and ((bmp.readAltitude(SEALEVELPRESSURE_HPA)>= 400)) {
  // check message from houston
  
 }



  while ((bmp.readAltitude(SEALEVELPRESSURE_HPA) <= 400) and (SW_STATE == "DESCENDING")){
    PL_STATE = "P";
    digitalWrite(22, HIGH);
    delay(2000);             // wait for two seconds
    digitalWrite(22, LOW);   // turn the LED off by making the voltage LOW
    delay(2000);  
   
    if (bmp.readAltitude(SEALEVELPRESSURE_HPA) < 5){
      SW_STATE = "LANDED"; 
      digitalWrite(22, HIGH);
      delay(1000);             // wait for two seconds
      digitalWrite(22, LOW);   // turn the LED off by making the voltage LOW
      delay(1000);  
        }
      
        
    // 1005,MISSION_TIME,PACKET_COUNT,SW_STATE,PL_STATE,ALTITUDE,TEMP,VOLTAGE,GYRO_R,GYRO_P,GYRO_Y;
    count++;
    Packet = String(1005) + String(",") + String(count) + String(",") + String(SW_STATE) + String(",") + String(PL_STATE) + String(",") + String(bmp.readAltitude(SEALEVELPRESSURE_HPA)) + String(",") + String(bmp.temperature) + String(",") + String(voltage) + String(",") + String(x) + String(",") + String(y) + String(",") + String(z);
  
    
    Serial1.print(Packet);
      }


  while (SW_STATE == "LANDED") {
     digitalWrite(22, HIGH);
     delay(1000);                      // wait for two seconds
     digitalWrite(22, LOW);   // turn the LED off by making the voltage LOW
     delay(1000); 
     //BUZZER
     digitalWrite(20, HIGH);  
    }
  }
