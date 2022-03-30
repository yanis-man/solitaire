from time import sleep

from Entities.Plate import Plate
p = Plate()
while not p.check_victory():
    p.display()