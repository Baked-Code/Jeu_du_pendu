from faker import Faker
from pendu import PenduWidget
import logging

logging.basicConfig(filename='journal.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')



class Mot:
    def __init__(self):
        self.mot = self._get_word(4, 8)
        self.finded_letter = ["_" for i in self.mot]
    
    def __str__(self) -> str:
        return self.mot

    def _get_word(self, min, max):
        fake = Faker("fr_FR")
        mot = fake.word()
        while len(mot) < min or len(mot) > max:
            mot = fake.word()
        return mot.upper()
    
    def _try_letter(self, letter):
        if letter.isalpha():
            if letter in self.mot:
                for i, char in enumerate(self.mot):
                    if char == letter:
                        self.finded_letter[i] = letter
                return True
            else:
                return False
        else:
            logging.error("Input de l'entrée lettre non valide")
            raise ValueError("L'input doit etre une lettre !")
    
    def _show_word(self):
        self.finded_letter = [l for l in self.mot]
    
if __name__ == "__main__":
    m = Mot()
    print(m)
    print(m.finded_letter)