#include "rtsp_client.h"
#include "rtsp_sock.h"
#include "rtsp_command.h"
#include "rtsp_util.h"
#include "rtsp.h"
#define SEND_BUFF_LEN 2048
#define USER_AGENT "DVN-IPQAM RTSP 1.0"

#define ADD_FIELD(fmt, value...) \
ret = sprintf(buffer + *at, (fmt), value); \
*at += ret;
static void rtsp_build_common (char *buffer, int *at, rtsp_client_t *client, rtsp_command_t *cmd)
{
	int ret;

	ADD_FIELD("CSeq: %u\r\n", client->next_cseq);

	if (cmd && cmd->accept)
	{
		ADD_FIELD("Accept: %s\r\n", cmd->accept);
	}
    if (cmd && cmd->authorization)
	{
		ADD_FIELD("Authorization: %s\r\n", cmd->authorization);
	}
	if (cmd && cmd->session)
	{
		ADD_FIELD("Session: %s\r\n", cmd->session);
	}

	if (cmd && cmd->range)
	{
		ADD_FIELD("Range: %s\r\n", cmd->range);
	}
	if (cmd && cmd->scale != 0)
	{
		ADD_FIELD("Scale: %d\r\n", cmd->scale);
	}
	if (cmd && cmd->speed != 0)
	{
		ADD_FIELD("Speed: %d\r\n", cmd->speed);
	}
    if (cmd && cmd->transport)
	{
		ADD_FIELD("Transport: %s;ServiceGroup=%d\r\n", cmd->transport,
                cmd->serviceGroupID);
	}

	if (cmd && cmd->x_RegionID)
	{
        ADD_FIELD("x-RegionID: %s\r\n", "2561");
	}

	if (cmd && cmd->x_Info)
	{
		ADD_FIELD("x-Info: %s\r\n", cmd->x_Info);
	}

	ADD_FIELD("User-Agent: %s\r\n", USER_AGENT);
}

static char* rtsp_proto_adjust(char* server_name, char* server_url)
{
    char *s;
    char *mediaName;
    char *url = server_url;

    s = strstr(url,"?");
    if (s != NULL) {
        *s = 0;
    }

    s = url + strlen("rtsp://");
    mediaName = strstr(s,"/");
    if (mediaName != NULL)
        mediaName += 1;
    sprintf(server_url, "rtsp://%s/%s", server_name, mediaName);
    return server_url;
}

int rtsp_send_cmd(const char *cmd_name, rtsp_client_t *client, rtsp_command_t *cmd, 
	const char* track_name)
{
	char buffer[SEND_BUFF_LEN];
	int len;
	int ret;
    char *cli_url = rtsp_strdup(client->url);
    
    cli_url = rtsp_proto_adjust(client->server_name, cli_url); 
	
    len = sprintf(buffer, "%s %s%s RTSP/1.0\r\n", cmd_name, cli_url, track_name);
	rtsp_build_common(buffer, &len, client, cmd);
	ret = sprintf(buffer + len, "\r\n");
 	len += ret;

    dTRACE("serverName %s server_port %d\n",client->server_name,client->server_port);
	dTRACE("\nrtsp send command %s [len=%d]: \n%s", cmd_name, len, buffer);
	ret = rtsp_send_sock(client, buffer, len);
	if (ret <= 0)
	{
		dTRACE("send data fail ret = %d\n\n",ret);
		free(cli_url);
        return -1;
	}
    
    free(cli_url);
	return 0;
}

