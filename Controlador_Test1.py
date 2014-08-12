#!/usr/bin/python
"""
#Script created by VND - Visual Network Description (SDN version) 
"""
from pox.core import core
from pox.lib.addresses import IPAddr
from pox.lib.addresses import EthAddr
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

#flow0: 
switch0 = 0000000000000004
flow0msg = of.ofp_flow_mod() 
flow0msg.cookie = 0 
flow0msg.priority = 1000
flow0msg.match.in_port = 2
# ACTIONS---------------------------------
flow0out = of.ofp_action_output (port = 1)
flow0msg.actions = [flow0out] 

#flow1: 
switch1 = 0000000000000004
flow1msg = of.ofp_flow_mod() 
flow1msg.cookie = 0 
flow1msg.priority = 1000
flow1msg.match.in_port = 1
# ACTIONS---------------------------------
flow1out = of.ofp_action_output (port = 2)
flow1msg.actions = [flow1out] 

#flow2: 
switch2 = 0000000000000003
flow2msg = of.ofp_flow_mod() 
flow2msg.cookie = 0 
flow2msg.priority = 1000
flow2msg.match.in_port = 1
# ACTIONS---------------------------------
flow2out = of.ofp_action_output (port = 2)
flow2msg.actions = [flow2out] 

#flow3: 
switch3 = 0000000000000003
flow3msg = of.ofp_flow_mod() 
flow3msg.cookie = 0 
flow3msg.priority = 1000
flow3msg.match.in_port = 2
# ACTIONS---------------------------------
flow3out = of.ofp_action_output (port = 1)
flow3msg.actions = [flow3out] 

def install_flows(): 
   log.info("    *** Installing static flows... ***")
   # Push flows to switches
   core.openflow.sendToDPID(switch0, flow0msg)
   core.openflow.sendToDPID(switch1, flow1msg)
   core.openflow.sendToDPID(switch2, flow2msg)
   core.openflow.sendToDPID(switch3, flow3msg)
   log.info("    *** Static flows installed. ***")

switches = set(v for k,v in vars().items() if k.startswith("switch"))

def _handle_ConnectionUp (event):
   connected = set(c.dpid for c in core.openflow.connections if c.connect_time)
   if switches.intersection(connected) == switches:
      install_flows()

def launch (): 
   log.info("*** Starting... ***")
   core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
   log.info("Waiting for %s switches", len(switches))

