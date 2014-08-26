'''
Created on Aug 27, 2014

@author: vaizguy
'''

import cProfile, pstats, StringIO, random, string
import unittest

from cryptikchaos.libs.Table.restTable import restTable


class TestRestTable(unittest.TestCase):
    
    def setUp(self):
        print "Starting RestTable test: {}".format(self.id())
        
    def tearDown(self):
        print "Finished RestTable test: {}".format(self.id())
    
    def test_speed(self):
        pr = cProfile.Profile()

        rst = restTable(['Title1', 'Title2', 'Title3'])

        for _ in xrange(0, 100000):
            col1 = "".join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in xrange(random.randint(1, 20)))
            col2 = "".join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in xrange(random.randint(1, 20)))
            col3 = random.randint(1, 99999)
            rst.add_row([col1, col2, col3])
       
        pr.enable()
        repr(rst)
        pr.disable()

        s= StringIO.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print s.getvalue()
        
    def test_restTable(self):
            
        rst = restTable(['1', '2', '3'])
        rst.add_row(('a', 'c', 'e'))
        rst.add_row(('ab', 'cd', 'ef'))
        rst_g = """
==  ==  ==
1   2   3
==  ==  ==
a   c   e
ab  cd  ef
==  ==  =="""
        r = str(rst).encode('string_escape')
        g = str(rst_g).encode('string_escape')
        self.assertEqual(r, g, "\nR:\n{}\nG:\n{}".format(r, g))

def run_test_case():
    unittest.main()
    
if __name__ == '__main__':
    run_test_case()

