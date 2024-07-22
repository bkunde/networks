import io
import random
import string
import unittest
import unittest.mock

import rdt
import simulator

class TestRDT(unittest.TestCase):

    def setUp(self):
        self.msgs = random.randrange(50, 100)
        self.expected = []
        for i in range(self.msgs-1):
            self.expected.append(string.ascii_lowercase[i%26])
        self.freq = 1000
        self.lossprob = 0
        self.corruptprob = 0
        self.pause = 0
        self._simulations = 100
        self.min_rcvd = self.msgs*.96
        self.msg = ("After {} simulations, your protocol did not transport " +
                "the messages with a high enough success rate{}.\n\n")
        self.report = "Got (worst case): {}\nExpected        : {}\n\nSimulator parameters:\n\n{}"


    def simulate(self):
        sim = simulator.Simulator(self.msgs, self.freq, self.lossprob,
                self.corruptprob, self.pause)
        rdt_ = rdt.RDT(sim)
        sim.run(rdt_)
        return sim

    def simulations(self):
        results = []
        worst = None
        for i in range(self._simulations):
            sim = self.simulate()
            results.append(len(sim.received))
            if not worst or len(sim.received) < len(worst):
                worst = sim.received
        return sim, sum(results)/len(results), worst

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_reliable_channel(self, stdout):
        sim, avg, worst = self.simulations()
        self.assertGreaterEqual(avg, self.min_rcvd,
                self.msg.format(self._simulations, ", even under perfect conditions") +
                self.report.format(worst, self.expected, sim.get_params()))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_bit_errors(self, stdout):
        self.corruptprob = .2
        sim, avg, worst = self.simulations()
        self.assertGreaterEqual(avg, self.min_rcvd,
                self.msg.format(self._simulations, " when dealing with bit errors") +
                self.report.format(worst, self.expected, sim.get_params()))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_loss(self, stdout):
        self.lossprob = .1
        sim, avg, worst = self.simulations()
        self.assertGreaterEqual(avg, self.min_rcvd,
                self.msg.format(self._simulations, " when dealing with packet loss") +
                self.report.format(worst, self.expected, sim.get_params()))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_both(self, stdout):
        self.lossprob = .1
        self.corruptprob = .2
        sim, avg, worst = self.simulations()
        self.assertGreaterEqual(avg, self.min_rcvd,
                self.msg.format(self._simulations, " when sending over an unreliable channel") +
                self.report.format(worst, self.expected, sim.get_params()))
