#!/usr/bin/python

"""
Script created by VND - Visual Network Description (SDN version)
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, OVSLegacyKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink

def topology():
    "Create a network."
    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    s1 = net.addSwitch( 's1', listenPort=6634, mac='00:00:00:00:00:01' )
    s2 = net.addSwitch( 's2', listenPort=6635, mac='00:00:00:00:00:02' )
    s3 = net.addSwitch( 's3', listenPort=6636, mac='00:00:00:00:00:03' )
    s4 = net.addSwitch( 's4', listenPort=6637, mac='00:00:00:00:00:04' )
    s5 = net.addSwitch( 's5', listenPort=6638, mac='00:00:00:00:00:05' )
    s6 = net.addSwitch( 's6', listenPort=6639, mac='00:00:00:00:00:06' )
    h7 = net.addHost( 'h7', mac='00:00:00:00:00:07', ip='192.168.1.1/24' )
    h8 = net.addHost( 'h8', mac='00:00:00:00:00:08', ip='192.168.1.2/24' )
    h9 = net.addHost( 'h9', mac='00:00:00:00:00:09', ip='192.168.1.3/24' )
    c23 = net.addController( 'c23', controller=RemoteController, ip='127.0.0.1', port=6633 )

    print "*** Creating links"
    net.addLink(s4, s6, 4, 3)
    net.addLink(s5, s6, 6, 2)
    net.addLink(s3, s5, 3, 5)
    net.addLink(s3, s4, 2, 3)
    net.addLink(s2, s5, 4, 4)
    net.addLink(s2, s4, 3, 2)
    net.addLink(s1, s5, 3, 2)
    net.addLink(s1, s4, 2, 1)
    net.addLink(h9, s3, 0, 1)
    net.addLink(h8, s2, 0, 1)
    net.addLink(h7, s1, 0, 1)

    print "*** Starting network"
    net.start()
    s6.start( [c23] )
    s5.start( [c23] )
    s4.start( [c23] )
    s3.start( [c23] )
    s2.start( [c23] )
    s1.start( [c23] )
    c23.start()

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

