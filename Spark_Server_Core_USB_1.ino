
#include "BluetoothSerial.h" //Header File for Serial Bluetooth, will be added by default into Arduino
#include <M5Core2.h>

BluetoothSerial SerialBT; //Object for Bluetooth

byte bt_byte, usb_byte;

#define SPARK_BT_NAME "Spark 40 Audio"

void setup() {
  M5.begin();

//  Serial.begin(115200); 

  M5.Lcd.setBrightness(100);
  M5.Lcd.setTextColor(WHITE);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(0, 0);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.println(">Spark Spoofer Core2 USB1<");
  M5.Lcd.println("                          ");  
  
  M5.Lcd.print("Starting BT..");
  if (!SerialBT.begin(SPARK_BT_NAME)) 
  {
    M5.Lcd.println("failed"); 
    while (true) {};
  }
  M5.Lcd.println("ready to pair");
}

void loop() {
  if (SerialBT.available()) //Check if we receive anything from Bluetooth
  {
    usb_byte = SerialBT.read(); //Read what we recevive 
    Serial.write(usb_byte);

  };
  
  if (Serial.available())
  {
    bt_byte = Serial.read();
    SerialBT.write(bt_byte);
  }
}
