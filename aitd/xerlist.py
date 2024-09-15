class ParserList(object):
    def __init__(self):
        pass

    def add(self, name, parser):
        setattr(self, name, parser)


class ComparatorList(object):
    def __init__(self):
        pass

    def add(self, name, comparator):
        setattr(self, name, comparator)


ParserList = ParserList()

ComparatorList = ComparatorList()