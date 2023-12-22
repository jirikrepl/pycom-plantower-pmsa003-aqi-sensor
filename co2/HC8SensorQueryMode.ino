#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX

void setup() {
  Serial.begin(9600);  // This is the default hardware serial port on Arduino Uno
  mySerial.begin(9600);  // Initialize SoftwareSerial
  delay(1000);
  Serial.println("Setup completed.");
}

void loop() {
  Serial.println("Sending request to MH-Z19...");

  // Request CO2 concentration
  uint8_t requestBytes[] = {0x64, 0x69, 0x03, 0x5E, 0x4E};
  mySerial.write(requestBytes, sizeof(requestBytes));

  // Wait for the response (minimum 14 bytes)
  Serial.println("Waiting for the response...");
  delay(100);
  while (mySerial.available() < 14);

  Serial.println("Response received.");

  // Read and interpret the response
  uint8_t firstByte = mySerial.read();
  uint8_t secondByte = mySerial.read();

  // Debug print received bytes
  Serial.print("First Byte: 0x");
  Serial.println(firstByte, HEX);
  Serial.print("Second Byte: 0x");
  Serial.println(secondByte, HEX);

  if (firstByte == 0x64 && secondByte == 0x69) {
    // If header is correct, skip the next two bytes
    mySerial.read(); // Discard third byte
    mySerial.read(); // Discard fourth byte

    int high = mySerial.read();
    int low = mySerial.read();
    int co2Value = low * 256 + high;
    // int co2Value = high * 256 + low;

    // Debug print received values
    Serial.print("High byte: ");
    Serial.println(high);
    Serial.print("Low byte: ");
    Serial.println(low);

    // Display CO2 concentration
    Serial.print("CO2 Concentration: ");
    Serial.print(co2Value);
    Serial.println(" ppm\n");

    // Discard 8 bytes
    byte discardBuffer[8];
    mySerial.readBytes(discardBuffer, 8);
  } else {
    Serial.println("Unexpected response. Skipping interpretation.");
  }

  delay(5000);  // Delay for better readability in the Serial Monitor
}
