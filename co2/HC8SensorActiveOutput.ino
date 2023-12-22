/**
  Data format in "active output" mode:

  The output format is 16BYTE.
  Data header: BYTE0 = 0X42; BYTE1=4D
  BYTE6 data is high, BYTE7 data is low, indicating CO2 concentration.
  BYTE15, data checksum. BYTE15= BYTE0+BYTE1+…….+BYTE13;

  Example: 42 4D 0C 51 09 A2 07 2B 01 35 05 81 20 08 20 AD;
  CO2 concentration = BYTE6 X 256 + BYTE7 = 07X256 + 2B = 1853;
**/

#include <SoftwareSerial.h>

SoftwareSerial sensorSerial(2, 3); // RX, TX

void setup() {
  Serial.begin(9600);  // Default hardware serial port on Arduino Uno
  sensorSerial.begin(9600);  // CO2 sensor serial
  delay(1000);
  Serial.println("Setup completed.");
}

void loop() {
  // header bytes
  uint8_t firstByte = 0xFF;
  uint8_t secondByte = 0xFF;

  while (firstByte != 0x42 && secondByte != 0x4D) {
    firstByte = sensorSerial.read();
    secondByte = sensorSerial.read();
    // Serial.print("First Byte: 0x");
    // Serial.println(firstByte, HEX);
    // Serial.print("Second Byte: 0x");
    // Serial.println(secondByte, HEX);
  }

  // If header is correct, skip the next four bytes
  byte discardBuffer[4];
  sensorSerial.readBytes(discardBuffer, 4);

  int high = sensorSerial.read();
  int low = sensorSerial.read();
  int co2Value = high * 256 + low;

  Serial.print("CO2 Concentration: ");
  Serial.print(co2Value);
  Serial.println(" ppm\n");

  delay(5000);
}
