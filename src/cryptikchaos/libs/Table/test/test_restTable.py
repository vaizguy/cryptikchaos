'''
Created on Aug 27, 2014

This file is part of CryptikChaos.

CryptikChaos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CryptikChaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CryptikChaos. If not, see <http://www.gnu.org/licenses/>.

@author: vaizguy
'''

import cProfile, pstats, StringIO, random, string
import unittest

import pythonpath
pythonpath.AddSysPath('../../../../../.')
pythonpath.AddSysPath('../../../../.')
pythonpath.AddSysPath('../../../.')

from cryptikchaos.libs.Table.restTable import restTable


class TestRestTable(unittest.TestCase):
    
    def setUp(self):
        print "Starting RestTable test: {}".format(self.id())
        
    def tearDown(self):
        print "Finished RestTable test: {}".format(self.id())
    
    def test_speed(self):
        pr = cProfile.Profile()

        rst = restTable(['Title1', 'Title2', 'Title3'])

        pr.enable()

        for _ in xrange(0, 100000):
            col1 = "".join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in xrange(random.randint(1, 20)))
            col2 = "".join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in xrange(random.randint(1, 20)))
            col3 = random.randint(1, 99999)
            rst.add_row([col1, col2, col3])
       
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

