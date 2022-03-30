import random

from utils import Card_Families, Card_Types, Column_translation
from .Card import Card
from .Stack import Stack
from .Actions import Actions

class Plate:

    def __init__(self) -> None:
        self.STACK_COUNT = 6
        self.stack = []
        self.cols = [[] for i in range(self.STACK_COUNT)]

        self.final_stack = [[] for i in range(4)]

        self.actions = Actions()

        # generates the full cards list
        for family in Card_Families:
            for type in Card_Types:
                card = Card(family, type)
                self.stack.append(card)

        random.shuffle(self.stack)
        # associate cards to respective column
        for col, col_pos in zip(self.cols, [i for i in range(self.STACK_COUNT)]):
            for i in range(col_pos+1):
                self.stack[0].flip()
                col.append(self.stack[0])
                del self.stack[0]
            #flip the last card of the column
            self.cols[col_pos][-1].flip()
            self.cols[col_pos] = col
        self.stack = Stack(self.stack)
    
    def __append_to(self, col_id, cards_list):
        for card in cards_list:
            self.cols[col_id].append(card)

    def _compute_neighbor(self):


        for col in self.cols:
            if len(col) > 1:
                COLUMN_LENGTH = len(col)
                for card, i in zip(col, [x for x in range(COLUMN_LENGTH)]):
                    # case of a card between two others
                    if i - 1 >= 0 and i + 1 < COLUMN_LENGTH:
                        if isinstance(card, Card):
                            card.previous = col[i-1]
                            card.next = col[i+1]
                    # case of a card at the beginning of a col
                    elif i == 0:
                        card.next = col[i+1]
                    # case of a card at the end
                    elif i - 1 >= 0:
                        if isinstance(card, Card):
                            card.previous = col[i-1]

    def _move(self, src, dst):

        src_column = int(src[1])

        translated_column = Column_translation[src[0].lower()].value
        to_move = self.cols[src_column][translated_column:]
        remaining_list = self.cols[src_column][:translated_column]

        # checks if the destination column is empty -> no need to test compatibility
        if len(self.cols[dst]) < 1:
            self.cols[src_column]
            self.__append_to(dst, to_move)
            self.cols[src_column] = remaining_list
            if len(self.cols[src_column]) > 1:
                self.cols[src_column][-1].flip()
        else:
            previous_card = to_move[0]
            # iterates throught the flying list of moving card to test inner compatibilty
            for card in to_move[1:]:
                if card.is_hidden():
                    print("Mouvement impossible: carte cachée")
                    return 
                else:
                    if self.__check_card_compatibility(previous_card, card):
                        previous_card = card
                        continue
                    else:
                        # if any card don't respect the order : break the loop
                        print("Mouvement impossible: carte incompatible")
                        return 

            # checks if the destination can handle the cards
            if self.__check_card_compatibility(self.cols[dst][-1], to_move[0]) and not self.cols[dst][-1].is_hidden():
                # put the flying card to the destination column
                self.__append_to(dst, to_move)
                self.cols[src_column] = remaining_list
                # flips the last src column card if hidden
                if len(self.cols[src_column]) >= 1 and self.cols[src_column][-1].is_hidden():
                    self.cols[src_column][-1].flip()
                else:
                    print("Mouvement impossible: destination cachée")
                    return
            else:
                print("Mouvement impossibe: destination non compatible")
                return
            
            return True


    def __check_order(self, under, over):
        # convert intial enum to list to check the correct order
        types_list = [card_type[1] for card_type in enumerate(Card_Types)]

        under_type_index = types_list.index(under.type)

        if under_type_index < len(types_list):
            if (under_type_index > types_list.index(over.type)):
                return True
            else:
                return False
     # checks if the previous card family is correct 
    def __check_card_compatibility(self, under, over):
            if self.__check_order(under, over) == False:
                return False
            else:
                # allows red on black
                if ( under.family == Card_Families.PIQUE or under.family == Card_Families.TREFLE and 
                    over.family == Card_Families.COEUR or over.family == Card_Families.CARREAU):
                    return True
                # allows black on red 
                elif ( under.family == Card_Families.CARREAU or under.family == Card_Families.COEUR and 
                    over.family == Card_Families.PIQUE or over.family == Card_Families.TREFLE):
                    return True   
                else:
                    return False
                
    def __stack(self, src):

        listed_families = [family[1] for family in enumerate(Card_Families)]
        src_column = int(src)
        selected_card = self.cols[src_column][-1]
        # compute the correct stack id based on families order
        card_family_stack_idx = listed_families.index(selected_card.family)
        # checks if the card is at the end of the column and not hidden
        if selected_card.is_hidden() or selected_card != self.cols[src_column][-1]:
            print("Impossible de déplacer: carte cachée")
            return False
        # if the stack is empty and the card is an Ace
        elif len(self.final_stack[card_family_stack_idx]) < 1:
            if selected_card.type == Card_Types.A:
                self.final_stack[card_family_stack_idx].append(selected_card)
                del self.cols[src_column][-1]
        # check the compatibilty of the sleected card and the last stack card
        elif self.__check_order(self.final_stack[card_family_stack_idx][-1], selected_card) == True:
            self.final_stack[card_family_stack_idx].append(selected_card)
            del self.cols[src_column][-1]
        else:
            print("Impossible de déplcar")
            return         
        # flips the last row card (if len > 1 obivously)
        if len(self.cols[src_column]) > 1 and self.cols[src_column][-1].is_hidden():
            self.cols[src_column][-1].flip()

    def __pick(self, dst): 
        dst = int(dst)

        picked = self.stack._pick()
        # no need to chekc compatibilty if the row is empty
        if len(self.cols[dst]) < 1:
            self.cols[dst].append(picked)
        under_card = self.cols[dst][-1]
        
        if self.__check_card_compatibility(under_card, picked) == True:
            self.cols[dst].append(picked)
        else:
            print("Placement incompatible")
            return 

    def display(self):
        # displays cards
        for col, line in zip(self.cols, [x for x in range(len(self.cols))]):
            print(f"n°{line}", end=" ")
            [print(card, end=" ") for card in col]
            print("\n")
        
        #display stack
        self._compute_neighbor()
        print(f"PIOCHE {self.stack}")

        #displays final families stacks
        print("PILE :")

        for final, family in zip(self.final_stack, Card_Families):
            if len(final) >= 1:
                print(f"{ final[-1] }", end=" ")
            else:
                print(f" | {family.value} |", end=" ")

        user_action = self.actions.take_actions()

        # actions dispatcher
        # move action
        if user_action[0] == "m":
            self._move(user_action[1]['src'], user_action[1]['dst'])
        # put card in the final families stack
        elif user_action[0] == "r":
            self.__stack(user_action[1])
        # swtich to the next card in stack
        elif user_action[0] == 'd':
            self.stack._next()
        # pick a card in the stack
        elif user_action[0] == "p":
            self.__pick(user_action[1])


    def check_victory(self):
        for final in self.final_stack:
            if len(final) < 13:
                return False
        
        return True
        



        

    

