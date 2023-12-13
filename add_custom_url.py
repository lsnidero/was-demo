import sys
import os

global  AdminConfig

def find_url_provider():
    url_providers = AdminConfig.list('URLProvider').splitlines()
    url_provider = url_providers[0]
    print ("Selected URLProvider " + url_provider)
    return url_provider

def add_custom_url(url_provider, name, jndi_name, spec):
    url_resource = AdminConfig.create('URL', url_provider, [['name', name], ['jndiName', jndi_name], ['spec', spec]])
    print ("Created url " + url_resource)
    return url_resource

# Main
print ("Setting custom urls  ...")

# Find the right provider
url_provider = find_url_provider()

# Add custom URLs
conf_file = open('/tmp/custom-urls.csv', 'r')

i = 0
for line in conf_file.readlines():
    if i == 0:
        i = i + 1 
    else:
        url_config = line.split(",")
        name = url_config[1]
        jndi_name = url_config[2]
        spec = url_config[3]
        print ("Custom Url with name: " + name + " jndi " + jndi_name + " spec " + spec)
        add_custom_url(url_provider, name, jndi_name, spec)
    

#conf_file.close()


AdminConfig.save()
