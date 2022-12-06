#ifndef MPU_9250_REGISTERS_H
#define MPU_9250_REGISTERS_H

#define IMU_I2C_ADDR  0x68

#define GYRO_CONFIG   0x1B
#define ACCEL_CONFIG  0x1C

#define ACCEL_XOUT_H  0x3B
#define ACCEL_XOUT_L  0x3C
#define ACCEL_YOUT_H  0x3D
#define ACCEL_YOUT_L  0x3E
#define ACCEL_ZOUT_H  0x3F
#define ACCEL_ZOUT_L  0x40

#define GYRO_XOUT_H   0x43
#define GYRO_XOUT_L   0x44
#define GYRO_YOUT_H   0x45
#define GYRO_YOUT_L   0x46
#define GYRO_ZOUT_H   0x47
#define GYRO_ZOUT_L   0x48 

#define AFS_SEL_0     16384.0
#define AFS_SEL_1     8192.0
#define AFS_SEL_2     4096.0
#define AFS_SEL_3     2048.0



#endif