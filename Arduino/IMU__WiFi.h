#ifndef IMU_WIFI_H
#define IMU_WIFI_H

const uint16_t MAX_IMU_READINGS = 50;


typedef struct __attribute__((PACKED)) {
  uint32_t reading_begin;
  
  uint16_t accel_x_raw;
  uint16_t accel_y_raw;
  uint16_t accel_z_raw;
  uint16_t pad1;

  uint32_t seperator;

  uint16_t gyro_x_raw;
  uint16_t gyro_y_raw;
  uint16_t gyro_z_raw;

  uint16_t pad2;

  uint32_t timestamp;
} imu_reading_t;

typedef struct __attribute__((PACKED)) {
  imu_reading_t readings[MAX_IMU_READINGS];
} imu_wifi_packet_t;


#endif