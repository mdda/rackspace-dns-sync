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

# Necessary for pyrax.exceptions.IdentityClassNotDefined exception
pip install --upgrade git+git://github.com/rackspace/pyrax.git
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


To confirm a Zone (look for name server claims):

```
dig @dns1.stabletransit.com example.com
```
