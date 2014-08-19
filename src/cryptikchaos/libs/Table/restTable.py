'''
Created on Aug 16, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"


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
        
        row = list(row)

        self.list_of_rows.append(row)
        
    def ext_minlength(self):
        
        self.cols_minlen_dict={}
        for row in self.list_of_rows:

            cnt = 1
            for i in xrange(0, len(row)):
                # convert column val into string
                row[i] = re.escape(str(row[i]))
                # set col
                col = str(row[i])
                # measure the size of the col
                col_len = len(col)
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
                col_len = len(str(col))
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

    import cProfile, pstats, StringIO, random, string
    
    pr = cProfile.Profile()
    rst = restTable(['Title1', 'Title2', 'Title3'])
    
    for i in xrange(0, 100000):
        col1 = "".join(random.choice(string.ascii_uppercase + string.digits)
                for x in xrange(random.randint(1, 20)))
        col2 = "".join(random.choice(string.ascii_uppercase + string.digits)
                for x in xrange(random.randint(1, 20)))
        col3 = random.randint(1, 99999)
        rst.add_row([col1, col2, col3])
    
    pr.enable()
    print rst
    pr.disable()
    
    s= StringIO.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()