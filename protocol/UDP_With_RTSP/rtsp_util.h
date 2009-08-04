#ifndef _RTSP_UTIL_H_
#define _RTSP_UTIL_H_ 

#ifdef __cplusplus
extern "C" 
{
#endif
char* rtsp_strdup(const char* str);

#define rtsp_isdigit(_c) ((_c >= '0' && _c <= '9') ? 1:0)

#ifdef __cplusplus
}
#endif

#endif


