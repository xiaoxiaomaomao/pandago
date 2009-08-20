#ifndef _RTSP_CLIENT_H_
#define _RTSP_CLIENT_H_ 

#ifdef __cplusplus
extern "C" 
{
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#define RTSP_ERR printf
#define RTSP_ALERT
#define RTSP_INFO printf
#define RTSP_DBG

#define CHECK_AND_FREE(a) if ((a) != 0) { free((void *)(a)); (a) = 0;}
#define RECV_BUFF_DEFAULT_LEN 2048

typedef struct rtsp_client_t {
  char *url;
  char *server_name;
  char *session;
  char* paramsFromServer;
  
  int32_t next_cseq;
  int32_t server_socket;
  struct in_addr server_addr;
  int32_t server_port;
  int32_t recv_timeout;
  int32_t m_buffer_len;
  int32_t m_offset_on;
  int32_t controlId;
  int32_t symbolRate;
  int32_t modulation;
  int32_t programNumber;
  int32_t frequency;
  int32_t state;
  int32_t curTime;
  int32_t sendHeartBeatTimes;
  int32_t m_duration;
  int32_t errorCode;
  char m_recv_buffer[RECV_BUFF_DEFAULT_LEN + 1];
  char *local_url;
  int32_t local_port;
  unsigned char* packetBuffer;
  unsigned int offset;
} rtsp_client_t;

#ifdef __cplusplus
}
#endif

#endif

