

def has_blocking_io(func):
    func._has_blocking_io = True
    return func
