# Adventure

Az alkalmazás a kalandjáték-kockázat könyveken alapuló interaktív játék mely 
igyekszik követni az eredeti könyvek szellemét és nem kényszeríti rá a 
játékosra a szabályokat.

A játék működése:

- A játékos egy könyvet választ.
- Betölti a hozzá tartozó fejezetet.
- A szöveg alapján tovább lapozhat megadott fejezetekre.
- Harcot indíthat szörnyek ellen (ügyesség + életerő rendszer).
- Szerencsepróbát tehet.
- Tárgyakat, felszerelést, varázslatokat kezelhet.
- Minden adat (életerő, szerencs, ügyesség, tárgyak, fejezet) **SQLite adatbázisban** mentődik.

---

# Modulok és funkciók

## db_connection.py
SQLite kapcsolat nyitása:

- MainConnection.return_main_connection()
  Megnyitja a fő adatbázis kapcsolatot (Kalandjatek.db)

---

## database_search.py
Adatbázis-lekérdezések:

- select_target_chapter(book_name, chapter)
- get_book_id(book_name)
- get_player(book_name)
- get_player_equipment(table, player_name)
- get_player_id(player_name)
- get_monsters(book_id, chapter)

---

## insert_into_db.py
Adatok írása az adatbázisba:

- register_new_player()
- save_progress()
- update_player()
- update_player_stuff()
- add_new_player_stuff()
- update_player_luck()
- update_player_hp()

---

## game_logic.py
A harcok és szerencsepróbák logikája:

- Kockadobás
- Harc lebonyolítása
- HP/Luck frissítés
- Tárgy felvétele / módosítása

---

## load_chapters.py
A fejezetek betöltése, lapozás:

- target_chapter()
- next_chapter()
- Gombok generálása a következő fejezetekhez
- Szörnyek automatikus felismerése az aktuális fejezethez

---

## extracting_chapter_numbers.py
A fejezet szövegéből automatikusan kivonja a „lapozz …” részeket, és megtalálja a következő fejezet számokat.

---

## pop_up_windows.py
A játék összes Popup ablakát kezeli:

- Harc popup
- Szerencsepróba popup
- Figyelmeztetések
- Tárgykezelő ablak
- Igen/Nem megerősítés

---

## widgets.py
Egységes megjelenésű custom Kivy widgetek:

- NewLabel
- NewTextInput
- BaseButton
- ClosingButton
- InforPopup

---

## adaptive_font_size.py
Készülékfüggő betűméret:

- adaptive_sp() — Androidon és iOS-en automatikusan skálázza a betűméretet

## global_values.py
A teljes alkalmazás alapvető komponenseit egy helyre szervezi.

- GlobalData 

Ez az osztály biztosítja a játék globális logikájának és szolgáltatásainak központi elérési pontját.

## gui.kv
Az alkalmazás teljes grafikus felülete Kivy KV nyelven van felépítve.

---

# Fő funkciók a játékban

### Fejezetek közti lapozás  
A szövegben megtalálja a „lapozz X”-et, és gombokat hoz létre a továbblépéshez.

### Harcrendszer  
Két D6 dobással számolja a támadó értékeket, majd életerőt csökkent.

### Szerencsepróba  
Két D6 dobás melyet összehasonlítja a játékos szerencséjével.

### Felszerelés és varázslatok kezelése  
Popupban megjeleníti a tárgyakat, szerkesztést enged, majd visszament az adatbázisba.

### Karakter állapotának mentése  
Életerő, szerencs, ügyesség, aktuális fejezet és tárgyak automatikusan mentődnek.

### Reszponzív UI  
Minden gomb, label és input egyedi widget, egységes háttérképpel és méretezéssel.

---

# Készítette: Bihari Richárd