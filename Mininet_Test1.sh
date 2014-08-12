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
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='192.168.1.1/24' )
    h2 = net.addHost( 'h2', mac='00:00:00:00:00:02', ip='192.168.1.2/24' )
    s3 = net.addSwitch( 's3', listenPort=6634, mac='00:00:00:00:00:03' )
    s4 = net.addSwitch( 's4', listenPort=6635, mac='00:00:00:00:00:04' )
    c8 = net.addController( 'c8', controller=RemoteController, ip='127.0.0.1', port=6633 )

    print "*** Creating links"
    net.addLink(h1, s3, 0, 1)
    net.addLink(s3, s4, 2, 1)
    net.addLink(s4, h2, 2, 0)

    print "*** Starting network"
    net.start()
    s4.start( [c8] )
    s3.start( [c8] )
    c8.start()

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

