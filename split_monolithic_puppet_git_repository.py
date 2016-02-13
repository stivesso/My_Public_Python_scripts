#!/bin/python

"""
Simple way to split a monolithic Puppet Environment Directory to many submodules
Takes two arguments, <target working directory> and <Puppet Environment Directory to split>
Usage: sys.argv[0]) + <target working directory> <Puppet Environment Directory to split>
"""

import subprocess
import sys
import os


def run_command(command):
    cmd = command.split()
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


def usage():
    if len(sys.argv) < 2:
        exit_msg = "Usage:" + str(sys.argv[0]) + " <target working directory> <Puppet Environment Directory to split>\
        \nexample: " + str(sys.argv[0]) + " /tmp/modules /etc/puppetlabs/code/environments/test"
        sys.exit(exit_msg)
    if not os.path.exists(sys.argv[2] + "/modules"):
        exit_msg = str(sys.argv[2]) + " must contain the modules subdirectory\
        \nexample: " + str(sys.argv[0]) + " /tmp/modules /etc/puppetlabs/code/environments/test"
        sys.exit(exit_msg)

# Check that there is the needed number of arguments
usage()

target_directory = sys.argv[1]
puppet_environment_directory = sys.argv[2]
puppet_module_path = puppet_environment_directory + "/modules"

# Check whether or not the target directory exists and create it otherwise
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

# let us split the environment directory subfolders (modules) in distinct git repository  
modules_list = [ module_name for module_name in os.listdir(puppet_module_path) if os.path.isdir(os.path.join(puppet_module_path, module_name)) ]
cmd_remove_git_origin = "git remote remove origin"
for module in modules_list:
    print "### Start Split for", module
    os.chdir(target_directory)
    git_clone_cmd = "git clone " + puppet_environment_directory + " " + str(module)
    print "running", git_clone_cmd, "...\n", "".join([str(x) for x in list(run_command(git_clone_cmd))])
    os.chdir(module)
    print "running", cmd_remove_git_origin, "...\n", "".join([str(x) for x in list(run_command(cmd_remove_git_origin))])
    cmd_filter_git = "git filter-branch --subdirectory-filter modules/" + module
    print "running", cmd_filter_git, "...\n", "".join([str(x) for x in list(run_command(cmd_filter_git))]) 
    print "### End Split for", module ,"\n\n"
