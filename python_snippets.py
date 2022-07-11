"""
Snippets of code that are sometimes needed, but not too big for a
separate file.

TODO: it needs to be documenting
"""


# ======= SINGLETON ====================================================


class SingletonMeta(type):
    instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.instances[cls]


class Singleton(metaclass=SingletonMeta):
    pass


# ======= EXCEPTION FROM DOC ===========================================


class ExceptionFromDoc(Exception):
    """Something went wrong"""

    def __init__(self, msg=None):
        if msg is None:
            msg = self.__doc__
        super(ExceptionFromDoc, self).__init__(msg.lstrip().rstrip())


class ExceptionFromFormattedDoc(ExceptionFromDoc):
    __doc__ = ExceptionFromDoc.__doc__

    def __init__(self, *formats):
        try:
            msg = self.__doc__.format(*formats)
        except IndexError:
            msg = 'The error could not be formatted, but an error of the form'
            msg += '\n' + self.__doc__ + '\n' + str(formats)
        super(ExceptionFromFormattedDoc, self).__init__(msg)


# ======== FOLDER WALK =================================================


import os


def get_all_files_from_folder(path):
    all_files = list()
    for (folder, _, files) in os.walk(path):
        for file in files:
            all_files.append(f'{folder}/{file}')
    return all_files


# ======== =============================================================


def do_input(description='', args=('y', 'n')):
    msg = description + ' (<' + '>/<'.join(args) + '>): '
    answer = None
    while answer not in args:
        if answer is not None:
            print('unexpected input!')
        answer = input(msg)
    return answer


# ======== =============================================================


def child_classes(locals_, parent_class):
    def _is_subclass(cls):
        return (
                isinstance(cls, type)  # is class
                and issubclass(cls, parent_class)  # is subclass
                and cls != parent_class  # not parent class
        )
    return [
        name
        for (name, cls) in locals_.items()
        if _is_subclass(cls)
    ]


# ======== =============================================================
