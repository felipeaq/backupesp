#define WINDOWDATA 166
#define STEP 16
#define STEPMAG 22
#define MAXITERATIONS WINDOWDATA/STEP
#define LENBUFFER 500
#include <inttypes.h>

#ifdef __cplusplus
extern "C" {
#endif



#ifndef DEFMPU_DATA
#define DEFMPU_DATA
struct mpu_data
{//TODO tornar thread safe
 uint8_t send_data[LENBUFFER][WINDOWDATA];   
 uint32_t pos_spi;
 uint32_t pos_tcp;
 uint32_t overflow;
 uint16_t len;

};
typedef struct mpu_data mpu_data;

void start_mpu_data(mpu_data *global_mpu_data);
void increment_pos_spi(mpu_data *global_mpu_data);
int increment_pos_tcp(mpu_data *global_mpu_data, char *wr_buffer);
void reset_overflow (mpu_data *global_mpu_data);

#endif
#ifdef __cplusplus
}
#endif