#include "rtsp.h"



int main()
{
    int handle[20] = {0};  
    int i = 0;   
    int ret = 0;
    for (i  = 0; i < 20; i++) {
        handle[i] = rtsp_create_handle("rtsp://192.168.0.161/test.ts");
        ret = rtsp_open(handle[i], 1);
        if (ret < 0) {
            printf ("open rtsp client failed\n");
            return -1;
        }
        ret = rtsp_play(handle[i],0);
        if (ret < 0) 
            return -1;
    }

    while(1) {
        for (i = 0; i < 20; i++)
            rtsp_keepalive(handle[i]);
        printf("keeplive");

    }

    for (i = 0; i < 20; i++) 
    rtsp_close(handle[i]);
}
