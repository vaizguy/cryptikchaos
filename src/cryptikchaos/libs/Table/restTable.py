'''
Created on Aug 16, 2014

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

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

import re


class restTable:

    def __init__(self, col_names):

        self.num_of_cols = len(col_names)
        self.table = ''
        self.list_of_rows = []
        self.cols_minlen_dict = {}
        self.header_col_dict = {}
        self.col_delim = "  "
        self.table = ""
        self.table_header = ""
        self.table_boundary = ""
        
        self.add_row(col_names)

    def add_row(self, row):
        
        if type(row) == tuple:
            row = list(row)

        self.list_of_rows.append([re.escape(str(c)) for c in row])
        
    def ext_minlength(self):
        
        self.cols_minlen_dict={}
        for row in self.list_of_rows:

            cnt = 1
            for i in xrange(0, len(row)):
                # measure the size of the col
                col_len = len(row[i])
                try:
                    if col_len > self.cols_minlen_dict[cnt]:
                        self.cols_minlen_dict[cnt] = col_len
                        self.header_col_dict[cnt] = "=" * col_len
                except KeyError:
                    self.cols_minlen_dict[cnt] = col_len
                    self.header_col_dict[cnt] = "=" * col_len
                    
                cnt += 1
               
    def set_table_header(self):
        
        # Get the minimum space for col
        self.ext_minlength()
        
        # Build table
        self.table_header = ""
        self.table_boundary = ""
        # Get header
        for cnt in xrange(1, self.num_of_cols+1):
            if cnt == self.num_of_cols:
                self.table_boundary += self.header_col_dict[cnt]
            else:
                self.table_boundary += "".join((self.header_col_dict[cnt], self.col_delim))

        self.table_header += self.table_boundary
            
    def set_table(self, ):
        
        # Set table header
        self.set_table_header()
        
        # Table content
        self.table = ""
        table_content = ''.join(('\n', self.table_header, '\n'))
        for row in self.list_of_rows:
            col_cnt = 1

            for col in row:
                max_col_len = self.cols_minlen_dict[col_cnt]
                col_len = len(col)
                if col_cnt == self.num_of_cols:
                    table_content += col 
                else:
                    table_content += ''.join((col, " "*(max_col_len-col_len), self.col_delim))
                col_cnt += 1
                
            if row == self.list_of_rows[0]:
                table_content += ''.join(('\n', self.table_boundary, '\n'))  
            else: 
                table_content += '\n'
        
        #print repr(table_content)
        self.table = "".join((table_content, self.table_boundary))
        
    def build(self):
        
        # Set table
        self.set_table()

    def __repr__(self):

        self.build()
        return self.table

if __name__ == '__main__':
    
    from test.test_restTable import TestRestTable, run_test_case
    run_test_case()
    
    


