import re

class Actions:
    def __init__(self) -> None:
        self.actions = ["Piocher", "Déplacer", "Ranger", "Défiler la pioche"]
    def take_actions(self):
        for id, action in enumerate(self.actions):
            print(f"\n{id} : {action}")
        player_choice = input("Votre choix : " )

        if player_choice == "0":
            print("Où voulez vous placer la carte ? (numéro de la ligne)")
            user_input = input()
            row_num = re.search('[0-5]{1}', user_input)
            if row_num:
                return ["p", row_num.group(0)]
            else:
                self.take_actions()

        # moving code bloc
        elif player_choice == "1":
            print("Entrez l'origine (sous la forme LigneColonne ex: 0a) et la destination (seulement la ligne) ex: 0a c")
            user_input = input()
            __parsed_move = self.__parse_move(user_input)
            if __parsed_move == False:
                self.take_actions()
            else:
                return ["m", __parsed_move]
        # put the card in the correct family stack
        elif player_choice == "2":
            print("Entrez la carte à ranger (numéro de la ligne)")
            user_input = input()
            row_num = re.search('[0-5]{1}', user_input)
            if row_num:
                return ["r", row_num.group(0)]
            else:
                self.take_actions()
        
        elif player_choice == "3":
            return ['d',]
        else:
            self.take_actions()
        
    def __parse_move(self, raw_input):
        dst_src = raw_input.split(" ")

        # checks if the user input isn't in the correct form
        if len(dst_src) != 2:
            return False
        src_parsed = [
            re.search('[a-f]{1}', dst_src[0], flags=re.IGNORECASE).group(0), 
            re.search('[0-5]{1}', dst_src[0], flags=re.IGNORECASE).group(0)
            ]
        dst = re.match('[0-5]{1}',dst_src[1], flags=re.IGNORECASE).group(0)
        if (src_parsed[0] == None or src_parsed[1] == None) or dst == None:
            return False

        return {
            "src": src_parsed,
            "dst": int(dst)
        }

    def _pick(self, dst):
        pass
