/*--------------------------------------------------------

	COPYRIGHT 2007 (C) DVN (Holdings) Ltd (Hongkong)

	AUTHOR:		wangry@dvnchina.com
	PURPOSE:	kasenna simple rtsp lib
	CREATED:	2007-12-10

	MODIFICATION HISTORY
	Date        By     Details
	----------  -----  -------

--------------------------------------------------------*/
#include "rtsp_client.h"
#include <arpa/inet.h>
#include <netdb.h>
#include <fcntl.h>
#include <errno.h>

static int rtsp_lookup_server_address (rtsp_client_t *client)
{
	const char *server_name;
	in_port_t server_port;
	struct hostent *host;

	server_name = client->server_name;
	server_port = client->server_port;

	if (inet_aton(server_name, &client->server_addr) != 0)
	{
		return 0;
	}

	host = gethostbyname(server_name);
	if (host == 0)
	{
		RTSP_ERR("can't get host address, host=%s\n", server_name);
		return -1;
	}

	client->server_addr = *(struct in_addr*)host->h_addr;

	return 0;
}

int rtsp_create_socket (rtsp_client_t *client)
{
	struct sockaddr_in sockaddr;
	int sockfd;
	unsigned int block_flag;		
	int ret;

	if (client->server_socket != -1)
	{
		RTSP_ALERT("socket is opened\n");
		return 0;
	}

	if (client->server_name == 0)
	{
		RTSP_ERR("server name is null, create socket fail\n");
		return -1;
	}

	if (rtsp_lookup_server_address(client) != 0)
	{
		return -1;
	}

	client->server_socket = socket(AF_INET, SOCK_STREAM, 0);
	if (client->server_socket == -1)
	{
		RTSP_ERR("Couldn't create socket\n");
		return -1;
	}

	sockaddr.sin_family = AF_INET;
	sockaddr.sin_port = htons(client->server_port);
	sockaddr.sin_addr = client->server_addr;

	/*·ÀÖ¹connect¹ý³¤Ê±¼äµÄ×èÈû------------------------------------------*/
	ret = -1;
	sockfd = client->server_socket;
	
	block_flag = fcntl(sockfd, F_GETFL);
	fcntl(sockfd, F_SETFL, block_flag | O_NONBLOCK);

	if (connect(sockfd, (struct sockaddr *)&sockaddr, sizeof(sockaddr)) != 0)
	{
		if (errno == EINPROGRESS)
		{
			struct timeval t;
			fd_set set;
			t.tv_sec = 5;
			t.tv_usec = 0;

			FD_ZERO(&set);
			FD_SET(sockfd, &set);
			if (select(sockfd+1, 0, &set, 0, &t) > 0)
			{
				int error = -1;
	   			int len = sizeof(int);			
				getsockopt(sockfd, SOL_SOCKET, SO_ERROR, &error, &len);
				if (error == 0)
				{
					ret = 0;
				}
			} 
		}
	}
	else
	{
		ret = 0;
	}
	fcntl(sockfd, F_SETFL, block_flag);
	
	if (ret == -1)
	{
		close(sockfd);
		client->server_socket = -1;
		RTSP_ERR("couldn't connect socket, timeout 5 second\n");
		return -1;
	}
	return 0;
}

int rtsp_send_sock (rtsp_client_t *client, const char *buffer, int len)
{
	if (client->server_socket == -1)
	{
		RTSP_ERR("rtsp_send_sock: socket handle is -1\n");
		return -1;
	}
	
	return send(client->server_socket, buffer, len, 0);
}

int rtsp_receive_socket (rtsp_client_t *client, char *buffer, int len)
{
	int ret;
	fd_set read_set;
	struct timeval t;

	if (client->server_socket == -1)
	{
		RTSP_ERR("rtsp_receive_socket: socket handle is -1\n");
		return -1;
	}

	if (client->recv_timeout != 0)
	{
		FD_ZERO(&read_set);
		FD_SET(client->server_socket, &read_set);
		t.tv_sec = client->recv_timeout / 1000;
		t.tv_usec = (client->recv_timeout % 1000) * 1000;
		ret = select(client->server_socket + 1, &read_set, 0, 0, &t);
		if (ret <= 0)
		{
			RTSP_ALERT("socket recv timed out, timeout=%d ret=%d\n", client->recv_timeout, ret);
			return -1;
		}
	}

	ret = recv(client->server_socket, buffer, len, 0);
	return ret;
}


void rtsp_close_socket (rtsp_client_t *client)
{
	if (client->server_socket != -1)
	{
		shutdown(client->server_socket, SHUT_RDWR);
		close(client->server_socket);
	}
	client->server_socket = -1;
}

