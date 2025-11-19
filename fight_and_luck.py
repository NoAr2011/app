from database_search import *
from pop_up_windows import *


class AddButtons:
    db_search = DataSelect()
    pop_ups = PopUpsForGame()


    def fight_luck_button(self, screen, monster_info, chapter_grid):
        page_button = Button()
        is_fight = True

        if len(monster_info) > 0:
            page_button.text = "Harc"
        else:
            page_button.text = "Szerencse\nPróba!"
            is_fight = False

        page_button.background_normal = "button09.png"
        page_button.border = (0, 0, 0, 0)
        page_button.bind(on_release=lambda instance: self.pop_ups.fight_luck_popup(screen, monster_info, is_fight))
        chapter_grid.cols = chapter_grid.cols + 1
        chapter_grid.add_widget(page_button)

