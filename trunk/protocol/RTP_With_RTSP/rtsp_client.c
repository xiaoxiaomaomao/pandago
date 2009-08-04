#include <time.h>

#include "string.h"
#include "rtsp.h"
#include "rtsp_util.h"
#include "rtsp_client.h"
#include "rtsp_sock.h"
#include "rtsp_command.h"
#include "rtsp_response.h"
#define MILLISECOND 1000LL
#define MICROSECOND 1000000

#define mTRACE printf

static int global_udp_port = 5000;

static void RTSP_LOCK()
{
}

static void RTSP_UNLOCK()
{
}


static unsigned int now()
{
    return 0; 
}

static void start_watchdog()
{
}

static void stop_watchdog()
{
}

static void watchdog_monitor_thread(void* param)
{
}

static void create_watchdog_monitor_thread()
{
}

static void destroy_watchdog_monitor_thread()
{
}

static void rtsp_monitor_thread(void* param)
{
}

static void create_rtsp_monitor_thread()
{
}

static void destroy_rtsp_monitor_thread()
{
}

static int rtsp_check_url (rtsp_client_t *client, const char *url)
{
    const char *str;
    const char *nextslash;
    const char *nextcolon;
    int hostlen;

    str = url;

    if (strncmp("rtsp://", url, strlen("rtsp://")) == 0)
        str += strlen("rtsp://");
    else
        return -1;

    nextslash = strchr(str, '/');
    nextcolon = strchr(str, ':');

    if (nextslash != 0 || nextcolon != 0)
    {
        if (nextcolon != 0 && (nextcolon < nextslash || nextslash == 0))
        {
            hostlen = nextcolon - str;
            nextcolon++;
            client->server_port = 0;
            while (rtsp_isdigit(*nextcolon))
            {
                client->server_port *= 10;
                client->server_port += *nextcolon - '0';
                nextcolon++;
            }
            if (client->server_port == 0 || (*nextcolon != '/' && *nextcolon != '\0'))
                return -1;
        }
        else
            hostlen = nextslash - str;

        if (hostlen == 0)
            return -1;

        client->server_name = (char*)malloc(hostlen + 1);
        if (client->server_name == 0)
            return -1;

        memcpy(client->server_name, str, hostlen);
        client->server_name[hostlen] = '\0';
    }
    else
    {
        if (*str == '\0')
            return -1;
        client->server_name = (char*)rtsp_strdup((char*)str);
    }

    client->url = (char*)rtsp_strdup((char*)url);
    if (client->server_port == 0)
        client->server_port = 554;

    return 0;
}


static void rtsp_free_client (rtsp_client_t* client)
{
    if (client != NULL) {
        rtsp_close_socket(client);
        CHECK_AND_FREE(client->local_url);
        CHECK_AND_FREE(client->url);
        CHECK_AND_FREE(client->server_name);
        CHECK_AND_FREE(client->session);
        CHECK_AND_FREE(client->paramsFromServer);
        free(client);
    }
}

void rtsp_destory_client(int handle)
{
    rtsp_client_t* rtsp_client = (rtsp_client_t*)handle;
    if (rtsp_client != 0) {
        rtsp_free_client(rtsp_client);
    }
}

static rtsp_client_t *rtsp_create_client (const char *url)
{
    rtsp_client_t *client;
    int ret;

    char* local_url = (char*)rtsp_strdup(url);
    client = (rtsp_client_t*) malloc(sizeof(rtsp_client_t));

    if (client == 0)
    {
        free(local_url);
        mTRACE("malloc rtsp client fail\n");
        return 0;
    }
    memset(client, 0, sizeof(rtsp_client_t));
    client->recv_timeout = 0;
    client->local_url = local_url;
    client->next_cseq = 1;                            //TODO
    client->server_socket = -1;
    client->state = RTSP_PLAYER_INIT;
    ret = rtsp_check_url(client, url);
    if (ret != 0)
    {
        mTRACE("rtsp url is error, url=%s\n", url);
        rtsp_free_client(client);
        return 0;
    }

    if (rtsp_create_socket(client) != 0)
    {
        rtsp_destory_client((unsigned int)client);
        return 0;
    }
    
    return client;
}

void rtsp_get_params(int handle, char* params)
{
    rtsp_client_t* client = (rtsp_client_t*)handle;
    if (client == NULL) {
        return ;
    }
    
    if (params != NULL && client->paramsFromServer != NULL) {
        strcpy(params, client->paramsFromServer);
    }
    return;
}

unsigned int rtsp_create_handle(const char* url)
{
    rtsp_client_t* rtsp_client = rtsp_create_client(url);
    if (rtsp_client == NULL) {
        return 0;
    }
    return (unsigned int)rtsp_client;
}

static int rtsp_comm_check_resp(rtsp_client_t* rtsp_client, rtsp_resp_t* resp)
{
    rtsp_client->next_cseq++;                                             //TODO

    if (strcmp(resp->caption, "RTSP/1.0") != 0)
    {
        mTRACE("rtsp respond title error, msg=%s\n", resp->caption);
        return -1;
    }
    
    if (strcmp(resp->retcode, "200") != 0)
    {
        mTRACE("rtsp respond code(%s) != 200\n", resp->retcode);
        return -1;
    }

    return 0;
}

rtsp_client_t* rtsp_get_client()
{
    return NULL;
}

int rtsp_get_state(int handle) 
{
    rtsp_client_t * rtsp_client = (rtsp_client_t*)handle;
    return rtsp_client->state;
}

void rtsp_set_state(int handle, int state)
{
    rtsp_client_t* rtsp_client = (rtsp_client_t*)handle;
    if (rtsp_client != NULL) {
        rtsp_client->state = state;
    }
}
int32_t rtsp_get_duration(int handle)
{
    rtsp_client_t * rtsp_client = (rtsp_client_t*)handle;
    return rtsp_client != NULL ? rtsp_client->m_duration : 0;
}

void rtsp_init_lock()
{
}

static int get_duration_time(const char *body)
{
    int time = 0;
    char *s = strstr(body,"range:npt=");
    assert(s != NULL);
    s = strchr(s,'-');
    assert( s != NULL);
    
    char *s1 = strchr(s,'.');
    *s1 = '\0';
    time =  atoi(s + 1);
    *s1 = '.';
	dTRACE("get duration time %d\n",time);
    return time;
}

int rtsp_open(int handle,int serviceGroupID)
{
    int ret = _rtsp_open(handle,serviceGroupID);
    rtsp_client_t * rtsp_client = (rtsp_client_t*)handle;
    if (ret < 0) {
        rtsp_client->state = RTSP_PLAYER_ERROR;
        return -1;
    }
    return 0;
}


int _rtsp_open(int handle, int serviceGroupID)
{
    rtsp_command_t cmd;
    rtsp_resp_t resp;
    char* local_url;

    int controlId;
    int symbolRate;
    int modulation;
    int programNumber;
    rtsp_client_t * rtsp_client;
    rtsp_init_lock();
    
    while (1)
    {
        rtsp_client = (rtsp_client_t*)handle;

        rtsp_client->recv_timeout = 5000;

        memset(&cmd, 0, sizeof(cmd));

        if (rtsp_send_cmd("OPTIONS", rtsp_client, &cmd, "") != 0)
        {
            mTRACE("after send OPTION failed\n"); 
            rtsp_client->errorCode = OPTIONS_SEND_FAILED;
            return RTSP_RET_ERR;
        }
        memset(&resp, 0, sizeof(resp));
        if (rtsp_recv_response(rtsp_client, &resp) != 0)
        {
            mTRACE("rtsp_recv_response \n\n"); 
            clear_response(&resp);
            rtsp_client->errorCode = OPTIONS_RESPONSE_FAILED;
            return RTSP_RET_ERR;
        }
        if (strncmp(resp.retcode, "200",3) != 0)
        {
            mTRACE("OPTIONS Return Code\n\n"); 
            clear_response(&resp);
            rtsp_client -> errorCode = OPTIONS_RESPONSE_FAILED;
            return RTSP_RET_ERR;
        }
        rtsp_client -> next_cseq ++;
        cmd.accept = "application/sdp";
        if (rtsp_send_cmd("DESCRIBE", rtsp_client, &cmd, "") != 0)
        {
            mTRACE("after send DESCRIBE faild\n");
	        rtsp_client->errorCode = DESCRIBE_SEND_FAILED;
            return RTSP_RET_ERR;
        }
        memset(&resp, 0, sizeof(resp));
        if (rtsp_recv_response(rtsp_client, &resp) != 0)
        {
            mTRACE("rtsp_recv_response \n\n");
            clear_response(&resp);
            rtsp_client->errorCode = DESCRIBE_RESPONSE_FAILED;
            return RTSP_RET_ERR;
        }
        if (strcmp(resp.caption, "RTSP/1.0") != 0)
        {
            mTRACE("RTSP/1.0");
            clear_response(&resp);
            return RTSP_RET_INVALID;
        }

        rtsp_client->next_cseq++;
        if (resp.cseq + 1 != rtsp_client->next_cseq)
        {
            clear_response(&resp);
            mTRACE("resq.cseq + 1 = %d, rtsp_client->nexe_cseq %d\n\n",resp.cseq,rtsp_client->next_cseq);
	        rtsp_client->errorCode = DESCRIBE_CHECK_FAILED;
            return RTSP_RET_INVALID;
        }

        if (strcmp(resp.retcode, "302") == 0)
        {
            local_url = (char*)rtsp_strdup(resp.location);

            clear_response(&resp);

        }
        else if(strcmp(resp.retcode, "200") == 0)
        {
            break;
        }
        else
        {
	        rtsp_client->errorCode = DESCRIBE_CHECK_FAILED;
            clear_response(&resp);
            return RTSP_RET_INVALID;
        }
    }

    if (resp.body != 0) {
        rtsp_client->m_duration = get_duration_time(resp.body);           
        dTRACE("duration time = %d",rtsp_client->m_duration);
    }
    clear_response(&resp);

    /*setup-----------------------------------------------------*/
    memset(&cmd, 0, sizeof(cmd));
    char transport[128] = {0};
    sprintf(transport, "RTP_AVP;unicast;client_port=%d-%d", global_udp_port, global_udp_port + 1);
    cmd.transport = transport;
    global_udp_port += 2;

    if (rtsp_send_cmd("SETUP", rtsp_client, &cmd, "/track1") != 0)//trackID=0
    {
        rtsp_client->errorCode = SETUP_SEND_FAILED;
        return RTSP_RET_ERR;
    }
    memset(&resp, 0, sizeof(resp));
    resp.handle = (int)rtsp_client;
    if (rtsp_recv_response(rtsp_client, &resp) != 0)
    {
        rtsp_client->errorCode = SETUP_RESPONSE_FAILED;
        mTRACE("rtsp_open rtsp_recv_response");
        clear_response(&resp);
        return RTSP_RET_ERR;
    }

    if (rtsp_comm_check_resp(rtsp_client, &resp) != 0)
    {
        rtsp_client->errorCode = SETUP_CHECK_FAILED;
        clear_response(&resp);
        return RTSP_RET_INVALID;
    }

    rtsp_client->session = (char*)rtsp_strdup(resp.session);
    rtsp_client->state = RTSP_PLAYER_READY;
    clear_response(&resp);
    return RTSP_RET_OK;
}

int rtsp_play(int handle, int32_t pos, int scale)
{
    rtsp_client_t * rtsp_client = (rtsp_client_t*)handle;
    int ret = _rtsp_play(handle, pos, scale);
    
    if (ret < 0) {
        rtsp_client->state = RTSP_PLAYER_ERROR;
        return -1;
    }
    return 0;
}  

int _rtsp_play(int handle, int32_t pos, int32_t scale)
{
    int time = pos;

    rtsp_client_t* rtsp_client = (rtsp_client_t*)handle;
    assert(rtsp_client);

    RTSP_LOCK();
    start_watchdog();

    char str[20];
    rtsp_command_t cmd;
    memset(&cmd, 0, sizeof(cmd));
    cmd.session = rtsp_client->session;

    cmd.scale = (scale == 0 ? 1 : scale);

    if (pos != -1)
    {
        sprintf(str, "npt=%d-", time);
        cmd.range = str;
	    rtsp_client->curTime = time;
    }
    if (rtsp_send_cmd("PLAY", rtsp_client, &cmd, "") != 0)
    {
        RTSP_UNLOCK();
        rtsp_client->errorCode = PLAY_SEND_FAILED;
        mTRACE("rtsp_send_cmd faield\n\n");
        return RTSP_RET_ERR;
    }

    rtsp_resp_t resp;
    memset(&resp, 0, sizeof(resp));

    if (rtsp_recv_response(rtsp_client, &resp) != 0)
    {
        mTRACE("rtsp_recv_response\n\n");
        rtsp_client->errorCode = PLAY_RESPONSE_FAILED;
        clear_response(&resp);
        RTSP_UNLOCK();
        return RTSP_RET_ERR;
    }

    if (rtsp_comm_check_resp(rtsp_client, &resp) != 0)
    {
        mTRACE("rtsp_comm_check_resp\n\n");
        clear_response(&resp);
        rtsp_client->errorCode = PLAY_CHECK_FAILED;
        RTSP_UNLOCK();
        return RTSP_RET_INVALID;
    }

    clear_response(&resp);
    stop_watchdog();
    RTSP_UNLOCK();
    rtsp_client->state = RTSP_PLAYER_PLAY;
    return RTSP_RET_OK;
}

int rtsp_pause(int handle)
{
    rtsp_client_t * rtsp_client = (rtsp_client_t*)handle;
    RTSP_LOCK();
    start_watchdog();

    rtsp_command_t cmd;
    memset(&cmd, 0, sizeof(cmd));
    cmd.session = rtsp_client->session;
    if (rtsp_send_cmd("PAUSE", rtsp_client, &cmd, "") != 0)
    {
        RTSP_UNLOCK();
        rtsp_client->errorCode = PAUSE_SEND_FAILED;
        return RTSP_RET_ERR;
    }

    rtsp_resp_t resp;
    memset(&resp, 0, sizeof(resp));
    if (rtsp_recv_response(rtsp_client, &resp) != 0)
    {
        clear_response(&resp);
        RTSP_UNLOCK();
        rtsp_client->errorCode = PAUSE_RESPONSE_FAILED;
        return RTSP_RET_ERR;
    }

    if (rtsp_comm_check_resp(rtsp_client, &resp) != 0)
    {
        rtsp_client->errorCode = PAUSE_CHECK_FAILED;
        clear_response(&resp);
        RTSP_UNLOCK();
        return RTSP_RET_INVALID;
    }
    rtsp_client->state = RTSP_PLAYER_PAUSE;
    clear_response(&resp);
    stop_watchdog();
    RTSP_UNLOCK();
    return RTSP_RET_OK;
}

int32_t rtsp_close(int handle)
{
    rtsp_client_t * rtsp_client = (rtsp_client_t*)handle;
    if (rtsp_client == NULL) {
        return;
    }

    RTSP_LOCK();
    start_watchdog();

    rtsp_command_t cmd;
    memset(&cmd, 0, sizeof(cmd));
    cmd.session = rtsp_client->session;
    
    if (rtsp_send_cmd("TEARDOWN", rtsp_client, &cmd, "") != 0)
    {
        rtsp_client->errorCode = TEARDOWN_SEND_FAILED;
        return RTSP_RET_ERR;
    }
   
    rtsp_resp_t resp;
    memset(&resp, 0, sizeof(resp));
    if (rtsp_recv_response(rtsp_client, &resp) != 0) {
        rtsp_client->errorCode = TEARDOWN_RESPONSE_FAILED;
        clear_response(&resp);
	    return RTSP_RET_ERR;
    }
   
    if (rtsp_comm_check_resp(rtsp_client, &resp) != 0)
    {
        rtsp_client->errorCode = TEARDOWN_CHECK_FAILED;
        clear_response(&resp);
        RTSP_UNLOCK();
        return RTSP_RET_ERR;
    }

    stop_watchdog();
    RTSP_UNLOCK();
    rtsp_client->state = RTSP_PLAYER_CLOSE;
    return RTSP_RET_OK;
}

int32_t rtsp_get_current_time(int handle)
{
    rtsp_client_t * rtsp_client = (rtsp_client_t*)handle;
    if(rtsp_client != NULL)
		dTRACE("rtsp_get_current_time %d\n\n",rtsp_client->curTime);
    return rtsp_client != NULL ? rtsp_client->curTime : 0;
}

static int get_current_play_time(rtsp_client_t* rtsp_client, const char* body)
{
    char* s_start;
    char* s_end;
    int time;
    if ((s_start = strstr(body,"curTime: ")) == 0) 
    {
        return 0;
    }

    s_start += strlen("curTime: ");
    if (strstr(s_start, "DONE") != 0) 
    {
        rtsp_client->state = RTSP_PLAYER_CLOSE;
        return 0;
    }

    s_end = strstr(s_start, "\r\n");
    assert(s_end != NULL);
    *s_end = '\0';
    time = atoi(s_start);
    *s_end = '\r';
    return time;
}

int rtsp_keepalive(int handle)
{
    rtsp_client_t * rtsp_client = (rtsp_client_t*)handle;
    int ret = _rtsp_keepalive(handle);
    if (ret < 0) {
        return -1;
    }
    return 0;
}

int _rtsp_keepalive(int handle)
{
    rtsp_client_t * rtsp_client = (rtsp_client_t*)handle;
    if(rtsp_client == NULL) 
    {
        return RTSP_RET_OK;
    }
    int times = 0;
    rtsp_command_t cmd;
    memset(&cmd, 0, sizeof(cmd));
    cmd.session = rtsp_client->session;
    if (rtsp_send_cmd("GET_PARAMETER", rtsp_client, &cmd, "") != 0)
    {
	    rtsp_client->errorCode = HEARTBEAT_SEND_FAILED;
        times = ++rtsp_client->sendHeartBeatTimes;
        if (times > RTSP_SEND_HEART_BEAT_TIMES)
        {
            rtsp_client->errorCode = HEARTBEAT_TIMEOUT;
            rtsp_client->state = RTSP_PLAYER_ERROR;
        }

        return RTSP_RET_ERR;
    }

    rtsp_resp_t resp;
    memset(&resp, 0, sizeof(resp));

    if (rtsp_recv_response(rtsp_client, &resp) != 0)
    {
	    rtsp_client->errorCode = HEARTBEAT_RESPONSE_FAILED;
        times = ++rtsp_client->sendHeartBeatTimes;
        if (times > RTSP_SEND_HEART_BEAT_TIMES) 
        {
            rtsp_client->errorCode = HEARTBEAT_TIMEOUT;
            rtsp_client->state = RTSP_PLAYER_ERROR;
        }
	
        clear_response(&resp);
        return RTSP_RET_ERR;
    }

    rtsp_client->sendHeartBeatTimes = 0;
    if (rtsp_comm_check_resp(rtsp_client, &resp) != 0)
    {
        clear_response(&resp);
        rtsp_client->errorCode = HEARTBEAT_CHECK_FAILED;
        rtsp_client->state = RTSP_PLAYER_ERROR;
        return RTSP_RET_INVALID;
    }
    
    if (resp.body != NULL) {
       rtsp_client->curTime = get_current_play_time(rtsp_client, resp.body);  
    }
    
    clear_response(&resp);
    return RTSP_RET_OK;
}

int rtsp_nodata_notify()
{
    return RTSP_RET_OK;
}

void rtsp_get_dvbinfo(int* freq, int* qampid)
{
   /* freq = rtsp_client->frequency;
    *qampid = rtsp_client->programNumber;
    */
}

char* rtsp_version()
{
    return VERSION;
}

int rtsp_get_error(int handle)
{
    rtsp_client_t* rtsp_client = (rtsp_client_t*)handle;
    return rtsp_client->errorCode;
}
