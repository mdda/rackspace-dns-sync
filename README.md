# rackspace-dns-sync

Define your DNS setup in Python, and efficiently sync *only the changes* with Rackspace.

## Motivation

Rackspace is very generous in offering FREE cloud DNS services if you sign up for 
a cloud account (and there's no requirement for paying for other services either).
It probably works out for them financially, since their DNS service is pretty 
impressive on its own, and (for example) I was motivated to praise them here, and 
elsewhere...

But managing the DNS through the web interface seems like an anti-pattern, particularly
if one needs to manage a decent number of domains, with similar (but not identical) 
properties and have a few different servers, etc.  This is a common problem for anyone
that has collected a few domain names, put up a few landing pages, seen some 
services grow a little, moved hosting providers, etc.

This project includes a simple way of defining the mapping of names to 
the required DNS entries programmatically (which means that it can be tracked 
via ```git```, for instance).  

And, using those definitions, allows for intelligent syncing with Rackspace - 
only updating the entries that require changes - which makes the whole process 
much more responsive (since downloading current state and then uploading 
differences is much quicker than simply re-sending 'already known' facts).

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

### Creating the Credentials File

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


### Checking it worked...

To confirm a Zone (look for name server claims):

```
dig @dns1.stabletransit.com example.com
```
