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


class TreePlanterList(object):
    def __init__(self):
        pass
    def add(self, name, treePlanter):
        setattr(self, name, treePlanter)

class ProcessorList(object):
    def __init__(self):
        pass
    def add(self, name, processor):
        setattr(self, name, processor)


class DisplayList(object):
    def __init__(self):
        pass
    def add(self, name, display):
        setattr(self, name, display)

ParserList = ParserList()

ComparatorList = ComparatorList()

TreePlanterList = TreePlanterList()

ProcessorList = ProcessorList()

DisplayList = DisplayList()
