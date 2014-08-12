#!/usr/bin/python
"""
#Script created by VND - Visual Network Description (SDN version) 
"""
from pox.core import core
from pox.lib.addresses import IPAddr
from pox.lib.addresses import EthAddr
import pox.openflow.libopenflow_01 as of
from flow import Flow

log = core.getLogger()

switch1 = 0000000000000001
switch2 = 0000000000000002
switch3 = 0000000000000003
switch4 = 0000000000000004

links_off = []

#c1 - h7 -> h8 (por s2)

c1 = [switch1, switch2, switch4]
c1_inter = [1, 2, 4, 5, 2, 1]
c1_prior = 1
flow1 = Flow(c1, c1_inter, c1_prior)

#c2 - h7 -> h8 (por s3)

c2 = [switch1, switch3, switch4]
c2_inter = [1, 3, 4, 5, 3, 1]
c2_prior = 2
flow2 = Flow(c2, c2_inter, c2_prior)

flow_list = [flow1, flow2]

def install_flow (flow, flow_inter):
   for i in range(len(flow)):
      flowmsg = of.ofp_flow_mod() 
      flowmsg.cookie = 0 
      flowmsg.priority = 1
      flowmsg.match.in_port = flow_inter[i*2]
      # ACTIONS---------------------------------
      flowout = of.ofp_action_output (port = flow_inter[i*2+1])
      flowmsg.actions = [flowout] 
      core.openflow.sendToDPID(flow[i], flowmsg)
      #--------------------------------------------------------
      flowmsg = of.ofp_flow_mod() 
      flowmsg.cookie = 0 
      flowmsg.priority = 1
      flowmsg.match.in_port = flow_inter[i*2+1]
      # ACTIONS---------------------------------
      flowout = of.ofp_action_output (port = flow_inter[i*2])
      flowmsg.actions = [flowout] 
      core.openflow.sendToDPID(flow[i], flowmsg)

def remove_flow (flow, flow_inter):
   for i in range(len(flow)):
      flowmsg = of.ofp_flow_mod() 
      flowmsg.command = of.OFPFC_DELETE
      flowmsg.out_port = flow_inter[i*2]
      core.openflow.sendToDPID(flow[i], flowmsg)
      #--------------------------------------------------------
      flowmsg = of.ofp_flow_mod() 
      flowmsg.command = of.OFPFC_DELETE
      flowmsg.out_port = flow_inter[i*2+1]
      core.openflow.sendToDPID(flow[i], flowmsg)

def select_best_flow (flow_array):
   valid_flows = flow_array[:]
   for i in range(len(flow_array)):
	for x in range(len(flow_array[i].flow)):
	   if [flow_array[i].flow[x], flow_array[i].interconexion[x*2]] in links_off:
		valid_flows.remove(flow_array[i])
		break
	   if [flow_array[i].flow[x], flow_array[i].interconexion[x*2+1]] in links_off:
		valid_flows.remove(flow_array[i])
		break
   best_flow = []
   for u in range(len(valid_flows)):
	if best_flow == []:
	   best_flow = valid_flows[u]
	elif best_flow.priority < valid_flows[u].priority:
	   best_flow = valid_flows[u]
   return best_flow

def clear_flows():
   msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
 
   # iterate over all connected switches and delete all their flows
   for connection in core.openflow.connections: # _connections.values() before betta
     connection.send(msg)

def install_flows(): 
   log.info("    *** Installing static flows... ***")
   # Push flows to switches
   best_flow = select_best_flow(flow_list)
   install_flow(best_flow.flow, best_flow.interconexion)
   log.info("    *** Static flows installed. ***")

switches = set(v for k,v in vars().items() if k.startswith("switch"))

def _handle_ConnectionUp (event):
   connected = set(c.dpid for c in core.openflow.connections if c.connect_time)
   if switches.intersection(connected) == switches:
      install_flows()

def _handle_PortStatus (event):
    if event.ofp.reason == of.OFPPR_ADD:
        action = "added"
    elif event.ofp.reason == of.OFPPR_DELETE:
        action = "removed"
    elif event.ofp.reason == of.OFPPR_MODIFY:
        action = "modified"
    print "Port %s on Switch %s has been %s." % (event.port, event.dpid, action)
    if event.ofp.desc.config == 0:
        print "Port %s on Switch %s up" % (event.port, event.dpid)
	clear_flows()
	if [event.dpid, event.port] in links_off:
	    links_off.remove([event.dpid, event.port])
	best_flow = select_best_flow(flow_list)
	install_flow(best_flow.flow, best_flow.interconexion)
	print "%s" % (best_flow.flow)
    elif event.ofp.desc.config == 1:
        print "Port %s on Switch %s down" % (event.port, event.dpid)
	clear_flows()
	links_off.append([event.dpid, event.port])
	best_flow = select_best_flow(flow_list)
	install_flow(best_flow.flow, best_flow.interconexion)
	print "%s" % (best_flow.flow)

def launch (): 
   log.info("*** Starting... ***")
   core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
   core.openflow.addListenerByName("PortStatus", _handle_PortStatus)
   log.info("Waiting for %s switches", len(switches))

