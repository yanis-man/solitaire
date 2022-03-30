class Stack:
    def __init__(self, raw_stack) -> None:
        self.stack = raw_stack

        self.current = self.stack[0]
        self.next = self.stack[1]

    def _check_size(func):
        def wrapper(self):
            if len(self.stack) > 2:
                func(self)
        return wrapper
    
    @_check_size
    def _next(self):
        del self.stack[0]
        self.stack.append(self.current)
        self.current = self.stack[0]
        self.next = self.stack[1]
    
    def _debug(self):
        return f'current : {self.current} ; next : {self.next}'

    # method to pick the current card in the stack
    def _pick(self):
        picked = self.current
        del self.stack[0]
        self.current = self.stack[0]
        self.next = self.stack[1]

        return picked

    def __str__(self) -> str:
        return self.current.__str__()