#ifndef _RTSP_H_
#define _RTSP_H_ 
#ifdef __cplusplus
extern "C" 
{
#endif

#include "rtsp_client.h"
#define VERSION "RTSP FOR IPQAM ONEWAVE 1.0"

#define RTSP_RET_OK			0
#define RTSP_RET_INVALID	-1
#define RTSP_RET_ERR		-2
#ifdef __DEBUG__
#define mTRACE printf
#define dTRACE printf
#else
#define mTRACE
#define dTRACE
#endif
/**
 * The rtsp client have sent heart beat for 10 times,but don't
 * receive any respond from server. The rtsp client think the server or
 * network is unavaliable.
 */
#define RTSP_SEND_HEART_BEAT_TIMES 10
#define RTSP_PLAYER_INIT  0
#define RTSP_PLAYER_READY 2
#define RTSP_PLAYER_PLAY  3
#define RTSP_PLAYER_CLOSE 4 
#define RTSP_PLAYER_PAUSE 5      
#define RTSP_PLAYER_ERROR 6

#define CONNECT_FAILED           -100

#define PLAY_SEND_FAILED         -201
#define PLAY_RESPONSE_FAILED     -202 
#define PLAY_CHECK_FAILED        -300

#define SETUP_SEND_FAILED        -203
#define SETUP_RESPONSE_FAILED    -204
#define SETUP_CHECK_FAILED       -301

#define PAUSE_SEND_FAILED        -205
#define PAUSE_RESPONSE_FAILED    -206
#define PAUSE_CHECK_FAILED       -302

#define DESCRIBE_SEND_FAILED     -207
#define DESCRIBE_RESPONSE_FAILED -208
#define DESCRIBE_CHECK_FAILED    -303

#define TEARDOWN_SEND_FAILED     -209
#define TEARDOWN_RESPONSE_FAILED -210
#define TEARDOWN_CHECK_FAILED    -309

#define HEARTBEAT_SEND_FAILED    -211
#define HEARTBEAT_RESPONSE_FAILED -212
#define HEARTBEAT_TIMEOUT        -213
#define HEARTBEAT_CHECK_FAILED     -214



unsigned int rtsp_create_handle();

/**
 * Open a rtsp connection,include SETUP,DESCRIBE sharkhand setup.
 * @param url The address of media; eg:rtsp://server_ip/movie.ts.
 * @param serviceGroupID The id of service group.
 * @param func Receive the message from server.
 * @Return RTSP_RET_ERR if open the connection failed.otherwise return RTSP_RET_OK.
 */
int rtsp_open(int handle, int serviceGroupID);

/**
 * Start play the media, send PLAY command.
 * @param The start time of the media.
 * @return RTSP_RET_ERR if open the connection failed.otherwise return RTSP_RET_OK.
 */
int	rtsp_play(int handle, int pos, int32_t scale);

/**
 * Pause the media stream. send PAUSE command.
 * @return RTSP_RET_ERR if open the connection failed.otherwise return RTSP_RET_OK.
 */
int	rtsp_pause(int handle);


/**
 * Send Heart beat to RTSP server.
 * send GET_PARAMTER to server to tell the server the client is live and 
 * get current play time of media from the server response. 
 * @return RTSP_RET_ERR if open the connection failed.otherwise return RTSP_RET_OK.
 * Attention: can ignore the return value,because the server maybe don't responsed the GET_PARAMTER 
 * command every times; if don't receive any response from server, after send RTSP_SEND_HEART_BEAT_TIMES 
 * GET_PARAMER,the rtsp_client state will be set at RTSP_PLAYER_CLOSE.
 */
int rtsp_keepalive(int handle);

int rtsp_nodata_notify();

/**
 * Close the media data stream.send TERADOWN command.
 * @return NULL.
 */
int rtsp_close(int handle);

void rtsp_break_block();

int rtsp_get_state(int handle);

void rtsp_set_state(int handle,int state);
/**
 * The the rtsp version
 * @return the version.
 */
char* rtsp_version();

rtsp_client_t* rtsp_get_client();

/**
 * Get the duration.
 * @return the duration of media data;
 */
int32_t rtsp_get_duration(int handle);

/**
 * Get current play time.
 * @return the current play time. by second unit.
 */
int32_t rtsp_get_current_time(int handle);
/**
 * Get the frequency and QAM id
 * @return None.
 */
//void rtsp_get_dvbinfo(int* fredq, int* qampid);
void rtsp_destory_client(int handle);

void rtsp_get_params(int handle, char* params);

int rtsp_get_error(int handle);

int rtsp_get_packet(int handle);
#ifdef __cplusplus
}
#endif

#endif

