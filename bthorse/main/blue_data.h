#include <inttypes.h>
#include <sys/time.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

int64_t get_time();
void set_time_bytes(uint8_t* bytes);
void set_bytes(int8_t *data, int16_t ax,int16_t ay,int16_t az,int16_t gx,int16_t gy,int16_t gz);
void set_sensor_bytes(int8_t* data, int16_t x,int16_t y,int16_t z);
void set_sensors_bytes(int8_t* data, int16_t ax,int16_t ay,int16_t az,int16_t gx,int16_t gy,int16_t gz);
void set_sensors_mag(int8_t* data, int16_t ax,int16_t ay,int16_t az,int16_t gx,int16_t gy,int16_t gz,int16_t mx,int16_t my,int16_t mz);
void set_bytes_mag(int8_t *data, int16_t ax,int16_t ay,int16_t az,int16_t gx,int16_t gy,int16_t gz,int16_t mx,int16_t my,int16_t mz);

#ifdef __cplusplus
}
#endif