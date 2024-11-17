# -*- coding: utf-8 -*-
# coding: utf-8
#!/usr/bin/python3
# this program is run by Python3
import sys
import os
import urllib3
import webbrowser

print('-----> 欢迎使用酷我音乐!')

def getMp3Datas(key, page, size):
    http = urllib3.PoolManager() 
    # headers = {
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)',
    # 'Host':'httpbin.org'}
    # data = {'word':'hello'}
    # data = json.dumps(data).encode()  # json.dumps方法可以将python对象转换为json对象
    url = "http://search.kuwo.cn/r.s?uid=2473669294&ver=kwplayer_ip_10.2.2.0&locationid=1&prod=kwplayer_ip_10.2.2.0&source=kwplayer_ip_10.2.2.0_TJ.ipa&q36=cfe7df7a47b79fdfef3824ee00001aa1480a&client=kt&cluster=0&strategy=2012&ver=mbox&show_copyright_off=1&encoding=utf8&rformat=json&mobi=1&vipver=1&pn={1}&rn={2}&newver=3&searchNo=2473669294{0}1653722221753&vermerge=1&issubtitle=1&correct=1&all={0}&ft=music&spPrivilege=0&searchapi=5".format(key, page, size)
    response = http.request('GET', url)
    if response.status != 200:
       print("------>", response)
       sys.exit(1)
    res_str = response.data.decode('utf-8')
    dic = eval(res_str)
    return dic
    
def getPlayUrl(mid):
    http = urllib3.PoolManager() 
    url = "http://antiserver.kuwo.cn/anti.s?type=convert_url&rid={0}&format=mp3|acc&response=url".format(mid)
    response = http.request('GET', url)
    if response.status != 200:
       print("------>", response)
       sys.exit(1)   
    return response.data.decode('utf-8')

def startListen(abslist):
    mIndex = int(input("-----> 输入0重新搜索,输入歌曲编号开始听歌🎧:"))
    if mIndex == 0:
       main()
       return 
    listIndex = mIndex - 1    
    while listIndex >= len(abslist) | listIndex < 0:
        listIndex = int(input("-----> 编号不合法,请从新输入歌曲编号开始听歌🎧:"))
    selectDic = abslist[listIndex]
    playUrl = getPlayUrl(selectDic["MUSICRID"])
    webbrowser.open_new_tab(playUrl) 
    startListen(abslist)

def getInputKeyAbslist():
    key = input("-----> 请输入关键词搜索音乐:")
    print("-----> 请稍等...") 
    dic = getMp3Datas(key, 0, 30)
    abslist = dic['abslist']
    for index in range(len(abslist)):
        item = abslist[index]
        print("-----> ",index + 1, "," , item["SONGNAME"],"-",item["ARTIST"])
    return abslist    
    
def main(argv=None):
    abslist = getInputKeyAbslist()
    startListen(abslist) 

if __name__ == "__main__":
    sys.exit(main())