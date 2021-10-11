"""
Another bicycle for generating tables.

Another one, but my own.
"""


class Cell:
    def __init__(self, data: str):
        strip = lambda val: val.replace('\t', ' ').rstrip().lstrip()
        content = str(data).splitlines()
        content = content or ['']
        content = list(map(strip, content))

        self.content = content
        self.height = len(content)
        self.width = max(len(s) for s in content)

    def as_size(self, width: int, height: int) -> list[str]:
        def sequence_to_size(sequence, size, null):
            length = len(sequence)
            last = (size - length) // 2
            first = last + (size - length) % 2
            return null * first + sequence + null * last

        content = sequence_to_size(self.content, height, [''])
        content = [sequence_to_size(line, width, ' ') for line in content]
        return content


class TableGenerator:
    def __init__(
            self,
            body: list[list],
            header: list = None,
            params: list = None,
    ):
        self.table = self.generate_table(body, header, params)

        self.widths: list[int]
        self.heights: list[int]
        self.row_separator: str
        self.cell_separator: list[str]
        self.calculate_sizes()

    @staticmethod
    def generate_table(body, header, params) -> list[list]:
        table = body  # size M x N -> [ [ val x N ] x M ]

        if params:
            table = [[par] + row for (par, row) in zip(params, table)]

        if header:
            if table and len(header) == len(table[-1]) - 1:
                header = [''] + header
            table = [header] + table

        m = len(table)
        if m == 0:
            raise ValueError('No data - table is empty!')
        n = len(table[0])
        is_same_length = all(len(row) == n for row in table)
        if not is_same_length:
            raise ValueError('Rows of the table have different lengths!')

        table = [
            [Cell(cell) for cell in row]
            for row in table
        ]

        return table

    def calculate_sizes(self) -> None:
        self.widths = [
            max(cell.width for cell in column) + 2  # 2 - for margins
            for column in zip(*self.table)
        ]
        self.heights = [
            max(cell.height for cell in row)
            for row in self.table
        ]
        cell_separators = ['-' * width for width in self.widths]
        self.row_separator = '+'.join([''] + cell_separators + [''])
        self.cell_separator = ['|'] * (len(self.widths) + 1)

    def generate(
            self,
            mark_header: bool = True,
            mark_params: bool = False
    ) -> str:
        assert self.table, 'No data - table is empty!'

        def generate_row_strings(row: list[Cell], height) -> list[str]:
            list_cells = [
                cell.as_size(width, height)
                for (cell, width) in zip(row, self.widths)
            ]

            join_string = lambda one_line_strings: cell_separator[0] + ''.join(
                string + sep
                for (string, sep) in zip(one_line_strings, cell_separator[1:])
            )
            list_strings = [
                join_string(one_line_strings)
                for one_line_strings in zip(*list_cells)
            ]

            return list_strings

        # create data for generate
        table = self.table
        cell_separator = self.cell_separator.copy()
        row_separator = self.row_separator
        header_row_separator = row_separator
        if mark_params:
            cell_separator[0], cell_separator[1] = '||', '||'
            second_plus_index = row_separator[1:].index('+') + 1
            row_separator = (
                '+'
                + row_separator[:second_plus_index]
                + '+'
                + row_separator[second_plus_index:]
            )
            header_row_separator = row_separator
        if mark_header:
            header_row_separator = header_row_separator.replace('-', '=')

        # add header row
        table_strings: list[str] = (
            [header_row_separator]
            + generate_row_strings(table[0], self.heights[0])
            + [header_row_separator]
        )

        # generate  rest of table
        for (row, height) in zip(table[1:], self.heights[1:]):
            table_strings += generate_row_strings(row, height)
            table_strings += [row_separator]

        str_table = '\n'.join(table_strings)
        return str_table


if __name__ == '__main__':
    header = ['Price / discount', 'Description', 'Is good']
    table = [
        [
            'watermelon',
            '$100 \n 5%',
            (
                'This is a very long \n'
                'description, it describes \n'
                'a watermelon'
            ),
            'Yes',
        ],
        [
            'melon',
            '$30 \n 10%',
            'Who even likes melons?', 
            'No',
        ],
        [
            'apricot',
            '$65',
            (
                'Apricots are divided by 2, \n'
                'and then by 2 more, \n'
                'and then by 2 more, \n'
                'and then by 2 more, \n'
                '...'
            ),
            'Yes',
        ],
        [
            'pineapple',
            '$89',
            'Pen-pineapple-apple-pen!',
            'No',
        ],
        [
            'apple',
            '$123',
            'Pen-pineapple-apple-pen! \n (again?)',
            'Yes',
        ],
        [
            'pear',
            '$20 \n 15%',
            "The pear is terrible, \n let's burn them all!",
            'No',
        ],
        [
            'tangerine',
            '$43',
            'We shared a tangerine... \n oh no, it was an orange!',
            'Yes \n (for a bit)',
        ],
        [
            'orange',
            '$54',
            (
                'We shared an orange. \n'
                'There are many of us, but he is alone. \n'
                'This slice is for the hedgehog. \n'
                'This slice is for the swift. \n'
                'This slice is for ducklings. \n'
                'This slice is for kittens. \n'
                'This slice is for beaver. \n'
                'And for the wolf – the peel.'
            ),
            'No',
        ],
        [
            'blueberry',
            '$55',
            'Why BLUEberry is called CHERnika?',
            'Yes',
        ],
    ]

    print(TableGenerator(table, header=header).generate(mark_params=True))
