#include "blue_data.h"
#define TIMESIZE 4
#define AXSIZE 2 
#define NUMBERAXIS 3
#include <stdio.h>
#include <stdlib.h>
#include "sdkconfig.h"

int64_t get_time(){
    struct timeval tv_now;
    gettimeofday(&tv_now, NULL);
    int64_t time_us = (int64_t)tv_now.tv_sec * 1000000L + (int64_t)tv_now.tv_usec;
    
    return time_us;
}

void set_time_bytes(uint8_t* bytes){

    struct timeval tv_now;
    gettimeofday(&tv_now, NULL);
    uint32_t time_us_control = (uint32_t)((uint64_t)tv_now.tv_sec * 1000000L + (uint64_t)tv_now.tv_usec)/100L;

    union {
    uint32_t time_us;
    uint8_t bytes[TIMESIZE];
  } l;
  
    l.time_us=time_us_control;
    memcpy(bytes, l.bytes, TIMESIZE);
}

void set_sensors_bytes(int8_t* data, int16_t ax,int16_t ay,int16_t az,int16_t gx,int16_t gy,int16_t gz){
  

  set_sensor_bytes(data,ax,ay,az);
  set_sensor_bytes(&data[NUMBERAXIS*2],gx,gy,gz);


}

void set_sensors_mag(int8_t* data, int16_t ax,int16_t ay,int16_t az,int16_t gx,int16_t gy,int16_t gz,int16_t mx,int16_t my,int16_t mz){
  

  set_sensor_bytes(data,ax,ay,az);
  set_sensor_bytes(&data[NUMBERAXIS*2],gx,gy,gz);
  set_sensor_bytes(&data[NUMBERAXIS*4],mx,my,mz);


}

void set_sensor_bytes(int8_t* data, int16_t x,int16_t y,int16_t z){
  union{
    int16_t v[NUMBERAXIS];
    int8_t data[NUMBERAXIS * AXSIZE];
  }s;

  s.v[0]=x;
  s.v[1]=y;
  s.v[2]=z;
  //printf("v=%hd v=%hd v=%hd data=%hhd data=%hhd data=%hhd data=%hhd data=%hhd data=%hhd\n",s.v[0],s.v[1],s.v[2],s.data[0]
  //,s.data[1],s.data[2],s.data[3],s.data[4],s.data[5]);
  //printf("%hhd, %hhd, %hhd, %hhd, %hhd, %hhd, ",s.data[0]
  //,s.data[1],s.data[2],s.data[3],s.data[4],s.data[5]);
  memcpy(data, s.data, NUMBERAXIS * AXSIZE);

}
void set_bytes(int8_t *data, int16_t ax,int16_t ay,int16_t az,int16_t gx,int16_t gy,int16_t gz){

  set_time_bytes((uint8_t*)data);
  set_sensors_bytes(&data[TIMESIZE], ax, ay, az, gx, gy, gz);

}

void set_bytes_mag(int8_t *data, int16_t ax,int16_t ay,int16_t az,int16_t gx,int16_t gy,int16_t gz,int16_t mx,int16_t my,int16_t mz){

  set_time_bytes((uint8_t*)data);
  set_sensors_mag(&data[TIMESIZE], ax, ay, az, gx, gy, gz,mx, my, mz);

}
