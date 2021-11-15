#include "ring_buffer.h"

#define MODULE_LOG_ENABLE 1
#define LOG_HEAD "RING_BUFFER"
#include "logger.h"

/***
 * Ring Buffer Initialization 
 */
RingBuffer* ring_buffer_init(int len){
  return initQueue(len);
}


void ring_buffer_add(RingBuffer* rbuffer, QueueElement e){
  if(rbuffer->capacity == rbuffer->size){
    QueueElement temp = front(rbuffer);
    dequeue(rbuffer);
    free(temp);           /* Free memory */
    enqueue(rbuffer, e);
  }
  else{
    enqueue(rbuffer, e);
  }
}


uint8_t TEST_RINGBUFFER(void){
  RingBuffer* rbuf = ring_buffer_init(5);
  ring_buffer_add(rbuf, 1);
  ring_buffer_add(rbuf, 2);
  ring_buffer_add(rbuf, 3);
  ring_buffer_add(rbuf, 4);
  ring_buffer_add(rbuf, 5);
  ring_buffer_add(rbuf, 6);

  if( (front(rbuf) != 2) || (rbuf->size) != 5 ){
    LOGE("TEST FAILED");
    return 1;
  }

  LOGI("TEST SUCCESS");
  return 0;
}