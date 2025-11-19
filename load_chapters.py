from fight_and_luck import *
from extracting_chapter_numbers import *


class LoadingChapters:
    db_search = DataSelect()
    get_next = ExtractingNext()
    checking_luck = "tedd próbára"
    adding_fight_luck = AddButtons()

    def target_chapter(self, player_data, target_screen, book_title_text, book_title, chapter_grid):

        if len(player_data) < 1:

            actual_chapter = self.db_search.select_target_chapter(book_title_text, 0)
            target_screen.ids["current_chapter"].text = "0"
        else:
            target_screen.ids["player_name"].text = player_data[2]

            target_screen.ids["start_dexterity"].text = str(player_data[3])  # start dex
            target_screen.ids["start_health"].text = str(player_data[4])  # start hp
            target_screen.ids["start_luck"].text = str(player_data[5])  # start luck
            target_screen.ids["actual_dexterity"].text = str(player_data[6])  # act dex
            target_screen.ids["actual_health"].text = str(player_data[7])  # act hp
            target_screen.ids["actual_luck"].text = str(player_data[8])  # act luck
            target_screen.ids["current_chapter"].text = str(player_data[9])

            actual_chapter = self.db_search.select_target_chapter(book_title_text, player_data[9])  # chapter
            actual_chapter_lowercase = actual_chapter.lower()
            splited_text = actual_chapter_lowercase.split("lapozz")

            self. check_buttons(splited_text, chapter_grid, target_screen, actual_chapter_lowercase)

        return actual_chapter

    def next_chapter(self, screen, instance):
        screen.clear_chapter_buttons()
        text_input = screen.ids["chapter_text"]

        book_title = screen.ids["book_title"].text
        actual_chapter = self.db_search.select_target_chapter(book_title, int(instance.text))
        actual_chapter_lowercase = actual_chapter.lower()
        splited_text = actual_chapter_lowercase.split("lapozz")
        chapter_grid = screen.ids["chapter_grid"]
        current_chapter = screen.ids["current_chapter"]
        current_chapter.text = instance.text

        self. check_buttons(splited_text, chapter_grid, screen, actual_chapter_lowercase)

        text_input.text = actual_chapter

    def check_buttons(self, splited_text, chapter_grid, screen, actual_chapter_lowercase):
        page_split = self.get_next.get_next_chapters(splited_text)

        self.get_next.add_new_buttons(chapter_grid, page_split, screen)

        book_id = self.db_search.get_book_id(screen.ids["book_title"].text)

        monster_info = self.db_search.get_monsters(book_id, screen.ids["current_chapter"].text)

        if len(monster_info) > 0:
            self.adding_fight_luck.fight_luck_button(screen, monster_info, chapter_grid)

        if self.checking_luck in actual_chapter_lowercase:
            self.adding_fight_luck.fight_luck_button(screen, {}, chapter_grid)