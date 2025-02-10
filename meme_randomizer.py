# Imports
import random                       # für die zufällige Ausgabe der Memes
import os                           # Interaktion mit dem Betriebssystem, in diesem Fall Zugriff auf die Dateien der Memes
import tkinter as tk 
from tkinter import filedialog, colorchooser, font# GUI für die grafische Benutzeroberfläche
from PIL import Image, ImageTk, ImageOps      # Bibliothek für Bildverarbeitung; Image=Klasse für Bilder öffnen, bearbeiten und speichern; ImageTk=Schnittstelle zu Tkinter
from tkinter import messagebox      # ermöglicht Pop-up Nachrichten
import emoji

# Dictionary mit Ordnern mit Memes nach Kategorie
CATEGORIES = {
    "Tiere": 
    {"Hunde": r"memes\Tiere\Hunde",
     "Katzen": r"memes\Tiere\Katzen",
     "Hund+Katze": r"memes\Tiere\Hund+Katze",
     "Katze+Maus": r"memes\Tiere\Katze+Maus",
     "Elefant": r"memes\Tiere\Elefant",
     "Maus": r"memes\Tiere\Maus",
     "Wildtiere": r"memes\Tiere\Wildtiere",
     "Meerestiere":r"memes\Tiere\Meerestiere",
     "Vögel": r"memes\Tiere\Vögel"},
     "Emotionen": 
     {"Glücklich": r"memes\Emotionen\Glücklich",
      "Traurig": r"memes\Emotionen\Traurig",
      "Verwirrt": r"memes\Emotionen\Verwirrt"},
    "Gaming": r"memes\Gaming",
    "IT": r"memes\IT",
    "Deutsch": r"memes\Deutsch",
    "Kochen": r"memes\Kochen",
    "Musik": r"memes\Musik"}

# Meme-Randomizer starten
def start_meme_randomizer():
    start_window.destroy()

    global root                                         
    root = tk.Tk()                                      # Hauptfenster
    root.title("Meme Randomizer")                       # gibt dem Fenster einen Titel
    root.configure(bg="grey25")                         # grauer Hintergrund

    def show_categories():
        for widget in frame.winfo_children():
            widget.destroy()                            # entfernt die bestehenden Widgets
        meme_label.config(image="", text="")            # löscht Bild und Text im Labek

        for category in CATEGORIES:
            if isinstance(CATEGORIES[category], dict):
                btn = tk.Button(frame, text=category, font=("Alasassy Caps", 12), fg="white", bg="grey25", command=lambda c=category: show_subcategories(c))
            else:
                btn = tk.Button(frame, text=category, font=("Alasassy Caps", 12), fg="white", bg="grey25", command=lambda c=category: show_random_meme(c, None))
            btn.pack(side=tk.LEFT, padx=10, pady=5)     # fügt die Buttons ins frame ein

    def show_subcategories(category):
        for widget in frame.winfo_children():
            widget.destroy()                            # entfernt bestehende Widgets
        for subcategory in CATEGORIES[category]:        # iteriert durch die Unterkategorrien
            btn = tk.Button(frame, text=subcategory, font=("Alasassy Caps", 12), bg="gray25", command=lambda c=category, s=subcategory: show_random_meme(c, s))
            btn.pack(side=tk.LEFT, padx=10, pady=5)     # bettet den Button für die Unterkategorien ein

        back_btn = tk.Button(frame, text="← Zurück", font=("Alasassy Caps", 12), fg="white", bg="grey20", command= show_categories)  # definiert den Zurück-Button
        back_btn.pack(side=tk.LEFT, padx=10, pady=5)   # bettet den Button im Tkinter-Fenster ein, mit automatischer Skallierung des Buttons; Abstand zu anderen Objekten 10 Pixel horizontal und 5 Pixel vertikal
    
    # Frame-Widget mit Scroll-Leiste erstellen
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root,orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, background= "grey25")    # erstellt ein Frame-Widget im Hauptfenster mit grauem Hintergrund, das als Container für die Buttons dient
    frame.pack()                        # bettet das Frame in das Fenster ein
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)            # bettet die Scroll-Leiste ein

    # Suchfeld zur GUI hinzufügen
    search_var = tk.StringVar()                             # Variable für den Suchbegriff

    search_entry = tk.Entry(root, textvariable=search_var, font=("Alasassy Caps", 12))  # Eingabefeld im Hauptfenster root erstellen und Ergebnis in Variable speichern
    search_entry.pack(pady=10)  # Abstand zur Leserlichkeit                                   # und einbetten

    search_button = tk.Button(root, text="🔍 Suchen", font=("Alasassy Caps", 12), 
                          fg="white", bg="grey20",  command=lambda: search_memes(search_var.get()))   # Suchbutton erstellen
    search_button.pack() # und einbetten

    # Suchfunktion
    def search_memes(query):
        query = query.lower()   # alles klein schreiben um Suche zu vereinfachen
        results = []            # Leere Liste für die Dateipfade der Suchergebnisse

        for category, value in CATEGORIES.items():                              # iteriert durch alle Kategorien und Unterkategorien
            if isinstance(value, dict):                                         # falls es Unterkategorien gibt (value=dict)
                for subcategory, path in value.items():                         # iteriert durch alle Bilder der Unterkategorie
                    if os.path.exists(path):                                    # prüft ob der Ordner existiert
                        for filename in os.listdir(path):                       # geht alle Dateien im Ordner durch und sucht nach Übereinstimmungen
                            if query in filename.lower():                       # falls der Dateiname den Suchbegriff enthält
                                results.append(os.path.join(path, filename))    # wird der Pfad der Liste results hinzugefügt
            else:                                                               
                    if os.path.exists(value):                                   # falls es keine Unterkategorie gibt
                        for filename in os.listdir(value):
                            if query in filename.lower():
                                results.append(os.path.join(value, filename))

            if not results:                                                         # falls nichts gefunden wurde
                meme_label.config(text="Keine Ergebnisse gefunden", image="")
                return
    
        for widget in frame.winfo_children():                                   # löscht alle bisherigen Buttons im frame, damit nur die neuen Suchergebnisse angezeigt werden
            widget.destroy()

        for meme_path in results:                                               # iteriert durch alle gefundenen Ergebnisse
            btn = tk.Button(frame, text=os.path.basename(meme_path), font=("Alasassy Caps", 12), fg="white", bg="grey20",           # und erstellt einen Button der dann bei Klick das jeweilige Meme anzeigt
                        command=lambda path=meme_path: show_meme(path))
            btn.pack()                                                          # bettet die Buttons ins Fenster ein
    
    # Meme öffnen für die Suchfunktion
    def show_meme(meme_path):
        if not os.path.exists(meme_path): # falls die Datei nicht mehr exestiert
            meme_label.config(text="Fehler: Datei nicht gefunden", image="")
            return
    
        img = Image.open(meme_path)     # öffnet das Bild
        img = img.resize((500,500))     # passt die Größe an
        img = ImageTk.PhotoImage(img)   # wandelt in Tkinter-Format um

        meme_label.config(image=img)    # Tkinter Widget zur Bildverarbeitung
        meme_label.image = img          # Referenz speichern

    # Funktion die ein Meme zufällig auswählt
    def show_random_meme(category, subcategory=None):    
        if subcategory:
            folder = CATEGORIES[category][subcategory]   # der Ordner der die Memes der ausgewählten Kategorie enthält
        else:
            folder = CATEGORIES[category]

        memes = os.listdir(folder)                      # listet alle Dateien des gewählten Ordners auf
    
        if not memes:                                   # falls kein Meme gefunden wurde 
            meme_label.config(text="Keine Memes gefunden", image="")
            return
    
        random_meme = random.choice(memes)              # wählt zufällig ein Meme aus
        meme_path = os.path.join(folder, random_meme)   # kombiniert den Ordnerpfad mit dem ausgewählten Meme, um den vollständigen Dateipfad zu erhalten

        img = Image.open(meme_path)                     # öffnet das zufällig ausgewählte Meme
        img = img.resize((500,500))                     # Größe anpassen 500x500 Pixel
        img = ImageTk.PhotoImage(img)                   # wandelt in ein Tkinter Format um

        meme_label.config(image=img)                    # Tkinter Widget zur Bilddarstellung
        meme_label.image = img                          # Referenz speichern

        for widget in frame.winfo_children():
            widget.destroy()                            # vorherige Buttons entfernen

        back_btn = tk.Button(frame, text="← Zurück", font=("Alasassy Caps", 12), fg="white", bg="grey20", command= show_categories)  # definiert den Zurück-Button
        back_btn.pack(side=tk.LEFT, padx=10, pady=5)   # bettet den Button im Tkinter-Fenster ein, mit automatischer Skallierung des Buttons; Abstand zu anderen Objekten 10 Pixel horizontal und 5 Pixel vertikal

    back_btn = tk.Button(frame, text="← Zurück", font=("Alasassy Caps", 12), fg="white", bg="grey20", command=show_categories)   # erstellt den Zurück-Button
    back_btn.pack()
    # Label für das Bild
    meme_label = tk.Label(root)         # Erstellung eines Label-Widgets im Hauptfenster, wo das Meme drauf plaziert wird
    meme_label.pack()                   # bettet das Label in der Benutzeroberfläche ein

    show_categories()

    root.mainloop()                     # startet die Tkinter-Anwendung, Fenster bleibt geöffnet und reagiert auf Benutzerinteraktionen

# Startfenster erstellen
start_window = tk.Tk()
start_window.title("Meme-Startmenü")
start_window.geometry("400x300")

label = tk.Label(start_window, text="Willkommen! Wähle eine Option:",font=("Alasassy Caps", 14))
label.pack(pady=20)

btn_randomizer = tk.Button(start_window, text="Meme Randomizer", font=("Alasassy Caps", 12), command=start_meme_randomizer)
btn_randomizer.pack(pady=10)


class MemeGenerator:
    def __init__(self, root):
        # Initialisiere das Hauptfenster des Programms und grundlegende Variablen
        self.root = root
        self.root.title("Meme Generator")

        # Erstelle ein Canvas (Zeichenfläche), auf dem das Bild und Text angezeigt werden
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Variablen für das Bild, die Tkinter-kompatible Version und Textobjekte
        self.img = None  # Das Bild, das bearbeitet wird
        self.tk_img = None  # Tkinter-kompatibles Bild, das auf dem Canvas angezeigt wird
        self.text_items = []  # Liste zur Speicherung der Textobjekte, die hinzugefügt werden
        self.current_text = None  # Der aktuell ausgewählte Text
        self.x, self.y = 400, 300  # Startkoordinaten für das Bild und den Text auf dem Canvas

        # Erstellen der Buttons im unteren Bereich des Fensters
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        # Button-Layout: Liste von Buttons mit jeweils einer Funktion, die aufgerufen wird
        buttons = [
            ("Bild hochladen", self.upload_image),
            ("Text hinzufügen", self.add_text),
            ("Text bearbeiten", self.edit_text),
            ("Emoji auswählen", self.show_emoji_selection),
            ("Rahmen hinzufügen", self.add_border),
            ("Bild verschieben", self.move_image),
            ("Bild zuschneiden", self.crop_image),
            ("Bild drehen", self.rotate_image),
            ("Bildgröße anpassen", self.resize_image),
            ("Speichern", self.save_image),
            ("Rückgängig", self.undo),  # Rückgängig-Button
            ("Schriftfarbe ändern", self.change_text_color),
            ("Hintergrundfarbe ändern", self.change_background_color)
        ]

        # Buttons im Layout anordnen (4 Buttons pro Zeile)
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(self.button_frame, text=text, command=command)
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)

        # Emojis-Liste
        self.emoji_list = [
            ":grinning_face:", ":face_with_tears_of_joy:", ":red_heart:",
            ":dog_face:", ":sunglasses:", ":heart_eyes:", ":thinking_face:",
            ":cat_face:", ":unicorn_face:", ":skull:"
        ]
        self.emoji_selection_window = None  # Fenster für die Emoji-Auswahl

    def upload_image(self):
        # Funktion, um ein Bild vom Computer hochzuladen
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.img = Image.open(file_path)  # Das ausgewählte Bild öffnen
            self.display_image()  # Bild auf der Canvas anzeigen

    def display_image(self):
        # Funktion, um das Bild im Tkinter-kompatiblen Format anzuzeigen
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.x, self.y, image=self.tk_img, anchor=tk.CENTER, tags="moveable_image")

    def add_text(self):
        # Funktion, um Text auf das Bild hinzuzufügen
        self.current_text = self.canvas.create_text(self.x, self.y, text="Text", fill="black", font=("Arial", 20), tags="editable")
        self.text_items.append(self.current_text)  # Speichern der Text-ID

        # Text auswählbar und verschiebbar machen
        self.canvas.tag_bind(self.current_text, "<Button-1>", self.select_text)  # Text auswählen
        self.canvas.tag_bind(self.current_text, "<B1-Motion>", self.move_text)  # Text mit der Maus bewegen

    def select_text(self, event):
        # Funktion zum Auswählen und Bearbeiten des Textes
        self.current_text = event.widget.find_closest(event.x, event.y)[0]  # Nähesten Text-Objekt finden
        self.edit_text()  # Text bearbeiten

    def move_text(self, event):
        # Funktion, um den Text mit der Maus zu verschieben
        new_x = event.x
        new_y = event.y
        self.canvas.coords(self.current_text, new_x, new_y)  # Textposition auf der Canvas aktualisieren
        self.x, self.y = new_x, new_y  # Koordinaten für den Text speichern

    def edit_text(self):
        # Funktion, um den ausgewählten Text zu bearbeiten
        if self.current_text:
            edit_window = tk.Toplevel(self.root)  # Neues Fenster für Textbearbeitung
            edit_window.title("Text bearbeiten")
            entry = tk.Entry(edit_window)  # Eingabefeld für neuen Text
            entry.pack()

            # Funktion zum Speichern des neuen Textes
            def update_text():
                new_text = entry.get()  # Neuer Text aus dem Eingabefeld
                self.canvas.itemconfig(self.current_text, text=new_text)  # Text auf Canvas aktualisieren
                edit_window.destroy()  # Fenster schließen

            tk.Button(edit_window, text="Speichern", command=update_text).pack()

    def change_text_color(self):
        # Funktion, um die Schriftfarbe zu ändern
        color = colorchooser.askcolor()[1]  # Farbwahl für die Schrift
        if color and self.current_text:
            self.canvas.itemconfig(self.current_text, fill=color)  # Textfarbe ändern

    def change_background_color(self):
        # Funktion, um die Hintergrundfarbe des Texts zu ändern
        color = colorchooser.askcolor()[1]  # Farbwahl für den Hintergrund
        if color and self.current_text:
            self.canvas.itemconfig(self.current_text, background=color)  # Hintergrundfarbe ändern

    def show_emoji_selection(self):
        # Funktion, um das Emoji-Auswahlfenster anzuzeigen
        if self.emoji_selection_window:
            return  # Wenn das Fenster bereits geöffnet ist, tue nichts

        # Neues Fenster zur Auswahl von Emojis
        self.emoji_selection_window = tk.Toplevel(self.root)
        self.emoji_selection_window.title("Wähle ein Emoji")
        for i, emoji_code in enumerate(self.emoji_list):
            emoji_label = tk.Label(self.emoji_selection_window, text=emoji.emojize(emoji_code), font=("Arial", 40), padx=10, pady=10)
            emoji_label.grid(row=i // 3, column=i % 3)

            # Emoji beim Klicken hinzufügen
            emoji_label.bind("<Button-1>", lambda e, emoji_code=emoji_code: self.add_emoji(emoji_code))

    def add_emoji(self, emoji_code):
        # Funktion, um das ausgewählte Emoji zum Bild hinzuzufügen
        emoji_text = emoji.emojize(emoji_code)  # Emoji-Text
        self.current_text = self.canvas.create_text(self.x, self.y + 50, text=emoji_text, font=("Arial", 40), tags="editable")
        self.text_items.append(self.current_text)  # Speichern der Emoji-ID

    def add_border(self):
        # Funktion, um einen schwarzen Rahmen um das Bild hinzuzufügen
        if self.img:
            self.img = ImageOps.expand(self.img, border=10, fill="black")  # Bild um 10 Pixel erweitern
            self.display_image()

    def move_image(self):
        # Funktion, um das Bild zu verschieben
        if self.img:
            self.canvas.tag_bind("moveable_image", "<Button-1>", self.start_move)
            self.canvas.tag_bind("moveable_image", "<B1-Motion>", self.move)

    def start_move(self, event):
        # Funktion zum Starten der Bewegung (Berechnung der Verschiebung)
        self.offset_x = event.x - self.x
        self.offset_y = event.y - self.y

    def move(self, event):
        # Funktion zum Verschieben des Bildes
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        self.canvas.coords("moveable_image", new_x, new_y)  # Bild auf neuer Position setzen
        self.x, self.y = new_x, new_y  # Neue Koordinaten speichern

    def crop_image(self):
        # Funktion, um das Bild zuzuschneiden (Beispielwerte)
        if self.img:
            left = 100
            top = 100
            right = 500
            bottom = 400
            cropped_img = self.img.crop((left, top, right, bottom))  # Bild zuschneiden
            self.img = cropped_img  # Neues Bild setzen
            self.display_image()

    def rotate_image(self):
        # Funktion, um das Bild zu drehen (90 Grad)
        if self.img:
            self.img = self.img.rotate(90, expand=True)  # Bild um 90 Grad drehen
            self.display_image()

    def resize_image(self):
        # Funktion, um die Bildgröße anzupassen
        if self.img:
            resize_window = tk.Toplevel(self.root)  # Neues Fenster für die Größe
            resize_window.title("Bildgröße anpassen")
            width_label = tk.Label(resize_window, text="Breite:")
            width_label.pack()
            width_entry = tk.Entry(resize_window)
            width_entry.pack()
            height_label = tk.Label(resize_window, text="Höhe:")
            height_label.pack()
            height_entry = tk.Entry(resize_window)
            height_entry.pack()

            # Funktion, um die neue Größe anzuwenden
            def apply_resize():
                try:
                    width = int(width_entry.get())  # Neue Breite
                    height = int(height_entry.get())  # Neue Höhe
                    new_img = self.img.resize((width, height))  # Bildgröße ändern
                    self.img = new_img
                    self.display_image()  # Neues Bild anzeigen
                    resize_window.destroy()  # Fenster schließen
                except ValueError:
                    print("Ungültige Größe eingegeben")  # Fehlerbehandlung

            tk.Button(resize_window, text="Größe anpassen", command=apply_resize).pack()

    def save_image(self):
        # Speichern des bearbeiteten Bildes
        if self.img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                self.img.save(file_path)  # Bild speichern

    def undo(self):
        # Rückgängig-Funktion, um die letzte Aktion rückgängig zu machen
        pass
    
def start_meme_generator():
    start_window.destroy()
    root = tk.Tk()  # Erstelle das Tkinter-Hauptfenster
    app = MemeGenerator(root)  # Erstelle das Meme-Generator-Objekt
    root.mainloop()

btn_generator = tk.Button(start_window, text="Meme Generator", font=("Alasassy Caps", 12), command=start_meme_generator)
btn_generator.pack(pady=10)


start_window.mainloop()