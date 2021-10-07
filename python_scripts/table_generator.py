class TableGenerator:
    class _Cell:
        content = []
        width = 0
        heigth = 0  
        def __init__(self, content):
            content = str(content).split('\n')
            content = [s.replace('\t', ' ') for s in content]
            content = [s.rstrip().lstrip() for s in content]
            self.content = content
            self.heigth = len(content)
            self.width = max(len(s) for s in self.content)

        def to_heigth(self, heigth):
            last = (heigth - self.heigth) // 2
            first = last + (heigth - self.heigth) % 2
            return [''] * first + self.content + [''] * last

        @staticmethod
        def to_width(text, width):
            last = (width - len(text)) // 2
            first = last + (width - len(text)) % 2
            return ' ' * first + text + ' ' * last

    table = []
    widths = []
    spliter = ''
    str_table = ''

    def __init__(
        self,
        body:list = list(),
        header:list = None,
        params:list = None,
    ):
        if header is None:
            header = body[0]
            body = body[1:]

        if params is None:
            params = [string[0] for string in body]
            body = [string[1:] for string in body]

        if len(header) == len(body[-1]):
            header = [''] + header

        table = [header] + [
            [par] + string for (par, string) in zip(params, body)
        ]

        self.table = [
            [self._Cell(content) for content in string]
            for string in table
        ]
        self.widths = [
            max(cell.width for cell in column)
            for column in zip(*self.table)
        ]
        self.spliter = '+' + '+'.join('-' * (w + 2) for w in self.widths) + '+'
        self.spliter += '\n'

    def _generate_string(self, string: list, mark_params:bool = False) -> str:
        heigth = max(cell.heigth for cell in string)
        string = [cell.to_heigth(heigth) for cell in string]
        string = list(zip(*string))

        s = ''
        for one_text_string in string:
            s += '|'
            for index, (text, width) in enumerate(zip(one_text_string, self.widths)):
                s += ' '
                s += self._Cell.to_width(text, width)
                s += ' |' 
                if index == 0 and mark_params:
                    s += '|'
            s += '\n'
        return s

    def generate(self, mark_header:bool = True, mark_params:bool = False) -> str:
        spliter = self.spliter
        if mark_params:
            second_plus_index = spliter[1:].index('+') + 1
            spliter = spliter[:second_plus_index] + '+' + spliter[second_plus_index:]

        self.str_table = spliter
        for (index, string) in enumerate(self.table):
            if index == 0 and mark_header:
                double_spliter = spliter.replace('-', '=')
                self.str_table = double_spliter
                self.str_table += self._generate_string(string, mark_params)
                self.str_table += double_spliter
                continue
            self.str_table += self._generate_string(string, mark_params)
            self.str_table += spliter

        return self.str_table 


if __name__ == '__main__':
    header = ['Name', 'Price (discount)', 'Description', 'Is Good']
    table = [
        [
            'watermelon',
            '$100 \n 5%',
            'This is a very long \n description, it describes \n a watermelon',
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
            'Apricots are divided by 2, \n and then by 2 more, \n and then by 2 more, \n and then by 2 more, \n ...', 
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
