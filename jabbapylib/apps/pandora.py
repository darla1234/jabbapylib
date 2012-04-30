#!/usr/bin/env python

"""
Made specifically for listening to Pandora Radio outside of US.
Requirements:
* Firefox browser
* FoxyProxy add-on for Firefox

In FoxyProxy create a custom proxy, where the URL 
pattern is *www.pandora.com/* . FoxyProxy has an XML
config file called foxyproxy.xml .

Launch this script. It will find a fast US proxy and it
will write its IP and port to foxyproxy.xml . 
Restart the browser, thus FoxyProxy will see the new
configuration.
Go to pandora.com and enjoy the music :)  
"""

import os
from jabbapylib.platform import platform
from lxml import etree

XML = 'foxyproxy.xml'
BAK = 'foxyproxy.bak'

def get_best_proxy():
    from proxies import extract_list, filter, get_working_proxies
    import operator
    #
    proxies = extract_list()
    proxies = filter(proxies)    
    working = get_working_proxies(proxies)
    working.sort(key=operator.attrgetter("avg_time"), reverse=False)
    return working[0]

def foxyproxy(ip, port):
    folder = platform.get_firefox_profile_folder()
    input = folder + '/' + XML
    if not os.path.exists(input):
        print >>sys.stderr, "Error: {file} doesn't exist".format(file=input)
    # else
    with open(input) as f:
        content = f.read()
    root = etree.fromstring(content)
    manualconf = root.xpath('/foxyproxy/proxies[1]/proxy[1]/manualconf[1]')[0]
    manualconf.attrib['host'] = ip
    manualconf.attrib['port'] = port
    #
    os.rename(input, folder + '/' + BAK)
    #
    tree = etree.ElementTree(root)
    if os.path.exists(folder + '/' + BAK):
        tree.write(input, pretty_print=True, xml_declaration=True)
        print '# written to', XML
        print '# please restart Firefox'

def main():
    proxy = get_best_proxy().ip
#    proxy = '97.65.200.194:8080'    # for testing only
    print '#', proxy
    ip = proxy
    port = ""
    if ':' in proxy:
        ip, port = proxy.split(':')

    foxyproxy(ip, port)
    
#############################################################################

if __name__ == "__main__":
    main()