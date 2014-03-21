A Python module for working with the Zabbix API.

example:
python zabbix_item_add.py -h

Usage: zabbix_item_add.py [options]

Options:
  -h, --help            show this help message and exit
  -s SERVER, --server=SERVER
                        (REQUIRED)Zabbix Server URL.
  -u USERNAME, --username=USERNAME
                        (REQUIRED)Username (Will prompt if not given).
  -p PASSWORD, --password=PASSWORD
                        (REQUIRED)Password (Will prompt if not given).
  -H HOSTNAME, --hostname=HOSTNAME
                        (REQUIRED)hostname for hosts.
  -k KEY, --key=KEY     (REQUIRED)Item key.
  -n NAME, --name=NAME  (REQUIRED)Name of the item.
  -d DELAY, --delay=DELAY
                        (REQUIRED,Default:120)Update interval of the item in
                        seconds.
  -i INTERFACEID, --interfaceid=INTERFACEID
                        (REQUIRED,Default:)ID of the item's host interface.
                        Used only for host items. Optional for Zabbix agent
                        (active), Zabbix internal, Zabbix trapper, Zabbix
                        aggregate, database monitor and calculated items.
  --history=HISTORY     (Default:7)Number of days to keep item's history data.
                        Default:7.
  --units=UNITS         (Default:)Value units.
  -t TYPE, --type=TYPE  (REQUIRED,Default:0)Type of the item. Possible values:
                        0 - Zabbix agent; 1 - SNMPv1 agent; 2 - Zabbix
                        trapper; 3 - simple check; 4 - SNMPv2 agent; 5 -
                        Zabbix internal; 6 - SNMPv3 agent; 7 - Zabbix agent
                        (active); 8 - Zabbix aggregate; 9 - web item; 10 -
                        external check; 11 - database monitor; 12 - IPMI
                        agent; 13 - SSH agent; 14 - TELNET agent; 15 -
                        calculated; 16 - JMX agent.
  --value_type=VALUE_TYPE
                        (REQUIRED,Default:0)Type of information of the item.
                        Possible values: 0 - numeric float; 1 - character; 2 -
                        log; 3 - numeric unsigned; 4 - text.
  --delta=DELTA         Value that will be stored. Possible values: 0 -
                        (default) as is; 1 - Delta, speed per second; 2 -
                        Delta, simple change.
  -f FILE, --file=FILE  Load values from input file. Specify - for standard
                        input Each line of file contains whitespace
                        delimited(if have <params>):
                        <hostname>\t<name>\t<key>\t<params>
  --params=PARAMS       Additional parameters depending on the type of the
                        item:  - executed script for SSH and telnet items;  -
                        additional parameters for database monitor items;  -
                        formula for calculated items.
