import logging # you may want to log stuff as you go
from simulator import A, B # use these to identify between hosts A and B

class Pkt:

    def __init__(self):
        # do not change these attrs or the simulator will break
        self.seqnum = None
        self.checksum = None
        self.payload = ""

    def make_checksum(self, data):
        checksum = sum(ord(char) for char in data)
        return checksum

    def verify_checksum(self, pkt):
        return (pkt.checksum == self.make_checksum(pkt.payload))

    def __str__(self):
        return self.payload

class RDT:
    def __init__(self, sim):
        self.sim = sim
        self.seqnum = 0
        self.expected_seqnum = 0
        self.last_pkt = None
        self.transmitting = False

    def rdt_sendA(self, msg):
        """called from layer 5 at A, it should transport the msg to B."""
        if not self.transmitting:
            packet = self.make_packet(msg)
            packet.seqnum = self.seqnum
            self.sim.tolayer3(A, packet)
            self.last_pkt = packet
            self.sim.start_timer(A, 5)
            self.transmitting = True


    def rdt_rcvA(self, pkt):
        """called from layer 3 when a packet arrives for layer 4 at A."""
        if pkt.verify_checksum(pkt):
            self.sim.tolayer5(A, pkt.payload)
            ack_pkt = self.make_ack(pkt.seqnum)
            self.sim.tolayer3(A, ack_pkt)
            self.sim.stop_timer(A)
            self.transmitting = False

    def timer_interruptA(self):
        """called when A's timer goes off."""
        if self.transmitting:
            self.sim.tolayer3(A, self.last_pkt)
            self.sim.start_timer(A, 5)
            self.transmitting = True

    def rdt_rcvB(self, pkt):
        """called from layer 3 when a packet arrives for layer 4 at B."""
        if pkt.verify_checksum(pkt):
            self.sim.tolayer5(B, pkt.payload)
            ack_pkt = self.make_ack(pkt.seqnum)
            self.sim.tolayer3(B, ack_pkt)
            self.sim.stop_timer(B)
            self.transmitting = False

    def make_packet(self, msg):
        pkt = Pkt()
        pkt.seqnum = 0
        pkt.checksum = pkt.make_checksum(msg)
        pkt.payload = msg
        return pkt

    def make_ack(self, acknum):
        ack = Pkt()
        ack.seqnum = acknum
        ack.checksum = ack.make_checksum(str(acknum))
        ack.payload = ''
        return ack
