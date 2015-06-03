#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pyrax
import pyrax.exceptions as exc

import RackspaceDNS

creds_file = "./user_credentials.NOGIT"
pyrax.settings.set('identity_type', 'rackspace')
pyrax.set_credential_file(creds_file)

dns_config = RackspaceDNS.Config(pyrax.cloud_dns, 30)

defaults = {
  "A":{
    "ttl": 6000,
  },
  "MX":{
    "priority": 10,
    "comment": "Mail server",
    "data": "mail.%",
  },
  "TXT":{ # Enable email to be google 'verified'
    #"data":"v=spf1 a a:gmail.com -all", 
    "data":"v=spf1 mx include:_spf.google.com ~all", 
  },
}

# Standardize VPS ip definitions
ip_ex1  = "111.222.33.44"  
ip_ex2  = "111.222.33.55"  

verifications= {
  'example.com':                  "google-site-verification=-Noaz7W2cm5p_ZuF7GiHkzoVy5DsEWp_3UXCasasds",
}

for site in [
             'example.com', 'example.net', 
            ]:
    dns_config.upsert_domain(site, emailAddress="RackSpaceDNS@example.com", ttl=900, comment="Example Domains")
    
    recs =     [
      { "type": "A", }, 
      { "type": "A", "name": "www.%", }, 
      
      { "type": "MX", },
      { "type": "A", "name": "mail.%", }, 

      { "type": "MX", "data":"mail2.%", },
      #{ "type": "A", "name": "mail2.%", "data": ip_b3a, }, 
      { "type": "A", "name": "mail2.%", "data": ip_d1, }, 

      { "type": "TXT", },
    ]
    if site in verifications:
        recs.append( { "type": "TXT", "data":verifications[site], } )
        
    dns_config.upsert_records(site, [ defaults, 
        {
         "A":{ "data": ip_ex1, },    
         #"A":{ "data": ip_ex2, },    # Still in old location TODO
        }
    ], recs)



### https://mycloud.rackspace.com/a/mdda123/dns#
### https://github.com/rackspace/pyrax/tree/master/samples/cloud_dns
### https://github.com/rackspace/pyrax/blob/master/docs/cloud_dns.md
