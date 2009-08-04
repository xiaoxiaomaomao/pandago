#include "rtsp_client.h"
#include "rtsp_sock.h"
#include "rtsp_response.h"
#include "rtsp_util.h"
#include "rtsp.h"
#define SEPERATOR "\r\n"
#define isspace(a) (a == '\r' || a == '\n' || a == ' ' || a == '\t')
#define SKIP_SPACE(a) {while (isspace(*(a)) && (*(a) != '\0'))(a)++;}
#define SET_DEC_FIELD(a) set_dec_field(&dec->a, line)
static void set_dec_field (char **field, const char *line)
{
	if (*field == 0)
	{
		*field = rtsp_strdup((char*)line);
	}
	else
	{
		RTSP_ERR("decoder fileld exist, old:%s new:%s\n", *field, line);
	}
}

#define RTSP_HEADER_FUNC(a) static void a (const char *line, rtsp_resp_t *dec, rtsp_client_t* rtsp_client)
RTSP_HEADER_FUNC(rtsp_header_allow_public)
{
	SET_DEC_FIELD(allow_public);
}
RTSP_HEADER_FUNC(rtsp_header_connection)
{
	if (strncasecmp(line, "close", strlen("close")) == 0)
	{
		dec->close_connection = 1;
	}
	else
	{
		dec->close_connection = 0;
	}
}
RTSP_HEADER_FUNC(rtsp_header_cookie)
{
	SET_DEC_FIELD(cookie);
}
RTSP_HEADER_FUNC(rtsp_header_content_base)
{
	SET_DEC_FIELD(content_base);
}
RTSP_HEADER_FUNC(rtsp_header_content_length)
{
	dec->content_length = atoi(line);
}
RTSP_HEADER_FUNC(rtsp_header_content_loc)
{
	SET_DEC_FIELD(content_location);
}
RTSP_HEADER_FUNC(rtsp_header_content_type)
{
	SET_DEC_FIELD(content_type);
}
RTSP_HEADER_FUNC(rtsp_header_cseq)
{
	dec->cseq = atoi(line);
}
RTSP_HEADER_FUNC(rtsp_header_location)
{
	SET_DEC_FIELD(location);
}
RTSP_HEADER_FUNC(rtsp_header_range)
{
	SET_DEC_FIELD(range);
}
RTSP_HEADER_FUNC(rtsp_header_retry_after)
{
	SET_DEC_FIELD(retry_after);
}
RTSP_HEADER_FUNC(rtsp_header_rtp)
{
	SET_DEC_FIELD(rtp_info);
}
RTSP_HEADER_FUNC(rtsp_header_session)
{
	SET_DEC_FIELD(session);
}
RTSP_HEADER_FUNC(rtsp_header_speed)
{
	SET_DEC_FIELD(speed);
}

RTSP_HEADER_FUNC(rtsp_header_transport)
{
    SET_DEC_FIELD(transport);
    rtsp_client_t* client = (rtsp_client_t*)(dec->handle);
    client->paramsFromServer = malloc(strlen(line) + 1);
    strcpy(client->paramsFromServer, line);
}

RTSP_HEADER_FUNC(rtsp_header_www)
{
	SET_DEC_FIELD(www_authenticate);
}
RTSP_HEADER_FUNC(rtsp_header_accept)
{
	SET_DEC_FIELD(accept);
}
RTSP_HEADER_FUNC(rtsp_header_accept_enc)
{
	SET_DEC_FIELD(accept_encoding);
}
RTSP_HEADER_FUNC(rtsp_header_accept_lang)
{
	SET_DEC_FIELD(accept_language);
}
RTSP_HEADER_FUNC(rtsp_header_auth)
{
	SET_DEC_FIELD(authorization);
}
RTSP_HEADER_FUNC(rtsp_header_bandwidth)
{
	SET_DEC_FIELD(bandwidth);
}
RTSP_HEADER_FUNC(rtsp_header_blocksize)
{
	SET_DEC_FIELD(blocksize);
}
RTSP_HEADER_FUNC(rtsp_header_cache_control)
{
	SET_DEC_FIELD(cache_control);
}
RTSP_HEADER_FUNC(rtsp_header_content_enc)
{
	SET_DEC_FIELD(content_encoding);
}
RTSP_HEADER_FUNC(rtsp_header_content_lang)
{
	SET_DEC_FIELD(content_language);
}
RTSP_HEADER_FUNC(rtsp_header_date)
{
	SET_DEC_FIELD(date);
}
RTSP_HEADER_FUNC(rtsp_header_expires)
{
	SET_DEC_FIELD(expires);
}
RTSP_HEADER_FUNC(rtsp_header_from)
{
	SET_DEC_FIELD(from);
}
RTSP_HEADER_FUNC(rtsp_header_ifmod)
{
	SET_DEC_FIELD(if_modified_since);
}
RTSP_HEADER_FUNC(rtsp_header_lastmod)
{
	SET_DEC_FIELD(last_modified);
}
RTSP_HEADER_FUNC(rtsp_header_proxyauth)
{
	SET_DEC_FIELD(proxy_authenticate);
}
RTSP_HEADER_FUNC(rtsp_header_proxyreq)
{
	SET_DEC_FIELD(proxy_require);
}
RTSP_HEADER_FUNC(rtsp_header_referer)
{
	SET_DEC_FIELD(referer);
}
RTSP_HEADER_FUNC(rtsp_header_scale)
{
	SET_DEC_FIELD(scale);
}
RTSP_HEADER_FUNC(rtsp_header_server)
{
	SET_DEC_FIELD(server);
}
RTSP_HEADER_FUNC(rtsp_header_unsup)
{
	SET_DEC_FIELD(unsupported);
}
RTSP_HEADER_FUNC(rtsp_header_uagent)
{
	SET_DEC_FIELD(user_agent);
}
RTSP_HEADER_FUNC(rtsp_header_via)
{
	SET_DEC_FIELD(via);
}
RTSP_HEADER_FUNC(rtsp_header_x_Info)
{
	SET_DEC_FIELD(x_Info);
}
RTSP_HEADER_FUNC(rtsp_header_x_Reason)
{
	SET_DEC_FIELD(x_Reason);
}
RTSP_HEADER_FUNC(rtsp_header_notices)
{
    if (strcmp("EOS", line) == 0) {
        rtsp_client->state = RTSP_PLAYER_CLOSE;
    }

    if (strcmp("BOS",line) == 0) {
        rtsp_client->state = RTSP_PLAYER_CLOSE;
    }

    if (strcmp("TOT",line) == 0) {
        rtsp_client->state = RTSP_PLAYER_CLOSE;
    }
}

static struct
{
	const char *val;
	int val_length;
	void (*parse_routine)(const char *line, rtsp_resp_t *decode, rtsp_client_t* client);
} header_types[] =
{
#define HEAD_TYPE(a, b) { a, sizeof(a) - 1, b }
	HEAD_TYPE("AlLow", rtsp_header_allow_public),
	HEAD_TYPE("Public", rtsp_header_allow_public),
	HEAD_TYPE("Connection", rtsp_header_connection),
	HEAD_TYPE("Content-Base", rtsp_header_content_base),
	HEAD_TYPE("Content-Length", rtsp_header_content_length),
	HEAD_TYPE("Content-Location", rtsp_header_content_loc),
	HEAD_TYPE("Content-Type", rtsp_header_content_type),
	HEAD_TYPE("CSeq", rtsp_header_cseq),
	HEAD_TYPE("Location", rtsp_header_location),
	HEAD_TYPE("Range", rtsp_header_range),
	HEAD_TYPE("Retry-After", rtsp_header_retry_after),
	HEAD_TYPE("RTP-client", rtsp_header_rtp),
	HEAD_TYPE("Session", rtsp_header_session),
	HEAD_TYPE("Set-Cookie", rtsp_header_cookie),
	HEAD_TYPE("Speed", rtsp_header_speed),
	HEAD_TYPE("Transport", rtsp_header_transport),
	HEAD_TYPE("WWW-Authenticate", rtsp_header_www),
	HEAD_TYPE("Accept", rtsp_header_accept),
	HEAD_TYPE("Accept-Encoding", rtsp_header_accept_enc),
	HEAD_TYPE("Accept-Language", rtsp_header_accept_lang),
	HEAD_TYPE("Authorization", rtsp_header_auth),
	HEAD_TYPE("Bandwidth", rtsp_header_bandwidth),
	HEAD_TYPE("Blocksize", rtsp_header_blocksize),
	HEAD_TYPE("Cache-Control", rtsp_header_cache_control),
	HEAD_TYPE("Content-Encoding", rtsp_header_content_enc),
	HEAD_TYPE("Content-Language", rtsp_header_content_lang),
	HEAD_TYPE("Date", rtsp_header_date),
	HEAD_TYPE("Expires", rtsp_header_expires),
	HEAD_TYPE("From", rtsp_header_from),
	HEAD_TYPE("If-Modified-Since", rtsp_header_ifmod),
	HEAD_TYPE("Last-Modified", rtsp_header_lastmod),
	HEAD_TYPE("Proxy-Authenticate", rtsp_header_proxyauth),
	HEAD_TYPE("Proxy-Require", rtsp_header_proxyreq),
	HEAD_TYPE("Referer", rtsp_header_referer),
	HEAD_TYPE("Scale", rtsp_header_scale),
	HEAD_TYPE("Server", rtsp_header_server),
	HEAD_TYPE("Unsupported", rtsp_header_unsup),
	HEAD_TYPE("User-Agent", rtsp_header_uagent),
	HEAD_TYPE("Via", rtsp_header_via),
	HEAD_TYPE("x-Info", rtsp_header_x_Info),
	HEAD_TYPE("x-Reason", rtsp_header_x_Reason),
	HEAD_TYPE("Notice",rtsp_header_notices),
    { 0, 0, 0 },
};


static void rtsp_decode_header (const char *line, rtsp_resp_t *response, rtsp_client_t* client)
{
	int i;
	const char *after;

	i = 0;
	while (header_types[i].val != 0)
	{
		if (strncasecmp(line, header_types[i].val, header_types[i].val_length) == 0)
		{
			after = line + header_types[i].val_length;
			SKIP_SPACE(after);

			if (*after == ':')
			{
				after++;
				SKIP_SPACE(after);
				(header_types[i].parse_routine)(after, response,client);
				return;
			}
		}
		i++;
	}
	RTSP_ALERT("%s [not processing]\n", line);
}

static int buffer_read (rtsp_client_t *client, int len)
{
	assert(client->m_buffer_len + len <= RECV_BUFF_DEFAULT_LEN);

	int ret;
	ret = rtsp_receive_socket(client,
								client->m_recv_buffer + client->m_buffer_len,
								len);
	dTRACE("rtsp_receive_socket...........\n");
    if (ret <= 0) 
	{
		return ret;
	}
	client->m_buffer_len += ret;
	client->m_recv_buffer[client->m_buffer_len] = '\0';

	return ret;
}

static int buffer_read_all (rtsp_client_t *client)
{
	return buffer_read(client, RECV_BUFF_DEFAULT_LEN - client->m_buffer_len);
}

static int buffer_len (rtsp_client_t *client)
{
	int ret = client->m_buffer_len - client->m_offset_on;
	assert(ret >= 0 && ret <= RECV_BUFF_DEFAULT_LEN);
	return ret;
}

static void buffer_move_head (rtsp_client_t *client)
{
	int len;
	len = client->m_buffer_len - client->m_offset_on;
	if (len > 0)
	{
		memmove(client->m_recv_buffer,
		  		client->m_recv_buffer + client->m_offset_on,
		  		len);
	}
	client->m_offset_on = 0;
	client->m_buffer_len = len;
	dTRACE("=====> move memory size = %d\n", len);	
}

static int buffer_move_and_read_all (rtsp_client_t *client)
{
	if (buffer_len(client) == RECV_BUFF_DEFAULT_LEN)
	{
		dTRACE("buffer is full when read, len=%d\n", RECV_BUFF_DEFAULT_LEN);
		return RECV_BUFF_DEFAULT_LEN;
	}
	buffer_move_head(client);
	buffer_read_all(client);

	return buffer_len(client);
}

static const char *get_next_line (rtsp_client_t *client)
{
	int ret;
	char *sep;

	if (buffer_len(client) == 0)
	{
		if (buffer_move_and_read_all(client) == 0)
		{
			return 0;
		}		
	}

	sep = strstr(client->m_recv_buffer + client->m_offset_on, SEPERATOR);
	if (sep != 0)
	{
		const char *retval = client->m_recv_buffer + client->m_offset_on;
		client->m_offset_on = sep - client->m_recv_buffer;
		client->m_offset_on += strlen(SEPERATOR);
		*sep = '\0';
		return retval;
	}

	if (client->m_offset_on == 0)
	{
		dTRACE("====> have no seperator in full buffer\n");	
		return 0;
	}
	
	if (buffer_move_and_read_all(client) == 0)
	{
		dTRACE("====> read fail after have no seperator in full buffer\n");	
		return 0;
	}

	sep = strstr(client->m_recv_buffer + client->m_offset_on, SEPERATOR);
	if (sep != 0)
	{
		const char *retval = client->m_recv_buffer + client->m_offset_on;
		client->m_offset_on = sep - client->m_recv_buffer;
		client->m_offset_on += strlen(SEPERATOR);
		*sep = '\0';
		dTRACE("====> get seperator at second try\n");	
		return retval;
	}

	dTRACE("====> have no seperator in full buffer at second read\n");	
	return 0;
}

int rtsp_recv_response (rtsp_client_t *client, rtsp_resp_t *response)
{
	const char *line;
	const char *p;
	rtsp_resp_t *decode;
	int done;
	int len;

	decode = response;
	
	if (buffer_move_and_read_all(client) == 0)
	{
		dTRACE("#######string buffer is null and no data recv\n");
		return -1;
	}

	do 
	{
		line = get_next_line(client);
		if (line == 0)
		{
			dTRACE("couldn't get response first line\n");
			return -1;
		}
	}
	while (*line == '\0');

	if (strncasecmp(line, "RTSP/1.0", strlen("RTSP/1.0")) != 0)
	{
		char str[20];
		
		p = line;
		while ( *p != ' ')
		{
			p++;
		}
		memcpy(str, line, p - line);
		str[p-line] = '\0';
		decode->caption = rtsp_strdup(str);
	}
	else
	{
		p = line + strlen("RTSP/1.0");
		SKIP_SPACE(p);
		memcpy(decode->retcode, p, 3);
		decode->retcode[3] = '\0';
		p += 3;
		SKIP_SPACE(p);
		decode->retresp = rtsp_strdup((char*)p);
		decode->caption = rtsp_strdup("RTSP/1.0");
	}

	done = 0;
	do
	{
		line = get_next_line(client);
		if (line == 0)
		{
			dTRACE("couldn't get line from response content\n");
			return -1;
		}

		if (*line != '\0')
		{
			rtsp_decode_header(line, response, client);
		}
		else
		{
            dTRACE("done ======= 1\n");
			done = 1;
		}
	}
	while (done == 0);
	if (decode->content_length != 0)
	{
		decode->body = (char*)malloc(decode->content_length + 1);
		decode->body[decode->content_length] = '\0';
		len = buffer_len(client);
		dTRACE("response body length=%d, current buffer size=%d, offset=%d\n", decode->content_length, len, client->m_offset_on);

		if (len < decode->content_length)
		{
			memcpy(decode->body, client->m_recv_buffer + client->m_offset_on, len);
			while (len < decode->content_length)
			{
				int left;
				int ret;

				client->m_offset_on = 0;
				client->m_buffer_len = 0;
				ret = buffer_read_all(client);
                if (ret <= 0)
				{
					dTRACE("recv fail at get rtsp body\n");
					return -1;
				}
                
				left = decode->content_length - len;
				if (left < client->m_buffer_len)
				{
					memcpy(decode->body + len, client->m_recv_buffer, left);
					len += left;
					client->m_offset_on = left;
				}
				else
				{
					memcpy(decode->body + len, client->m_recv_buffer, client->m_buffer_len);
					len += client->m_buffer_len;
					client->m_offset_on = client->m_buffer_len;
				}
			}
		}
		else
		{
			memcpy(decode->body, client->m_recv_buffer + client->m_offset_on, decode->content_length);
			client->m_offset_on += decode->content_length;
		}
	}

	if (decode->body != 0)
	{
        dTRACE("%s", decode->body);
	}

	dTRACE("complete recv response, buffer state: offset=%d len=%d\n", client->m_offset_on, buffer_len(client));

	return 0;
}
void clear_response (rtsp_resp_t *resp)
{
	CHECK_AND_FREE(resp->caption);
	CHECK_AND_FREE(resp->retresp);
	CHECK_AND_FREE(resp->body);
	CHECK_AND_FREE(resp->accept);
	CHECK_AND_FREE(resp->accept_encoding);
	CHECK_AND_FREE(resp->accept_language);
	CHECK_AND_FREE(resp->allow_public);
	CHECK_AND_FREE(resp->authorization);
	CHECK_AND_FREE(resp->bandwidth);
	CHECK_AND_FREE(resp->blocksize);
	CHECK_AND_FREE(resp->cache_control);
	CHECK_AND_FREE(resp->content_base);
	CHECK_AND_FREE(resp->content_encoding);
	CHECK_AND_FREE(resp->content_language);
	CHECK_AND_FREE(resp->content_location);
	CHECK_AND_FREE(resp->content_type);
	CHECK_AND_FREE(resp->date);
	CHECK_AND_FREE(resp->cookie);
	CHECK_AND_FREE(resp->expires);
	CHECK_AND_FREE(resp->from);
	CHECK_AND_FREE(resp->if_modified_since);
	CHECK_AND_FREE(resp->last_modified);
	CHECK_AND_FREE(resp->location);
	CHECK_AND_FREE(resp->proxy_authenticate);
	CHECK_AND_FREE(resp->proxy_require);
	CHECK_AND_FREE(resp->range);
	CHECK_AND_FREE(resp->referer);
	CHECK_AND_FREE(resp->require);
	CHECK_AND_FREE(resp->retry_after);
	CHECK_AND_FREE(resp->rtp_info);
	CHECK_AND_FREE(resp->scale);
	CHECK_AND_FREE(resp->server);
	CHECK_AND_FREE(resp->session);
	CHECK_AND_FREE(resp->speed);
	CHECK_AND_FREE(resp->transport);
	CHECK_AND_FREE(resp->unsupported);
	CHECK_AND_FREE(resp->user_agent);
	CHECK_AND_FREE(resp->via);
	CHECK_AND_FREE(resp->www_authenticate);
	CHECK_AND_FREE(resp->x_Info);
	CHECK_AND_FREE(resp->x_Reason);
	resp->content_length = 0;
	resp->cseq = 0;
	resp->close_connection = 0;
}

/*
a=Range:npt=0.000000-5952.960000
a=x-frequency:xxxxxxx
a=x-pid:xxx
*/
void simple_parse_sdp(char* sdp, int* range, int* freq, int* pid,int* controlId, int* symbolRate, int* modulation,int* programNumber)
{
    char* p;

    RTSP_DBG("======>begin parse sdp\n");

    p = strstr(sdp, "npt=");
    p+=4;
    p = strchr(p, '-');
    p++;
    *range = atoi(p);

    p = strstr(sdp, "frequency=");
    p+=10;
    *freq = atoi(p);

    p = strstr(sdp, "x-pid:");
    p+=6;
    *pid = atoi(p);

    p = strstr(sdp,"control:track");
    p += 13;

    *controlId = atoi(p);

    RTSP_DBG("=========> parse sdp: range=%d freq=%d pid=%d\n", *range, *freq, *pid);
}


