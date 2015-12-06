#!/usr/bin/python
import urllib2
import json
import os

tld_port = os.environ.get('TLD_PORT', '80')
tld_host = os.environ.get('TLD_HOST', 'example.com')
etcd_host = os.environ.get('ETCD_HOST', '127.0.0.1')
base_url = "http://%s:4001/v2/keys" % etcd_host
response = urllib2.urlopen(base_url + "/services/nginx?recursive=true")
data = json.load(response)

upstreams = {}
for n in data['node']['nodes']:
    if 'nodes' in n:
        for node in n['nodes']:
            name, index = node['key'].split('/')[-2:]
            name_i = '%s-%s' % (name, index)
            url = node['value']
    
            if name not in upstreams:
                upstreams[name] = []
            upstreams[name].append(url)
    
            if name_i not in upstreams:
                upstreams[name_i] = []
            upstreams[name_i].append(url)

conf_upstreams = ["upstream %s { %s }" % (name, " ".join(["server %s;" % url for url in urls])) for name, urls in upstreams.items()]
conf_servers = ["server { listen %s; server_name %s.%s; location / { proxy_pass http://%s; }}" % (tld_port, name, tld_host, name) for name, _ in upstreams.items()]
# "http {\n%s\n%s\n}"
config = "%s\n%s\n" % ("\n".join(conf_upstreams), "\n".join(conf_servers))
print config
