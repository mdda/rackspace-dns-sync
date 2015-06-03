
import pyrax
import pyrax.exceptions as exc

class Config():
    dns = None
 
     # This caches the value...
    domain_dictionary=None

    def __init__(self, _dns, _timeout=10):
        self.dns = _dns
        self.dns.set_timeout(_timeout)

        
    def get_domain_dictionary(self):
        l=dict()
        for domain in self.dns.get_domain_iterator():
            l[domain.name]=domain
        return l
        
    def upsert_domain(self, name, emailAddress=None, ttl=900, comment=""):
        if self.domain_dictionary is None:
            self.domain_dictionary = self.get_domain_dictionary()
            
        if emailAddress is None: emailAddress = "admin@%s" % name
        
        print "Domain %s" % name
        if name in self.domain_dictionary:
            dom = self.domain_dictionary[name]
            
            # detect whether we need to update
            changes=dict(name=name, emailAddress=emailAddress, comment=comment, ttl=ttl)
            for k,v in changes.items():
                if getattr(dom, k) == v:
                    print "  No change to %s" % k
                    del changes[k]
                else:
                    print "  Change to %s (%s -> %s)" % (k, getattr(dom, k), changes[k])

            if len(changes)>0:
                try:
                    self.domain_dictionary[name].update(emailAddress=emailAddress, ttl=ttl, comment=comment)
                    print "  Domain %s updated" % name
                except exc.DomainCreationFailed as e:
                    print "  Domain update failed:", e
                    exit()
            else:
                print "  Domain %s no changes" % name
        else:
            # Add the new domain
            try:
                dom = self.dns.create(name=name, emailAddress=emailAddress, ttl=ttl, comment=comment)
                print "  Domain %s created" % name
                self.domain_dictionary[name]=dom
            except exc.DomainCreationFailed as e:
                print "  Domain creation failed:", e
                exit()

    def overlay_record_info(self, name, overlays, rec_list):
        rec_list_final = list()
        for r in rec_list:
            if not 'name' in r: r['name']=name
            t = r['type']    
            
            # Fill in all the entries from the defaults, plus overlay, plus given values
            build_up=dict()
            for overlay in overlays:
                if t in overlay:
                    build_up.update(overlay[t])
                
            build_up.update(r)
            r = build_up # Here's the final, filled in version
            
            if t =='A' or t=='TXT' or t=='CNAME':
                r['name'] = r['name'].replace('%', name)
                
            if t =='MX':
                r['data'] = r['data'].replace('%', name)

            #print "  Record : %s" % (repr(r))
            rec_list_final.append(r)
            
        return rec_list_final


    def upsert_records(self, name, overlays, rec_list):  ## NB: name must be an existing (sub)domain
        rec_list=self.overlay_record_info(name, overlays, rec_list)
        #exit()
        
        dom = self.domain_dictionary[name]
        
        existing_recs = self.dns.get_record_iterator(dom)
        
        # Iterate through the existing records, and see whether they're in the updates (and match precisely)
        #  if so, then do nothing (don't delete on the server, and don't send an add_records either)
        #  if they're not in the updates list precisely, remember to delete them
        existing_recs_to_delete=[]
        rec_list_delete_indices=[]
        for existing_rec in existing_recs:
            if existing_rec.type == "NS":
                # Don't change these; they are automatic & required
                continue
                
            ## Find the existing_rec in the rec_list (if possible)
            found_existing_rec=False
            for i,r in enumerate(rec_list):
                found=True
                for k,v in r.items():
                    if hasattr(existing_rec, k) and getattr(existing_rec, k)==v:
                        # This value matches exactly
                        pass
                    else:
                        found=False
                if found:
                    # This is an exact match r === existing_rec
                    print "  No need to change record %s" % (repr(r))
                    rec_list_delete_indices.append(i)
                    found_existing_rec=True
                    
            if not found_existing_rec:
                #print "  Changes required for %s" % (repr(existing_rec))
                existing_recs_to_delete.append(existing_rec)
        
        # This list is just the updated/unwanted entries - delete them via the API
        for existing_rec in existing_recs_to_delete:
            existing_rec.delete()

        rec_list_updates=[]
        for i,r in enumerate(rec_list):
            if not i in rec_list_delete_indices:
                print "  Updating %s" % (repr(r))
                rec_list_updates.append(r)
            
        #print 
        #print repr(rec_list_updates)
        #exit()
        
        # This list has had all the existing (unchanged) entries removed already
        if len(rec_list_updates)>0:
            dom.add_records(rec_list_updates)
