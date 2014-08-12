#!/usr/bin/python
"""
#Script created by VND - Visual Network Description (SDN version) 
"""
from pox.core import core
from pox.lib.addresses import IPAddr
from pox.lib.addresses import EthAddr
import pox.openflow.libopenflow_01 as of
from flow import Flow
from node import Node
import random

log = core.getLogger()

switch1 = 0000000000000001
switch2 = 0000000000000002
switch3 = 0000000000000003
switch4 = 0000000000000004
switch5 = 0000000000000005
switch6 = 0000000000000006

links_off = []

active_nodes = []

#c1 - h7 -> h8 (por s4)

c1 = [switch1, switch4, switch2]
c1_inter = [1, 2, 1, 2, 3, 1]
c1_prior = 3
flow1 = Flow(c1, c1_inter, c1_prior)

#c2 - h7 -> h8 (por s5)

c2 = [switch1, switch5, switch2]
c2_inter = [1, 3, 2, 4, 4, 1]
c2_prior = 2
flow2 = Flow(c2, c2_inter, c2_prior)

#c3 - h7 -> h8 (por s6)

c3 = [switch1, switch5, switch6, switch4, switch2]
c3_inter = [1, 3, 2, 6, 2, 3, 4, 2, 3, 1]
c3_prior = 1
flow3 = Flow(c3, c3_inter, c3_prior)

flow_list = [flow1, flow2, flow3]	#Creo el flow1

#c4 - h7 -> h9 (por s4)

c4 = [switch1, switch4, switch3]
c4_inter = [1, 2, 1, 3, 2, 1]
c4_prior = 3
flow4 = Flow(c4, c4_inter, c4_prior)

#c5 - h7 -> h9 (por s5)

c5 = [switch1, switch5, switch3]
c5_inter = [1, 3, 2, 5, 3, 1]
c5_prior = 2
flow5 = Flow(c5, c5_inter, c5_prior)

#c6 - h7 -> h9 (por s6)

c6 = [switch1, switch5, switch6, switch4, switch3]
c6_inter = [1, 3, 2, 6, 2, 3, 4, 3, 2, 1]
c6_prior = 1
flow6 = Flow(c6, c6_inter, c6_prior)

flow_list2 = [flow4, flow5, flow6]	#Creo el flow2

#c7 - h8 -> h9 (por s4)

c7 = [switch2, switch5, switch3]
c7_inter = [1, 4, 4, 5, 3, 1]
c7_prior = 3
flow7 = Flow(c7, c7_inter, c7_prior)

#c8 - h8 -> h9 (por s5)

c8 = [switch2, switch4, switch3]
c8_inter = [1, 3, 2, 3, 2, 1]
c8_prior = 2
flow8 = Flow(c8, c8_inter, c8_prior)

#c9 - h8 -> h9 (por s6)

c9 = [switch2, switch5, switch6, switch4, switch3]
c9_inter = [1, 4, 4, 6, 2, 3, 4, 3, 2, 1]
c9_prior = 1
flow9 = Flow(c9, c9_inter, c9_prior)

flow_list3 = [flow7, flow8, flow9]	#Creo el flow3

def add_to_list (add_node):
   aux = 0
   for i in range(len(active_nodes)):
	if (active_nodes[i].node == add_node.node) and (active_nodes[i].entrance == add_node.entrance) and (active_nodes[i].exit != add_node.exit):
	   active_nodes[i].exit.extend(add_node.exit)
	   aux = 1
   if aux == 0:
	active_nodes.append(add_node)

def preinstall_flow (flow, flow_inter):
   for i in range(len(flow)):
      #---------------IDA------------------------
      switch = flow[i]
      entrance = flow_inter[i*2]
      exit =  flow_inter[i*2+1]
      node = Node(switch, entrance, [exit])
      add_to_list (node)
      #---------------VUELTA------------------------
      switch = flow[i]
      entrance = flow_inter[i*2+1]
      exit =  flow_inter[i*2]
      node = Node(switch, entrance, [exit])
      add_to_list (node)

def install_flow ():
   for i in range(len(active_nodes)):
      print "Nodo: %s" % active_nodes[i].node
      print "Entrada: %s" % active_nodes[i].entrance
      #log.info(active_nodes[i].node)
      flowmsg = of.ofp_flow_mod() 
      flowmsg.cookie = 0
      flowmsg.priority = 1
      flowmsg.match.in_port = active_nodes[i].entrance
      # ACTIONS---------------------------------
      flowout = []
      for x in range(len(active_nodes[i].exit)):
            flowout.append(of.ofp_action_output (port = active_nodes[i].exit[x]))
            print "Salida: %s" % active_nodes[i].exit[x]
      flowmsg.actions = flowout
      core.openflow.sendToDPID(active_nodes[i].node, flowmsg)

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
   active_nodes = []
   msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
 
   # iterate over all connected switches and delete all their flows
   for connection in core.openflow.connections: # _connections.values() before betta
     connection.send(msg)

def install_flows(): 
   log.info("    *** Installing static flows... ***")
   # Push flows to switches
   best_flow = select_best_flow(flow_list)
   preinstall_flow(best_flow.flow, best_flow.interconexion)
   best_flow2 = select_best_flow(flow_list2)
   preinstall_flow(best_flow2.flow, best_flow2.interconexion)
   best_flow3 = select_best_flow(flow_list3)
   preinstall_flow(best_flow3.flow, best_flow3.interconexion)
   install_flow()
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
    clear_flows()
    if event.ofp.desc.config == 0:
        print "Port %s on Switch %s up" % (event.port, event.dpid)
	if [event.dpid, event.port] in links_off:
	    links_off.remove([event.dpid, event.port])
    elif event.ofp.desc.config == 1:
        print "Port %s on Switch %s down" % (event.port, event.dpid)
	links_off.append([event.dpid, event.port])
    best_flow = select_best_flow(flow_list)
    preinstall_flow(best_flow.flow, best_flow.interconexion)
    best_flow2 = select_best_flow(flow_list2)
    preinstall_flow(best_flow2.flow, best_flow2.interconexion)
    best_flow3 = select_best_flow(flow_list3)
    preinstall_flow(best_flow3.flow, best_flow3.interconexion)
    install_flow()
    print "%s" % (best_flow.flow)

def launch (): 
   log.info("*** Starting... ***")
   core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
   core.openflow.addListenerByName("PortStatus", _handle_PortStatus)
   log.info("Waiting for %s switches", len(switches))

