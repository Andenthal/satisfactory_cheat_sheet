#!/usr/bin/env python3
from recipes import *


def main():
    """
    Entry point
    :return: None
    """

    # how much do 2 Iron Rod and 2 Iron Plate Constructors consume/product?
    print(f'2 rods + 2 plate = {iron_rod.multiply(2) + iron_plate.multiply(2)}')
    print("---")
    # how much iron does 1 building making Reinforced Iron Plate consume and produce in total?
    print(f'reinforced plate: {reinforced_iron_plate}')
    print("---")
    # I have access to 270 iron ore, how many stators can I make from that?
    # disregard other resource requirements (if applicable)
    print("making stators with only an iron requirement")
    how_many_can_i_make(stator, iron_ore=270)
    print("---")
    # notice how adding in copper as an explicit resource requirement changes the numbers
    print("making stators with both copper and iron requirement")
    how_many_can_i_make(stator, iron_ore=270, copper_ore=270)
    print("---")


if __name__ == '__main__':
    main()
