#ifndef _RTSP_SOCK_H_
#define _RTSP_SOCK_H_ 

#ifdef __cplusplus
extern "C" 
{
#endif

int rtsp_create_socket (rtsp_client_t *client);
int rtsp_send_sock (rtsp_client_t *client, const char *buffer, int len);
int rtsp_receive_socket (rtsp_client_t *client, char *buffer, int len);
void rtsp_close_socket (rtsp_client_t *client);

#ifdef __cplusplus
}
#endif

#endif

