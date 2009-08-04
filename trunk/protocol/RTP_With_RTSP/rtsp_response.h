/*--------------------------------------------------------
	
	COPYRIGHT 2007 (C) DVN (Holdings) Ltd (Hongkong)

	AUTHOR:		wangry@dvnchina.com
	PURPOSE:	kasenna simple rtsp lib
	CREATED:	2007-12-10  

	MODIFICATION HISTORY
	Date        By     Details
	----------  -----  -------

--------------------------------------------------------*/
#ifndef _RTSP_RESPONSE_H_
#define _RTSP_RESPONSE_H_ 

#ifdef __cplusplus
extern "C" 
{
#endif

typedef struct rtsp_resp_t {
  int content_length;
  int cseq;
  int close_connection;
  char retcode[4];
  char *caption;
  char *retresp;
  char *body;
  char *accept;
  char *accept_encoding;
  char *accept_language;
  char *allow_public;
  char *authorization;
  char *bandwidth;
  char *blocksize;
  char *cache_control;
  char *content_base;
  char *content_encoding;
  char *content_language;
  char *content_location;
  char *content_type;
  char *cookie;
  char *date;
  char *expires;
  char *from;
  char *if_modified_since;
  char *last_modified;
  char *location;
  char *proxy_authenticate;
  char *proxy_require;
  char *range;
  char *referer;
  char *require;
  char *retry_after;
  char *rtp_info;
  char *scale;
  char *server;
  char *session;
  char *speed;
  char *transport;
  char *unsupported;
  char *user_agent;
  char *via;
  char *www_authenticate;
  char *x_Info;
  char *x_Reason;
  int handle;
}rtsp_resp_t;

void clear_response (rtsp_resp_t *resp);
void simple_parse_sdp(char* sdp, int* range, int* freq, int* pid,int* controlId, int* symbolRate, int* modulation,int* programNumber);
int rtsp_recv_response (rtsp_client_t *client, rtsp_resp_t *response);

#ifdef __cplusplus
}
#endif

#endif

