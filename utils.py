import enum

class Card_Families(enum.Enum):
    # CARDS FAMILY
    PIQUE = "\u2660"
    COEUR = "\u2665"
    CARREAU = "\u2666"
    TREFLE = "\u2663"

class Card_Types(enum.Enum):
    # CARDS TYPES
    M = "R"
    L = "D"
    K = "V"
    J = "10"
    I = "9"
    H = "8"
    G = "7"
    F = "6"
    E = "5"
    D = "4"
    C = "3"
    B = "2"
    A = "A"

class Column_translation(enum.Enum):
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4
    f = 5