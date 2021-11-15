#ifndef SERIAL_TRANSFER_H
#define SERIAL_TRANSFER_H

#include "main.h"
#include "ring_buffer.h"

typedef enum{
  HIGH_PRIORITY_PACKET,
  MEDIUM_PRIORITY_PACKET,
  LOW_PRIORITY_PACKET
}packet_priority_t;

typedef struct{
  int16_t packet_length;
  uint8_t buf[256];
}packet_t;

typedef struct{
  RingBuffer* high_priority_queue;
  RingBuffer* medium_priority_queue;
  RingBuffer* low_priority_queue;
}packet_queues_t;

err_code_t serial_transfer_init(void);

err_code_t serial_transfer_add_to_queue(packet_priority_t priority, packet_t* packet);

err_code_t serial_transfer_loop(void);



#endif




