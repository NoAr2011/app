from reading_text_files import *
from load_chapters import *

class GlobalData:
    def __init__(self):
        self.db_search = DataSelect()
        self.get_next = ExtractingNext()
        self.adding_to_db = AddingData()
        self.pop_ups = PopUpsForGame()

        self.checking_luck = "tedd próbára"
        self.read_files = ReadFile()
        self.textinput_main_font = adaptive_sp(18)
        self.button_main_font = adaptive_sp(18)
        self.get_chapters = LoadingChapters()