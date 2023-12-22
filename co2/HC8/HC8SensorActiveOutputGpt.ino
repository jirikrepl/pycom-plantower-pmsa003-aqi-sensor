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

// Define the size of the CO2 buffer in "element-seconds"
// The CO2 sensor sends data every second,
// and the CO2_BUFFER_SIZE determines the number of measurements stored.
// It is also used as the interval (in seconds) for printing the average value.
#define CO2_BUFFER_SIZE 60
unsigned long intervalPrintTime = CO2_BUFFER_SIZE * 1000UL;

// Initialize an array to store CO2 values
uint16_t co2Values[CO2_BUFFER_SIZE];
// Variable to keep track of the current index in the buffer
int co2Index = 0;
// Variable to keep track of the number of valid measurements in the buffer
int validMeasurements = 0;
// Variable to keep track of the last print time
unsigned long lastPrintTime = 0;

void setup() {
  // Start the serial communication with the CO2 sensor
  sensorSerial.begin(9600);
  Serial.begin(9600);  // You can change this baud rate based on your needs
}

void printAverage() {
  // Calculate the average of the valid CO2 values in the buffer
  uint32_t sum = 0;
  for (int i = 0; i < validMeasurements; i++) {
    sum += co2Values[i];
  }
  uint16_t average = static_cast<uint16_t>(sum / validMeasurements);

  // Print the average CO2 concentration
  Serial.print("Average CO2 Concentration: ");
  Serial.println(average);
}

void loop() {
  if (sensorSerial.available() >= DATA_PACKET_SIZE) {
    // Read the data packet from the CO2 sensor
    uint8_t dataPacket[DATA_PACKET_SIZE];
    sensorSerial.readBytes(dataPacket, DATA_PACKET_SIZE);

    // Check if the data packet has a valid header
    if (dataPacket[0] == 0x42 && dataPacket[1] == 0x4D) {
      // Extract CO2 concentration from the data packet
      uint16_t co2Concentration = (dataPacket[6] << 8) | dataPacket[7];

      // Verify the checksum
      uint8_t checksum = 0;
      for (int i = 0; i < DATA_PACKET_SIZE - 1; i++) {
        checksum += dataPacket[i];
      }

      if (checksum == dataPacket[DATA_PACKET_SIZE - 1]) {
        // Data is valid, store CO2 concentration in the buffer
        co2Values[co2Index] = co2Concentration;
        co2Index = (co2Index + 1) % CO2_BUFFER_SIZE;

        // Update the number of valid measurements in the buffer
        validMeasurements = min(validMeasurements + 1, CO2_BUFFER_SIZE);

        // Print CO2 concentration
        // Serial.print("CO2 Concentration: ");
        // Serial.println(co2Concentration);

        // Check if it's time to print the average
        if ((millis() - lastPrintTime >= intervalPrintTime) || (millis() < lastPrintTime)) {
          printAverage();
          lastPrintTime = millis();
        }
      } else {
        // Checksum error
        Serial.println("Checksum error!");
      }
    } else {
      // Invalid header
      Serial.println("Invalid data packet header!");
    }
  }
}
