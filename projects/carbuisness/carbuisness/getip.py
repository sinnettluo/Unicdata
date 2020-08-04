import requests

def getProxy():
    url = 'http://120.27.216.150.:5000'
    proxy = requests.get(url, auth=('admin', 'zd123456')).text
    return proxy

def main():
    get_proxy = getProxy()
    print(get_proxy)

if __name__=="__main__":
    main()
