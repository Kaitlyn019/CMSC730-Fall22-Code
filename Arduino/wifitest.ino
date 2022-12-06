#include <WiFi.h>
#include "IMU__WiFi.h"
#include "MPU-9250.h"
#include <Wire.h>
#include "imu.h"
#include <time.h> 


const char* ssid = "umd-iot";
const char* password = "s27ntkrkt7b9";


WiFiClient client;
const uint16_t port = 8090;
const char * host = "10.3.29.246";

//const uint8_t sda = 21;
//const uint8_t scl = 22;
const uint16_t polling_rate_hz = 100;

//MPU9250 imu = MPU9250(sda, scl);

imu_wifi_packet_t packet;

void setup(){
    Serial.begin(115200);
    delay(1000);

    Serial.print("ESP Board MAC Address:  ");
    Serial.println(WiFi.macAddress());

    //imu.begin();
    
    imu_setup();

    // 78:E3:6D:65:4A:24

    WiFi.mode(WIFI_STA); //Optional
    WiFi.begin(ssid, password);
    Serial.println("\nConnecting");

    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(100);
    }

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
}

void loop(){
    // packet = generate_test_packet();
    
    for (int i = 0; i < MAX_IMU_READINGS; i++) {
      get_imu_reading(&packet.readings[i]);
      // get_next_imu_reading(imu, &packet.readings[i]);
      delay(100);
    }

    Serial.println(sizeof(packet));
    if (!client.connect(host, port)) {
 
        Serial.println("Connection to host failed");
 
        delay(1000);
        return;
    }
 
    Serial.println("Connected to server successful!");
 
    //client.print("Hello from ESP32!");
    client.write((const char *) &packet, sizeof(packet));
    
    Serial.println("Sent packet");
    client.stop();

    delay(1000);
    //delay(5000); // 5 seconds for user to write feature name during training
}

void get_imu_reading(imu_reading_t *reading) {
  float ax, ay, az;
  float gx, gy, gz;

  imu_read(&ax, &ay, &az, &gx, &gy, &gz);

  reading->accel_x_raw = (ax+16)*100;
  reading->accel_y_raw = (ay+16)*100;
  reading->accel_z_raw = (az+16)*100;
  reading->gyro_x_raw = gx+1000;
  reading->gyro_y_raw = gy+1000;
  reading->gyro_z_raw = gz+1000;
  reading->timestamp = millis();

  Serial.println(reading->gyro_y_raw);
}


// using code above

void get_next_imu_reading(MPU9250 imu, imu_reading_t *reading) {
  accel_raw_t accel_output;
  gyro_raw_t gyro_output;
  
  imu.read_gyro_raw(&gyro_output);
  imu.read_accel_raw(&accel_output);

  reading->accel_x_raw = accel_output.x_raw/2048.0;
  reading->accel_y_raw = accel_output.y_raw/2048.0;
  reading->accel_z_raw = accel_output.z_raw/2048.0;

  reading->gyro_x_raw = gyro_output.x_raw;
  reading->gyro_y_raw = gyro_output.y_raw;
  reading->gyro_z_raw = gyro_output.z_raw;

  reading->timestamp = millis();

}

imu_wifi_packet_t generate_test_packet() {
  imu_wifi_packet_t result;

  for (uint16_t i = 0; i < MAX_IMU_READINGS; i++) {
    imu_reading_t *next_reading = &result.readings[i];

    next_reading->reading_begin = 0xDEADBEEF;
    next_reading->seperator = 0x99999999;

    next_reading->accel_x_raw = i;
    next_reading->accel_y_raw = i;
    next_reading->accel_z_raw = i;

    next_reading->gyro_x_raw = 4 * i;
    next_reading->gyro_y_raw = 4 * i;
    next_reading->gyro_z_raw = 4 * i;

    next_reading->timestamp = millis();

  }

  return result;

}