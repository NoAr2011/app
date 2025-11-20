from kivy.graphics.svg import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from global_values import *

GLOBALS = GlobalData()

class WindowManager(ScreenManager):
    pass


class StartScreen(Screen):
    def on_kv_post(self, base_widget):
        Clock.schedule_once(self.populate_books, 0.1)

    def populate_books(self, *args):

        books = ["A Gyikkiraly Szigete", "A Hoboszorkany Barlangjai", "A Remulet Utvesztoje", "A Varazslo Kriptaja",
            "A Vegzet Erdeje", "Az Orszagut Harcosa", "Bajnokok Probaja", "Halallabirintus", "Tolvajok Varosa"]

        grid = self.ids["book_main_grid"]
        grid.clear_widgets()

        for title in books:

            btn = Button(
                text=title,
                color=(0, 0, 0, 0),
                size_hint=(None, None),
                size=(self.width / 4, self.height / 4),
                background_normal=title + ".jpg"
            )
            btn.bind(on_release=self.select_book)
            grid.add_widget(btn)

    def select_book(self, instance):
        app_globals = GLOBALS

        current_app = App.get_running_app()
        root_screen = current_app.root
        target_screen = root_screen.get_screen("book")
        chapter_grid = target_screen.ids["chapter_grid"]
        book_title = target_screen.ids["book_title"]
        book_title.text = instance.text
        book_title_text = target_screen.ids["book_title"].text

        player_data = app_globals.db_search.get_player(book_title_text)

        main_grid = target_screen.ids["main_grid"]
        main_grid.background = book_title.text + ".jpg"

        self.manager.current = "book"

        text_input = target_screen.ids["chapter_text"]

        text_input.text = app_globals.get_chapters.target_chapter(player_data, target_screen, book_title_text,
                                                      book_title, chapter_grid)

class BookScreen(Screen):
    app_globals = GLOBALS
    textinput_font = app_globals.textinput_main_font
    button_font = app_globals.button_main_font

    def clear_all_widgets(self):
        self.clear_chapter_buttons()

        self.ids["player_name"].text = ""
        self.ids["start_dexterity"].text = ""
        self.ids["start_health"].text = ""
        self.ids["start_luck"].text = ""
        self.ids["actual_dexterity"].text = ""
        self.ids["actual_health"].text = ""
        self.ids["actual_luck"].text = ""

    def clear_chapter_buttons(self):
        chapter_grid = self.ids["chapter_grid"]
        chapter_grid.clear_widgets()

    def next_chapter(self, instance):

        if self.ids["player_name"].text != "":
            self.app_globals.get_chapters.next_chapter(self, instance)

    def jump_to_chapter(self):

        chapter_input = self.ids["target_chapter"]

        if self.ids["player_name"].text != "" and chapter_input.text != "":

            self.app_globals.get_chapters.next_chapter(self, chapter_input)

        else:
            self.app_globals.pop_ups.warning_popup(self, "Nincs karakter vagy oldalszám!")

    def save_state(self):
        if self.ids["player_name"].text != "":
            self.app_globals.adding_to_db.save_progress(self.ids["actual_dexterity"].text,
                                       self.ids["actual_health"].text,
                                       self.ids["actual_luck"].text,
                                       self.ids["current_chapter"].text,
                                       self.ids["player_name"].text)

            self.app_globals.pop_ups.warning_popup(self, "Mentés sikeres!")
        else:
            self.app_globals.pop_ups.warning_popup(self, "Előbb alkoss egy karaktert!")

    def book_name(self):
        current_app = App.get_running_app()
        root_screen = current_app.root
        target_screen = root_screen.get_screen("newPlayer")
        target_screen.ids["book_name"].text = self.ids["book_title"].text
        target_screen.ids["chapter"].text = self.ids["current_chapter"].text

    def backpack_edit(self, instance):
        if self.ids["player_name"].text != "":
            if instance == "Felszerelés":
                target_table = "equipment"
            else:
                target_table = "spells"

            player_data = self.app_globals.db_search.get_player_equipment(target_table, self.ids["player_name"].text,
                                                                          self.ids["book_title"].text)
            player_id = self.app_globals.db_search.get_player_id(self.ids["player_name"].text,
                                                                 self.ids["book_title"].text)

            self.app_globals.pop_ups.player_stuff(self, instance, player_id, player_data)
        else:
            self.app_globals.pop_ups.warning_popup(self, "Előbb alkoss egy karaktert!")

    def backpack_new(self, instance):
        if self.ids["player_name"].text != "":
            player_id = self.app_globals.db_search.get_player_id(self.ids["player_name"].text,
                                                                 self.ids["book_title"].text)

            self.app_globals.pop_ups.player_stuff(self, instance, player_id, {})
        else:
            self.app_globals.pop_ups.warning_popup(self, "Előbb alkoss egy karaktert!")

    def options_spinner(self, instance):

        if instance.text == "Játékszabályok":
            current_app = App.get_running_app()
            root_screen = current_app.root
            target_screen = root_screen.get_screen("rules")
            target_textInput = target_screen.ids["rules"]
            rules_data = self.app_globals.read_files.read_rules()

            target_textInput.text = rules_data

            self.manager.current = "rules"
            instance.text = " ... "

        if instance.text == "Új Karakter":
            self.manager.current = "newPlayer"
            self.book_name()
            self.clear_chapter_buttons()
            instance.text = " ... "


class GameRules(Screen):
    pass


class NewPlayer(Screen):
    app_globals = GLOBALS
    textinput_font = app_globals.textinput_main_font
    button_font = app_globals.button_main_font

    def save_player(self):

        player_name = self.ids["player_name"].text
        dexterity = self.ids["start_dexterity"].text
        health = self.ids["start_health"].text
        luck = self.ids["start_luck"].text
        chapter = self.ids["chapter"].text

        if player_name != "" and dexterity != "" and health != "" and luck != "":

            book_id = self.app_globals.db_search.get_book_id(self.ids["book_name"].text)

            if 0 < int(dexterity) < 13 and 0 < int(health) < 25 and 0 < int(luck) < 13:

                existing_player =  self.app_globals.db_search.get_player(self.ids["book_name"].text)
                existing_name = self.app_globals.db_search.get_player_id_name(player_name)

                if len(existing_name) > 0:
                    self.app_globals.pop_ups.warning_popup(self, "Ezzel a névvel mér regisztráltál karaktert!")
                    return

                if len(existing_player) > 0:
                    warning_text = "Módosítod a meglévő karaktered? Mindened törlődik!"
                    self.app_globals.pop_ups.change_player_warning(self, warning_text, dexterity, health, luck, chapter,
                                                  player_name, book_id)
                else:
                    self.app_globals.adding_to_db.register_new_player(player_name, dexterity, health, luck, book_id, chapter)
                    self.app_globals.pop_ups.warning_popup(self, "Karakter regisztrálva!")
            else:
                self.app_globals.pop_ups.warning_popup(self, "túllépted a maximum értéket!")
        else:
            self.app_globals.pop_ups.warning_popup(self, "Tölts ki Minden mezőt!")

    def clear_all_widgets(self):
        self.ids["player_name"].text = ""
        self.ids["start_dexterity"].text = ""
        self.ids["start_health"].text = ""
        self.ids["start_luck"].text = ""
        self.ids["chapter"].text = ""
        self.ids["target_chapter"] = ""

        self.add_data_book_screen()

    def generate_player(self):
        dexterity = random.randrange(1, 7) + 6  # D6+6
        health = random.randrange(1, 7) + random.randrange(1, 7) + 12  # 2D6 +12
        luck = random.randrange(1, 7) + 6  # D6+6
        self.ids["start_dexterity"].text = str(dexterity)
        self.ids["start_health"].text = str(health)
        self.ids["start_luck"].text = str(luck)

    def add_data_book_screen(self):
        current_app = App.get_running_app()
        root_screen = current_app.root
        target_screen = root_screen.get_screen("book")
        chapter_grid = target_screen.ids["chapter_grid"]

        book_title = self.ids["book_name"]

        player_data = self.app_globals.db_search.get_player(book_title.text)

        text_input = target_screen.ids["chapter_text"]

        text_input.text = self.app_globals.get_chapters.target_chapter(player_data, target_screen,
                                                                                 book_title.text, book_title,
                                                                                 chapter_grid)


kv = Builder.load_file("gui.kv")


class MainApp(App):

    def build(self):

        if platform == 'android' or platform == 'ios':
            Window.maximize()
        else:
            Window.size = (600, 700)
        return WindowManager()


if __name__ == "__main__":
    MainApp().run()
