# rackspace-dns-sync

Define your DNS setup in Python, and sync only the changes with Rackspace (for speed).

## Motivation


The system has been in use for over 12 months, and works really nicely...


## Installation

```
sudo yum install python-virtualenv 

cd .  # pwd = <REPO>/
virtualenv env
. env/bin/activate

pip install pyrax

# Necessary if you get a pyrax.exceptions.IdentityClassNotDefined exception
pip install --upgrade git+git://github.com/rackspace/pyrax.git
```

## Creating the Credentials File

After reading through http://www.collazo.ws/2011/07/08/using-rackspace-dnsaas-with-curl-part-1 
you should make sure that you can get your Authorization Token (returned in the ```X-Auth-Token: ``` line) 
from your login (```X-Auth-User```) and API Key (```X-Auth-Key```) by filling them 
into the following (and then putting the result into ```user_credentials.NOGIT``` 
in the same format as the included ```user_credentials.SAMPLE```) :

```
curl -D - \
   -H "X-Auth-User: myusername" \
   -H "X-Auth-Key: 01234567890abcdef01234567890abcdef" \
   https://auth.api.rackspacecloud.com/v1.0 \
   | grep X-Auth-Token:
```



## Running

After reading, understanding and modifying the ```ensure_dns.py``` file, run the sync with :

```
cd .  # pwd = <REPO>/
virtualenv env
. env/bin/activate

python ensure_dns.py
```

This will print out debug messages as it goes along.


## Checking it worked...

To confirm a Zone (look for name server claims):

```
dig @dns1.stabletransit.com example.com
```
