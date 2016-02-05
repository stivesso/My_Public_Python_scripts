#!/bin/python
"""
My quick and dirty way to login to Iscsi Storage, discover LUNs and login to that target storage
by Steve ESSO
"""
import subprocess
import sys

def run_command(command):
    cmd = command.split()
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def usage():
    if len(sys.argv) < 2:
        exit_msg = "Usage:" + str(sys.argv[0]) + "<ip address of one Iscsi target>:<port> \nexample: "  + str(sys.argv[0]) + " 192.168.10.17:3260"
        sys.exit(exit_msg)

usage()
command = "iscsiadm --mode discoverydb --type sendtargets --portal " + str(sys.argv[1]) + " --discover"
dict_portal_iqn = {}

for output in run_command(command):
    iscsit_details_list = output.strip("\n").split()
    #print iscsit_details_list
    dict_portal_iqn[iscsit_details_list[0].split(",")[0]] = iscsit_details_list[1]

for target_portal in dict_portal_iqn:
    command_login = "iscsiadm --mode node --targetname " + str(dict_portal_iqn[target_portal]) + " --portal " + str(target_portal) + " --login"
    print "running: ", command_login
    print [login_output for login_output in run_command(command_login)]
