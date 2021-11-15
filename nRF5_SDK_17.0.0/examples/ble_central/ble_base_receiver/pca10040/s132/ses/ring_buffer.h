#ifndef RING_BUFFER_H
#define RING_BUFFER_H

#include "queue.h"
#include "stdint.h"

typedef Queue RingBuffer;

RingBuffer* ring_buffer_init(int len);

void ring_buffer_add(RingBuffer* rbuffer, QueueElement e);

uint8_t TEST_RINGBUFFER(void);

#endif





