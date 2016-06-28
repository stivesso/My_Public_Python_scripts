#!/usr/bin/python

import os
import sys

## Some global variables
SPACE_CHAR = " "
DNS_RECORD_TYPE = ['A','AAAA','AFSDB','APL','CAA','CDNSKEY','CDS','CERT','CNAME','DHCID','DLV','DNAME','DNSKEY','DS','HIP','IPSECKEY','KEY','KX','LOC','MX','NAPTR','NS','NSEC','NSEC3','NSEC3PARAM','PTR','RRSIG','RP','SIG','SOA','SRV','SSHFP','TA','TKEY','TLSA','TSIG','TXT','URI']


## Helper Functions
def check_args(lst):
    """The aim of this is to check that we have enough arguments"""
    # Must have at least as first argument the zone file to turn to yaml
    if len(lst) < 3 or not os.path.isfile(lst[1]):
        print "This script needs at least a valid zone file path as argument"
        print "Its usage is", sys.argv[0], " zonefile_path  domain_name"
        print "zonefile_path being the path to the zone file and domain_name the domain name"
        sys.exit("Insufficient Number of Arguments")

def check_A_records(zonefile_list):
    for line in zonefile_list:
        print (SPACE_CHAR * 4) + "'" + line[1].split()[0] + "'"
        print (SPACE_CHAR * 6) + "owner"
        print (SPACE_CHAR * 8) + "'" + line[1].split()[-1] + "'"

def check_MX_records(zonefile_list,zonename):
    index = 1
    for line in zonefile_list:
        print (SPACE_CHAR * 2) + "-"
        print (SPACE_CHAR * 4) + "mxnamevar                : 'Mail Server", index, "for" + zonename + "'"
        print (SPACE_CHAR * 4) + "zone                     : '" + zonename + "'"
        print (SPACE_CHAR * 4) + "owner                    : '" + line[1].split()[0] + "'"
        print (SPACE_CHAR * 4) + "priority                 : '" + line[1].split()[line[1].split().index("MX") + 1] + "'"
        print (SPACE_CHAR * 4) + "host                     : '" + line[1].split()[-1] + "'"
        index += 1

def check_OTHERS_records(zonefile_list,zonename):
    others_type_list = set([record for line in zonefile_list for record in DNS_RECORD_TYPE if record in line[1]])
    for other_type in others_type_list:
        print (SPACE_CHAR * 2) + "-"
        print (SPACE_CHAR * 4) + "namevar                  : '" + str(other_type) + " for " + zonename + "'"
        print (SPACE_CHAR * 4) + "record_type              : '" + str(other_type) + "'"
        print (SPACE_CHAR * 4) + "hash_data                :"
        for line in zonefile_list:
            if other_type in line[1].split():
                idx_after_other_type = line[1].split().index(other_type) + 1
                print (SPACE_CHAR * 6) + "'" + line[1].split()[0] + "'  :"
                print (SPACE_CHAR * 8) + "owner  :"
                print (SPACE_CHAR * 10) + "'" + ' '.join(line[1].split()[idx_after_other_type:]) + "'"

## Main function

# Check Zone file path
check_args(sys.argv)
# Get all the records
zone_records_list_no_num = [line for record in DNS_RECORD_TYPE for line in open(sys.argv[1]).readlines() if record in line and not line.startswith(";")]
zone_records_list = [pair for pair in enumerate(zone_records_list_no_num)]

# Get Domain Name
domain_name = sys.argv[2]

# Get only A Entries
zone_records_A_entries_list  = [line for line in zone_records_list if 'A' in line[1].split() or 'AAAA' in line[1].split()]

# Get only MX Entries
zone_records_MX_entries_list = [line for line in zone_records_list if 'MX' in line[1].split()]

# Get All others Entries except SOA which is to be created manually
zone_records_OTHERS_entries_list = [item for item in zone_records_list if item not in zone_records_A_entries_list and item not in zone_records_MX_entries_list and 'SOA' not in item[1].split()]

print "########Beginning A Entries##"
check_A_records(zone_records_A_entries_list)
print "########End A Entries##"

print "\n"

print "########Beginning MX Entries##"
check_MX_records(zone_records_MX_entries_list,domain_name)
print "########End MX Entries##"

print "\n"

print "########Beginning Others Entries##"
check_OTHERS_records(zone_records_OTHERS_entries_list,domain_name)
print "########End Others Entries##"
