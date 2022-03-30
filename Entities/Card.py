class Card:
    def __init__(self, family, type) -> None:
        self.family = family
        self.type = type
        self.isHidden = False

        # describes the card on top and under the current
        self.previous = None
        self.next = None
    def __str__(self) -> str:
        if self.isHidden:
            return "| X |"
        return f"| {self.type.value} {self.family.value} |"
    
    def _debug(self):
        return f'previous {self.previous} ; current {self.__str__()} ; next {self.next}'

    def flip(self):
        self.isHidden = not self.isHidden
    
    def is_hidden(self):
        return self.isHidden