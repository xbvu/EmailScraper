

class TupleSortingOn0(tuple):
    # https://stackoverflow.com/questions/21768493
    # decorator for sorting on zero key
    # only 'less than' comparison is used in PriorityQueue
    def __lt__(self, rhs):
        return self[0] < rhs[0]