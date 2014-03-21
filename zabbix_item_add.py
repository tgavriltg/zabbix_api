#!/usr/bin/env python
#coding:utf8

'''
Created on 19.03.2014

@author: zhhmj
'''

import optparse
import sys
import traceback
from getpass import getpass
from zabbix_api import ZabbixAPI

def get_options():
    usage = "usage: %prog [options]"
    OptionParser = optparse.OptionParser
    parser = OptionParser(usage)

    parser.add_option("-s","--server",action="store",type="string",\
        dest="server",help="(REQUIRED)Zabbix Server URL.")
    parser.add_option("-u", "--username", action="store", type="string",\
        dest="username",help="(REQUIRED)Username (Will prompt if not given).")
    parser.add_option("-p", "--password", action="store", type="string",\
        dest="password",help="(REQUIRED)Password (Will prompt if not given).")
    parser.add_option("-H","--hostname",action="store",type="string",\
        dest="hostname",help="(REQUIRED)hostname for hosts.")
    parser.add_option("-k","--key",action="store",type="string",\
        dest="key",help="(REQUIRED)Item key.")
    parser.add_option("-n","--name",action="store",type="string",\
        dest="name",help="(REQUIRED)Name of the item.")
    parser.add_option("-d","--delay",action="store",type="int",\
        dest="delay",default="120",help="(REQUIRED,Default:120)Update interval of the item in seconds.")
    parser.add_option("-i","--interfaceid",action="store",type="string",\
        dest="interfaceid",default="",help="(REQUIRED,Default:"")ID of the item's host interface. Used only for host items. Optional for Zabbix agent (active), Zabbix internal, Zabbix trapper, Zabbix aggregate, database monitor and calculated items.")
    parser.add_option("--history",action="store",type="int",\
        dest="history",default="7",help="(Default:7)Number of days to keep item's history data. Default:7.")
    parser.add_option("--units",action="store",type="string",\
        dest="units",default="",help="(Default:"")Value units.")
    parser.add_option("-t","--type",action="store",type="int",\
        dest="type",default="2",help="""(REQUIRED,Default:0)Type of the item.
Possible values:
0 - Zabbix agent;
1 - SNMPv1 agent;
2 - Zabbix trapper;
3 - simple check;
4 - SNMPv2 agent;
5 - Zabbix internal;
6 - SNMPv3 agent;
7 - Zabbix agent (active);
8 - Zabbix aggregate;
9 - web item;
10 - external check;
11 - database monitor;
12 - IPMI agent;
13 - SSH agent;
14 - TELNET agent;
15 - calculated;
16 - JMX agent.""")
    parser.add_option("--value_type",action="store",type="int",\
        dest="value_type",default="0",help="""(REQUIRED,Default:0)Type of information of the item.
Possible values:
0 - numeric float;
1 - character;
2 - log;
3 - numeric unsigned;
4 - text.""")
    parser.add_option("--delta",action="store",type="int",\
        dest="delta",default="0",help="""Value that will be stored.
Possible values:
0 - (default) as is;
1 - Delta, speed per second;
2 - Delta, simple change.""")
    parser.add_option("-f","--file",dest="filename",\
        metavar="FILE",help="Load values from input file. Specify - for standard input Each line of file contains whitespace delimited(if have <params>): <hostname>\\t<name>\\t<key>\\t<params>")
    parser.add_option("--params",action="store",type="string",\
        dest="params",default="",help="""Additional parameters depending on the type of the item: 
- executed script for SSH and telnet items; 
- additional parameters for database monitor items; 
- formula for calculated items.""")

    options,args = parser.parse_args()

    if not options.server:
        options.server = raw_input('server http:')

    if not options.username:
        options.username = raw_input('Username:')

    if not options.password:
        options.password = getpass()

    if ( options.key or options.name ) and options.filename:
	print("name,key and filename is not exist at the same time.")
	sys.exit(-1)

    if ( options.key or options.name ) and not options.hostname:
        options.hostname = raw_input('hostname:')

    return options, args

def errmsg(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(-1)

if __name__ == "__main__":
    options, args = get_options()

    zapi = ZabbixAPI(server=options.server, path="", log_level=0)
    zapi.login(options.username, options.password)

    hostname = options.hostname
    key = options.key
    name = options.name
    type = options.type
    value_type = options.value_type
    delay = options.delay
    interfaceid = options.interfaceid
    history = options.history
    units = options.units
    delta = options.delta
    params = options.params
    file = options.filename


    if file:
        with open(file,"r") as f:
            content = f.readlines()
            for i in content:
                l = i.split("\t")
		hostname = l[0].rstrip()
	        name = l[1].rstrip()
                key = l[2].rstrip()
                params = l[3].rstrip()
		print hostname,'\t',name,'\t',key,'\t',params
                hostid=zapi.host.get({"filter":{"host":hostname}})[0]["hostid"]
                print hostid
                zapi.item.create({"name":name,"key_":key,"hostid":hostid,"type":(type),"interfaceid":interfaceid,"value_type":value_type,"delay":delay,"history":history,"delta":delta,"units":units,"params":params})
    else:
        hostid=zapi.host.get({"filter":{"host":hostname}})[0]["hostid"]
        print hostid
        zapi.item.create({"name":name,"key_":key,"hostid":hostid,"type":(type),"interfaceid":interfaceid,"value_type":value_type,"delay":delay,"history":history,"delta":delta,"units":units,"params":params})
