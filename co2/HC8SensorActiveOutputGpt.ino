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

// Define the CO2 sensor serial interface
SoftwareSerial sensorSerial(2, 3);  // RX, TX

// Define the number of bytes in a data packet
#define DATA_PACKET_SIZE 16

void setup() {
  // Start the serial communication with the CO2 sensor
  sensorSerial.begin(9600);
  Serial.begin(9600);  // You can change this baud rate based on your needs

  Serial.println("CO2 Sensor Communication Debug");
}

void loop() {
  if (sensorSerial.available() >= DATA_PACKET_SIZE) {
    // Read the data packet from the CO2 sensor
    uint8_t dataPacket[DATA_PACKET_SIZE];
    sensorSerial.readBytes(dataPacket, DATA_PACKET_SIZE);

    Serial.print("Received Data Packet: ");
    for (int i = 0; i < DATA_PACKET_SIZE; i++) {
      Serial.print(dataPacket[i], HEX);
      Serial.print(" ");
    }
    Serial.println();

    // Check if the data packet has a valid header
    if (dataPacket[0] == 0x42 && dataPacket[1] == 0x4D) {
      // Extract CO2 concentration from the data packet
      uint16_t co2Concentration = (dataPacket[6] << 8) | dataPacket[7];

      // Verify the checksum
      uint8_t checksum = 0;
      for (int i = 0; i < DATA_PACKET_SIZE - 1; i++) {
        checksum += dataPacket[i];
      }

      Serial.print("Checksum Calculated: ");
      Serial.println(checksum, HEX);
      Serial.print("Checksum Received: ");
      Serial.println(dataPacket[DATA_PACKET_SIZE - 1], HEX);

      if (checksum == dataPacket[DATA_PACKET_SIZE - 1]) {
        // Data is valid, print CO2 concentration
        Serial.print("CO2 Concentration: ");
        Serial.println(co2Concentration);
      } else {
        // Checksum error
        Serial.println("Checksum error!");
      }
    } else {
      // Invalid header
      Serial.println("Invalid data packet header!");
    }

    Serial.println();
  }
}
