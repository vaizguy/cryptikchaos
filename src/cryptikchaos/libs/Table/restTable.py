'''
Created on Aug 16, 2014

@author: vaizguy
'''

import re


class restTable:

    def __init__(self, col_names):

        self.num_of_cols = len(col_names)
        self.row_1 = col_names
        self.table = ''

        self.list_of_rows = []
        self.add_row(self.row_1)

    def add_row(self, row):
        
        row = list(row)

        self.list_of_rows.append(row)

    def build(self):

        cols_minlen_dict = {}

        for row in self.list_of_rows:

            cnt = 1
            for i in range(0, len(row)):
                # convert column val into string
                row[i] = re.escape(str(row[i]))
                # set col
                col = row[i]
                # measure the size of the col
                col_len = len(str(col))
                try:
                    if len(str(col)) > cols_minlen_dict[cnt]:
                        cols_minlen_dict[cnt] = col_len
                except KeyError:
                    cols_minlen_dict[cnt] = col_len

                cnt += 1

        #print cols_minlen_dict

        # header syntax
        # =============
        header_col_dict = {}
        # Get header cols boundary
        for (k, v) in cols_minlen_dict.iteritems():
            header_col_dict[k] = "=" * v

        #print header_col_dict

        # Build table
        col_delim = "  "
        self.table = ""
        
        # Build header
        table_header = ""
        table_boundary = ""
        # Get header
        for cnt in range(1, self.num_of_cols+1):
            if cnt == self.num_of_cols:
                table_boundary += header_col_dict[cnt]
            else:
                table_boundary += header_col_dict[cnt] + col_delim

        table_header += table_boundary

        # Table content
        table_content = '\n' + table_header + '\n'
        for row in self.list_of_rows:
            col_cnt = 1

            for col in row:
                max_col_len = cols_minlen_dict[col_cnt]
                col_len = len(str(col))
                if col_cnt == self.num_of_cols:
                    table_content += col 
                else:
                    table_content += col + " "*(max_col_len-col_len) + col_delim
                col_cnt += 1
                
            if row == self.list_of_rows[0]:
                table_content += '\n' + table_boundary + '\n' 
            else: 
                table_content += '\n'
        
        #print repr(table_content)
        self.table = table_content + table_boundary

    def __repr__(self):

        self.build()
        return self.table


if __name__ == '__main__':

    rst = restTable(['Title1', 'Title2', 'Title3'])

    rst.add_row(['Val1', 'Kjjjjjjjjjjjjjey1', 'Col3'])
    rst.add_row(['Val2', 'Key2', 'c3'])
    rst.add_row(['Val3', 'Key3', 'coljjjjjjjjjjjjjjumn3'])
    rst.add_row((5, '6', 'coljjjjjjjjjjjjjjumn3'))

    print rst

