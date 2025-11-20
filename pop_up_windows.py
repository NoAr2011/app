from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from widgtes import *
from game_logic import *


class PopUpsForGame:
    game_logic = ImplementGameLogic()
    text_input_image = "button10.png"
    label_image = "button03.png"
    button_image = "button09.png"

    @staticmethod
    def warning_popup(screen, warning_text):
        content = GridLayout()
        content.cols = 1
        content.spacing = 30

        item_label = NewTextInput(18)
        item_label.text = warning_text
        item_label.readonly = True

        content.add_widget(item_label)

        info_popup = InforPopup(content, screen, 2.5)

        close_button = ClosingButton()
        close_button.on_release = info_popup.dismiss

        close_button.size = screen.width/7, screen.height/8

        content.add_widget(close_button)

        info_popup.open()

    def change_player_warning(self, screen, warning_text, dex_start, hp_start, luck_start, chapter,
                              player_name, book_id):
        content = GridLayout()
        content.cols = 1
        content.spacing = 30

        item_label = NewTextInput(16)
        item_label.text = warning_text

        item_label.readonly = True

        content.add_widget(item_label)

        info_popup = InforPopup(content, screen, 2)

        button_grid = GridLayout()
        button_grid.cols = 2

        ok_button = ClosingButton()
        ok_button.text = "Igen"
        ok_button.on_release = info_popup.dismiss

        ok_button.size = screen.width / 2.5, screen.height / 8
        ok_button.bind(on_release=lambda instance: self.game_logic.change_player(self, screen, dex_start, hp_start,
                                                                                 luck_start, chapter, player_name,
                                                                                 book_id))

        close_button = ClosingButton()
        close_button.text = "Mégsem"
        close_button.on_release = info_popup.dismiss

        close_button.size = screen.width / 7, screen.height / 8

        button_grid.add_widget(ok_button)
        button_grid.add_widget(close_button)
        content.add_widget(button_grid)

        info_popup.open()

    @staticmethod
    def make_row(screen, target_widget, col_size, name, desc, quant):
        row = GridLayout(cols=col_size, size_hint_y=None, size=(screen.width / 2, screen.height / 8))
        row.add_widget(NewLabel(text=name))
        desc_text = NewTextInput(18)
        desc_text.text = desc
        row.add_widget(desc_text)
        quant_text = NewTextInput(18)
        quant_text.text = quant
        row.add_widget(quant_text)
        target_widget.add_widget(row)

    def player_stuff(self, screen, button_text, player_id, player_data):
        content = GridLayout(cols=1, spacing=5)

        header = GridLayout(cols=3, spacing=10, size_hint_y=None,size =(screen.width / 2, screen.height / 8))

        for title in ["Megnvezés", "Leírás", "Mennyiség"]:
            header.add_widget(NewLabel(text=title))

        content.add_widget(header)

        info_popup = InforPopup(content, screen, 1.2)
        info_popup.title = button_text

        stuff_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        stuff_grid.bind(minimum_height=stuff_grid.setter('height'))

        stuff_scroll = ScrollView(size_hint_y=None, size=(screen.width / 1.2, screen.height / 2.4))
        stuff_scroll.add_widget(stuff_grid)

        if len(player_data) > 0:
            for i in range(0, len(player_data), 3):
                self.make_row(screen, stuff_grid, 3, player_data[i], player_data[i+1], str(player_data[i+2]))

        else:
            temp_grid = GridLayout()
            temp_grid.cols = 3
            temp_grid.size_hint_y = None
            temp_grid.size = screen.width / 2, screen.height / 8

            name_text = NewTextInput(14)
            desc_text = NewTextInput(16)
            quant_text = NewTextInput(16)

            temp_grid.add_widget(name_text)
            temp_grid.add_widget(desc_text)
            temp_grid.add_widget(quant_text)

            stuff_grid.add_widget(temp_grid)

        content.add_widget(stuff_scroll)
        button_grid = GridLayout()
        button_grid.cols = 2

        ok_button = ClosingButton()

        ok_button.text = "Mentés"
        ok_button.size_hint_y = None
        ok_button.size = screen.width / 7, screen.height / 8

        if len(player_data) > 0:

            ok_button.bind(on_release=lambda instance: self.game_logic.update_backpack(self, button_text, screen,
                                                                                       player_id, stuff_grid))
        else:
            ok_button.bind(on_release=lambda instance: self.game_logic.new_backpack_item(self, button_text, screen,
                                                                                         player_id, name_text.text,
                                                                                         desc_text.text,
                                                                                         quant_text.text))
        close_button = ClosingButton()
        close_button.on_release = info_popup.dismiss
        close_button.size_hint_y = None
        close_button.size = screen.width / 7, screen.height / 8

        button_grid.add_widget(ok_button)
        button_grid.add_widget(close_button)
        content.add_widget(button_grid)
        info_popup.open()

    def fight_luck_popup(self, screen, monster_info, fight):

        current_app = App.get_running_app()
        target_screen = current_app.root.get_screen("book")
        player_name = target_screen.ids["player_name"].text

        content = GridLayout(cols=1, spacing=30)

        header = GridLayout(cols=4, spacing=10, size_hint_y=None, size=(screen.width / 2, screen.height / 10))

        scroll_widget = ScrollView()
        scroll_widget.size_hint_y = None
        scroll_widget.size = screen.width / 1.3, screen.height / 4

        main_grid = GridLayout(cols=4, spacing=10, size_hint_y=None,)
        main_grid.bind(minimum_height=main_grid.setter('height'))

        scroll_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)

        scroll_grid.bind(minimum_height=scroll_grid.setter('height'))

        scroll_grid.add_widget(main_grid)
        scroll_widget.add_widget(scroll_grid)
        name_label = NewLabel(text="Név")
        header.add_widget(name_label)

        player_name_text = NewLabel(text=player_name)
        main_grid.add_widget(player_name_text)

        if fight:
            title_text = "Harc"
            player_health = target_screen.ids["actual_health"].text
            player_dext = target_screen.ids["actual_dexterity"].text
            desc_label = NewLabel()
            desc_label.text = "Ügysség"
            quant_label = NewLabel()
            quant_label.text = "Életerő"

            header.add_widget(desc_label)
            header.add_widget(quant_label)

            player_dext_text = NewLabel()
            player_hp_text = NewLabel()

            player_dext_text.text = player_dext
            player_hp_text.text = player_health

            main_grid.add_widget(player_dext_text)
            main_grid.add_widget(player_hp_text)

        else:
            title_text = "Szerencse próba"
            player_luck = target_screen.ids["actual_luck"].text
            luck_label = NewLabel()

            luck_label.text = "Szerencse"

            header.add_widget(luck_label)

            player_luck_text = NewLabel()
            player_luck_text.text = player_luck

            main_grid.add_widget(player_luck_text)

        dice_label = NewLabel()
        dice_label.text = "Dobott érték"
        header.add_widget(dice_label)

        player_dice_text = NewTextInput(18)

        main_grid.add_widget(player_dice_text)

        content.add_widget(header)

        info_popup = InforPopup(content, screen, 1.5)
        info_popup.title = title_text

        for i in range(0, len(monster_info), 3):
            enemy_name_text = NewLabel()
            enemy_dext_text = NewLabel()
            enemy_hp_text = NewLabel()
            enemy_dice_text = NewTextInput(18)

            enemy_name_text.text = monster_info[i]
            enemy_dext_text.text = str(monster_info[i + 1])
            enemy_hp_text.text = str(monster_info[i + 2])

            main_grid.add_widget(enemy_name_text)
            main_grid.add_widget(enemy_dext_text)
            main_grid.add_widget(enemy_hp_text)
            main_grid.add_widget(enemy_dice_text)

        content.add_widget(scroll_widget)

        button_grid = GridLayout()
        button_grid.cols = 3

        generate_button = ClosingButton()

        generate_button.text = "Kocka\ndobás"
        generate_button.size_hint_y = None
        generate_button.size = screen.width / 7, screen.height / 8

        if fight:
            generate_button.bind(on_release=lambda instance: self.game_logic.generate_dice(main_grid))

            fight_button = ClosingButton()
            fight_button.text = "Harc\nindítása"
            fight_button.size_hint_y = None
            fight_button.size = screen.width / 7, screen.height / 8
            fight_button.bind(on_release=lambda instance: self.game_logic.fight_enemy(self, screen, main_grid))
            button_grid.add_widget(fight_button)

        else:
            generate_button.bind(
                on_release=lambda instance: self.game_logic.generate_luck(self, screen, player_dice_text,
                                                                          player_luck_text, player_name))

        close_button = ClosingButton()
        close_button.on_release = info_popup.dismiss
        close_button.size_hint_y = None
        close_button.size = screen.width / 7, screen.height / 8

        button_grid.add_widget(generate_button)
        button_grid.add_widget(close_button)
        content.add_widget(button_grid)
        info_popup.open()





