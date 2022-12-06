// FOR THE MPU9250
#include "Wire.h"
// library from https://github.com/bolderflight/MPU9250
const int sda = 21;
const int scl = 22;

float gyroAngleX = 0.0;
float gyroAngleY = 0.0;
float gyroAngleZ = 0.0;

float currentTime, previousTime;

float caliX = 0.0;
float caliY = 0.0;
float caliZ = 0.0;

void callibrate(){
  Serial.println("Calibrating gyroscope...");
  int count = 0;
  
  gyroAngleX = 0;
  gyroAngleY = 0;
  gyroAngleZ = 0;

  float currentTime = millis();
  float previousTime = 0;

  while (count < 100) {

    count ++;

    Wire.beginTransmission(0x68);
    Wire.write(0x43);
    Wire.endTransmission();
        
    Wire.requestFrom(0x68, 6); 
    byte gyro_x_h = Wire.read();
    byte gyro_x_l = Wire.read();
    byte gyro_y_h = Wire.read();
    byte gyro_y_l = Wire.read();
    byte gyro_z_h = Wire.read();
    byte gyro_z_l = Wire.read();

    int16_t GYRO_X_RAW = gyro_x_h << 8 | gyro_x_l;
    int16_t GYRO_Y_RAW = gyro_y_h << 8 | gyro_y_l;
    int16_t GYRO_Z_RAW = gyro_z_h << 8 | gyro_z_l;

    float gyroX_Per_S = (GYRO_X_RAW/131.0);
    float gyroY_Per_S = (GYRO_Y_RAW/131.0);
    float gyroZ_Per_S = (GYRO_Z_RAW/131.0);

    previousTime = currentTime;
    currentTime = millis();
    float elapsedTime = (currentTime - previousTime)/1000.0;

    gyroAngleX = gyroAngleX + gyroX_Per_S * elapsedTime;
    gyroAngleY = gyroAngleY + gyroX_Per_S * elapsedTime;
    gyroAngleZ = gyroAngleZ + gyroX_Per_S * elapsedTime;

    delay(100);
  }

  caliX = gyroAngleX/100;
  caliY = gyroAngleY/100;
  caliZ = gyroAngleZ/100;

  gyroAngleX = 0;
  gyroAngleY = 0;
  gyroAngleZ = 0;

}

void imu_setup() {
  Wire.begin(sda, scl);

  Wire.beginTransmission(0x68);
  Wire.write(0x1C);
  Wire.write(0b1011);
  Wire.endTransmission();

  currentTime = millis();
  callibrate();
}

void reset_gyro(){
  gyroAngleX = 0.0;
  gyroAngleY = 0.0;
  gyroAngleZ = 0.0;
}

void imu_read(float *ax, float *ay, float *az, float *gx, float *gy, float *gz) {
  
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission(); 

  Wire.requestFrom(0x68, 6); 
  
  int16_t ACCEL_X_RAW = Wire.read() << 8 | Wire.read();
  int16_t ACCEL_Y_RAW = Wire.read() << 8 | Wire.read();
  int16_t ACCEL_Z_RAW = Wire.read() << 8 | Wire.read();

  *ax = ACCEL_X_RAW/2048.0;
  *ay = ACCEL_Y_RAW/2048.0;
  *az = ACCEL_Z_RAW/2048.0;

  Wire.beginTransmission(0x68);
  Wire.write(0x43);
  Wire.endTransmission(); 

  Wire.requestFrom(0x68, 6); 
  
  int16_t GYRO_X_RAW = Wire.read() << 8 | Wire.read();
  int16_t GYRO_Y_RAW = Wire.read() << 8 | Wire.read();
  int16_t GYRO_Z_RAW = Wire.read() << 8 | Wire.read();

  previousTime = currentTime;
  currentTime = millis();
  float elapsedTime = (currentTime - previousTime)/1000.0;

  gyroAngleX = gyroAngleX + ((GYRO_X_RAW/131.0) - caliX) * elapsedTime;
  gyroAngleY = gyroAngleY + ((GYRO_Y_RAW/131.0) - caliY) * elapsedTime;
  gyroAngleZ = gyroAngleZ + ((GYRO_Z_RAW/131.0) - caliZ) * elapsedTime;

  *gx = gyroAngleX;
  *gy = gyroAngleY;
  *gz = gyroAngleZ;

}