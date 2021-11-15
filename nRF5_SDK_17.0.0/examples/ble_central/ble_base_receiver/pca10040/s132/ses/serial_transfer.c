#define MODULE_LOG_ENABLE 1
#define LOG_HEAD "UART"
#include "logger.h"

#include "serial_transfer.h"
#include "config.h"
#include "hardware.h"

#include "nrf_uart.h"
#include "app_uart.h"
#include "app_error.h"

#define UART_TX_BUF_SIZE 256                      
#define UART_RX_BUF_SIZE 256                        

/* Private Static Variables and Objects */
static packet_queues_t packet_queues;

/**
 * @brief Interrupt handler for UART Module
 * @param Uart event_type
 * @return None
 */
void serial_uart_error_handle(app_uart_evt_t * p_event){
  if (p_event->evt_type == APP_UART_COMMUNICATION_ERROR){
    APP_ERROR_HANDLER(p_event->data.error_communication);
  }
  else if (p_event->evt_type == APP_UART_FIFO_ERROR){
    APP_ERROR_HANDLER(p_event->data.error_code);
  }
}

/**
 * @brief Send buffer over Uart
 * @param buf  pointer to start location of bytes
 * @param len  length of buffer to send (in bytes)
 * @return err_code
 */
err_code_t serial_uart_send_buf(uint8_t* buf, uint16_t len){
  for(uint16_t i=0; i<len; i++){
    while ( app_uart_put(buf[i]) != NRF_SUCCESS);
  }
  return ERR_NONE;
}

/**
 * @brief Hardware Uart Initialization
 * @param None
 * @return None
 */
static void serial_uart_init(void){
  uint32_t err_code;
  const app_uart_comm_params_t comm_params ={
    UART_PIN_DISCONNECTED,    //rx pin
    UART_TX_PIN,
    UART_PIN_DISCONNECTED,
    UART_PIN_DISCONNECTED,
    APP_UART_FLOW_CONTROL_DISABLED,
    false,
    NRF_UART_BAUDRATE_115200
  };

  APP_UART_FIFO_INIT(
    &comm_params, UART_RX_BUF_SIZE, UART_TX_BUF_SIZE, serial_uart_error_handle, APP_IRQ_PRIORITY_LOWEST, err_code
  );

  APP_ERROR_CHECK(err_code);
}

/**
 * @brief Initialize and setup serial transfer module
 * @param None
 * @return err_code
 */
err_code_t serial_transfer_init(void){
  serial_uart_init();

  packet_queues.high_priority_queue   = ring_buffer_init(SERIAL_HIGH_PRIORITY_QUEUE_SIZE);
  packet_queues.medium_priority_queue = ring_buffer_init(SERIAL_MEDIUM_PRIORITY_QUEUE_SIZE);
  packet_queues.low_priority_queue    = ring_buffer_init(SERIAL_LOW_PRIORITY_QUEUE_SIZE);

  LOGD("Init complete");
  return ERR_NONE;
}

/**
 * @brief Add packet to transfer queue.
 * @param priority   priority of packet
 * @param packet     pointer to packet
 * @return err_code
 */
err_code_t serial_transfer_add_to_queue(packet_priority_t priority, packet_t* packet){
  if(packet == NULL) return ERR_MEMORY_ALLOC;
  
  switch(priority){
    case HIGH_PRIORITY_PACKET:
      ring_buffer_add(packet_queues.high_priority_queue, packet);
      break;

    case MEDIUM_PRIORITY_PACKET:
      ring_buffer_add(packet_queues.medium_priority_queue, packet);
      break;

    case LOW_PRIORITY_PACKET:
      ring_buffer_add(packet_queues.low_priority_queue, packet);
      break;

    default:
      break;  
  }
  return ERR_NONE;
}

/**
 * @brief Process the front element in queue
 * @param queue     pointer to queue to be processed
 * @return err_code
 */
static err_code_t serial_process_queue(RingBuffer* q){
  packet_t* packet = front(q);

  /* Discard invalid packets */
  if(packet->packet_length < 1){
    dequeue(q);
    free(packet);
    return ERR_NONE;
  }

  /* If BLE Send not successful, do not dequeue */
  if(serial_uart_send_buf(packet->buf, packet->packet_length)){
    return ERR_PERIPH;
  }

  dequeue(q);
  free(packet); 
  return ERR_NONE;
}

/**
 * @brief Called on every iteration of main loop to handle serial transfer
 * @param priority   None
 * @return err_code
 */
err_code_t serial_transfer_loop(void){
  for(uint16_t i=0; i<SERIAL_TRANSFER_PACKETS_PER_LOOP; i++){
    
    /* If High Priority Queue is not empty */
    if(packet_queues.high_priority_queue->size ){
      uint8_t ans = serial_process_queue(packet_queues.high_priority_queue);
      if(ans) return ans;
      else continue;
    }

    /* If Medium Priority Queue is not empty */
    else if(packet_queues.medium_priority_queue->size ){
      uint8_t ans = serial_process_queue(packet_queues.medium_priority_queue);
      if(ans) return ans;
      else continue;
    }

    /* If Low Priority Queue is not empty */
    else if(packet_queues.low_priority_queue->size ){
      uint8_t ans = serial_process_queue(packet_queues.low_priority_queue);
      if(ans) return ans;
      else continue;
    }
  }
}
