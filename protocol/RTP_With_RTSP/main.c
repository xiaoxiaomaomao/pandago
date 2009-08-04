#include "rtsp.h"

int main()
{
    unsigned int handle = rtsp_create_handle("rtsp://192.168.0.99/fent.ts");
    unsigned int i = 0;
    rtsp_open(handle, 1);
    rtsp_play(handle, 0, 1);
    rtsp_pause(handle);
    rtsp_play(handle, 100,1);
    while(1)
    {;}
    return 0;
}
