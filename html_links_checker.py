"""
Html links checker
Check all the links in a given folder of htmls files
and out put the invalid links.
"""

from BeautifulSoup import BeautifulSoup
import glob
import os
import sys
import requests

requests.packages.urllib3.disable_warnings()

html_list = []
http_list = []
invalid_list = {}


def get_htmls(path):
    """
    Get all the html in the given folder.
    :param path:
    :return:
    """
    os.chdir(path)
    for file in glob.glob("*.html"):
        print(file)
        html_list.append(file)


def test_links():
    """
    Test all the links in htmls.
    :return:
    """
    for html in html_list:
        soup = BeautifulSoup(open(html))
        print('')
        print("NOW CHECKING:{}".format(html))
        for a in soup.findAll('a', href=True):
            link = a['href']

            # If link is http/https, send a request to test if it's valid
            if link.startswith("http"):
                if link.endswith('\\'):
                    link = link[:-1]

                if link not in http_list:
                    http_list.append(link)
                    try:
                        request = requests.get(link, verify=False)
                        if request.status_code == 404 or request.status_code == 403:
                            invalid_list[link] = request.status_code
                    except requests.exceptions.ConnectionError as e:
                        print("Error:{}, link:{}".format(str(e), link))

                if link in invalid_list:
                    print("Web site does not exist, error:{}, link:{}".format(invalid_list[link], link))

            # If it's a internal link, check the whole html page to see if the name or class can be find or not
            elif link.startswith("#"):
                anchor_name = link[1:]
                if not soup.find('a', attrs={'name': anchor_name}) and not soup.find(attrs={'id': anchor_name}):
                    print("Invalid link, anchor_name:{}, link_name:{}".format(anchor_name.encode('utf8'),
                                                                              link.encode('utf8')))

if __name__ == '__main__':
    print(sys.argv[0])
    get_htmls(sys.argv[1])
    test_links()

