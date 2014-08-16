'''
Created on Aug 16, 2014

@author: vaizguy
'''


class rstTable:

    def __init__(self, col_names):

        num_of_cols = len(col_names)
        self.row_1 = col_names
        self.table = ''

        self.list_of_rows = []
        self.list_of_rows.append(self.row_1)

    def add_row(self, row):

        self.list_of_rows.append(row)

    def build(self):

        cols_dict = {}
        cols_minlen_dict = {}

        for row in self.list_of_rows:

            cnt = 1
            for col in row:

                # measure the size of the col
                col_len = len(str(col))
                try:
                    if len(str(col)) > cols_minlen_dict[cnt]:
                        cols_minlen_dict[cnt] = col_len
                except KeyError:
                    cols_minlen_dict[cnt] = col_len

                # Save col value
                try:
                    cols_dict[cnt].append(col)
                except KeyError:
                    cols_dict[cnt] = [col]
                    
                cnt += 1

        #print cols_dict
        print cols_minlen_dict

        # header syntax
        # =============
        header_col_dict = {}

        for (k, v) in cols_minlen_dict.iteritems():
            header_col_dict[k] = "=" * v

        #print header_col_dict

        # Build table
        col_delim = "  "

        # Build header
        table_header = ""

        # first/third line
        tbl_header_buondary = ''
        for cnt in range(1, len(cols_dict)+1):
            
            tbl_header_buondary += header_col_dict[cnt] + col_delim

        # strip line
        tbl_header_buondary = tbl_header_buondary.rstrip()
        #print repr(tbl_header_buondary)

        table_header += tbl_header_buondary

        # Get titles
        titles_row = ''

        cnt = 1
        for col in self.list_of_rows[0]:
            max_col_len = cols_minlen_dict[cnt]
            col_len = len(str(col))
            titles_row += str(col) + " "*(max_col_len-col_len) + col_delim
            cnt += 1

        titles_row = titles_row.rstrip()
        #print repr(titles_row)

        table_header += '\n' + titles_row + '\n' + table_header
        #print repr(table_header)

        # Table content
        table_content = ""
        for row in self.list_of_rows[1:]:
            col_cnt = 1

            for col in row:
                max_col_len = cols_minlen_dict[col_cnt]
                col_len = len(str(col))
                table_content += str(col) + " "*(max_col_len-col_len) + col_delim
                col_cnt += 1

            table_content = table_content.rstrip()
            table_content += '\n'
        
        table_content = table_content.rstrip()
        #print repr(table_content)

        # Get table
        self.table = table_header + '\n' + table_content + '\n' + tbl_header_buondary

    def __repr__(self):

        self.build()
        return self.table


if __name__ == '__main__':

    rst = rstTable(['Title1', 'Title2', 'Title3'])

    rst.add_row(['Val1', 'Key1', 'Col3'])
    rst.add_row(['Val2', 'Key2', 'c3'])
    rst.add_row(['Val3', 'Key3', 'column3'])

    print rst

