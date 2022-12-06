from construct import *
from construct.lib import *

MAX_IMU_READINGS = 50

def imu_reading():
    return Struct(
        'reading_begin' / BytesInteger(4, swapped=True),

        'accel_x_raw' / BytesInteger(2, swapped=True),
        'accel_y_raw' / BytesInteger(2, swapped=True),
        'accel_z_raw' / BytesInteger(2, swapped=True),

        'pad1' / BytesInteger(2, swapped=True),

        'seperator' / BytesInteger(4, swapped=True),

        'gyro_x_raw' / BytesInteger(2, swapped=True),
        'gyro_y_raw' / BytesInteger(2, swapped=True),
        'gyro_z_raw' / BytesInteger(2, swapped=True),

        'pad2' / BytesInteger(2, swapped=True),

        'timestamp' / BytesInteger(4, swapped=False),
        )

imu_wifi_packet_t = Struct(
    "readings" / Array(MAX_IMU_READINGS, imu_reading())
    )
