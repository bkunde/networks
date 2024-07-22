import io
import random
import unittest
import unittest.mock

import parse

ALL_PROTOS = ['HTTP', 'TCP','QUIC','MDNS','DNS','TLSv1.2','ARP','UDP']

class TestParser(unittest.TestCase):

    def test_read_trace(self):
        for i in range(3):
            # create random file, remember contents
            # import and call read_trace
            # assertEqual output, contents
            pass

    @unittest.mock.patch('parse.read_trace')
    #@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_main(self, test_patch):
        for i in range(3):
            total_packets = random.randrange(500, 1000, 2)
            total_bytes = total_packets * random.randrange(10, 1500)
            num_uniq_addrs = random.randrange(10, total_packets//2)
            num_uniq_protos = random.randrange(2, len(ALL_PROTOS))
            trace, protos, avg = gen_trace_contents(num_uniq_addrs, num_uniq_protos, total_packets, total_bytes)
            protostr = ','.join(protos)
            with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                test_patch.return_value = trace
                parse.main()
                printed = mock_stdout.getvalue().split('\n')
            self.assertEqual(printed[0], f"Number of unique IP addresses: {num_uniq_addrs}")
            self.assertIn("Unique protocols observed:", printed[1])
            printed_protos = printed[1].split(': ')[1]
            printed_protos_split = printed_protos.split(',')
            same_number = len(protos) == len(printed_protos)
            for p in printed_protos_split:
                if p not in protos:
                    self.fail(f"Protocol {p} not in trace.")
            self.assertEqual(sorted(printed_protos_split), sorted(protos), "Your protocols aren't quite right.")
            self.assertEqual(printed[2], f"Number of packets captured: {total_packets}")
            self.assertEqual(printed[3], f"Total bytes captured: {total_bytes}")
            self.assertEqual(printed[4], f"Average number of bytes per packet: {avg}")
            self.assertEqual(printed[5], f"Median bytes per packet: {avg}")

def gen_addrs(count):
    addrs = []
    for i in range(count):
        addrs.append(f"192.168.1.{i+2}")
    return addrs

def gen_protos(count):
    protos = []
    pool = ALL_PROTOS.copy()
    for i in range(count):
        if pool:
            protos.append(pool.pop())
    return protos

def gen_trace_contents(num_uniq_addrs, num_uniq_protos, total_packets, total_bytes):
    '''return list of lines reflecting params'''
    srcs = gen_addrs(num_uniq_addrs)
    random.shuffle(srcs)
    dsts = srcs.copy()
    random.shuffle(dsts)
    protos = gen_protos(num_uniq_protos)
    a = total_bytes//total_packets
    lines = ['"No.","Time","Source","Destination","Protocol","Length","Info"']
    for i in range(total_packets):
        src = srcs[i%num_uniq_addrs]
        dst = dsts[i%num_uniq_addrs]
        proto = random.choice(protos)
        lines.append(f'"{i+1}","{i+1}","{src}","{dst}","{proto}","{a}","info"')
    return lines, protos, a
