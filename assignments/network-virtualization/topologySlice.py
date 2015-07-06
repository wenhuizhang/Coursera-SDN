'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()


class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")
	
					
	
    def flow_add_forward(self, event, port_tuple):
	match = of.ofp_match()
	match.in_port = port_tuple[0]	
	msg = of.ofp_flow_mod()
	msg.match = match 
	msg.actions.append(of.ofp_action_output(port = port_tuple[1]))
	event.connection.send(msg)    
    
    def flow_add_backward(self, event, port_tuple):
        match = of.ofp_match()
        match.in_port = port_tuple[1]
        msg = of.ofp_flow_mod()
        msg.match = match
        msg.actions.append(of.ofp_action_output(port = port_tuple[0]))
        event.connection.send(msg)		

    def add_flow(self, event, port_tuple):
	self.flow_add_forward(event, port_tuple)
	self.flow_add_backward(event, port_tuple)
	

    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):

        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)

        """ Add your logic here """
	if dpid == "00-00-00-00-00-01":
		self.add_flow(event, (3, 1))
		self.add_flow(event, (4, 2))
		log.debug("Adding flows for %s.", dpid)

	if dpid == "00-00-00-00-00-02":
		self.add_flow(event, (1, 2))
		log.debug("Adding flows for %s.", dpid)
	
	if dpid == "00-00-00-00-00-03":
		self.add_flow(event, (1, 2))
		log.debug("Adding flows for %s.", dpid)
	
	if dpid == "00-00-00-00-00-04":
		self.add_flow(event, (1, 3))
		self.add_flow(event, (2, 4))
		log.debug("Adding flows for %s.", dpid)


def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
