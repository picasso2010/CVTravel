import json
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock

class SepsiszentgyorgyTravelApp(App):
    def build(self):
        self.title = "CVTravel - Menetrend"
        
        # Adatok betöltése a helyi (vagy frissített) JSON-ból
        self.data = self.load_data()
        self.stations = self.extract_stations()
        self.destinations = self.extract_destinations()

        root = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Cím
        root.add_widget(Label(text="Sepsiszentgyörgy Menetrend", font_size=22, size_hint_y=None, height=40))

        # 1. Honnan (Megálló választó Spinner / Legördülő)
        root.add_widget(Label(text="Honnan indulnál?", font_size=14, size_hint_y=None, height=25))
        self.spinner_from = Spinner(
            text='Válassz megállót...',
            values=self.stations,
            size_hint_y=None,
            height=45
        )
        root.add_widget(self.spinner_from)

        # 2. Hova (Célállomás választó Spinner)
        root.add_widget(Label(text="Hová szeretnél utazni?", font_size=14, size_hint_y=None, height=25))
        self.spinner_to = Spinner(
            text='Válassz útirányt...',
            values=self.destinations,
            size_hint_y=None,
            height=45
        )
        root.add_widget(self.spinner_to)

        # Keresés gomb
        btn_search = Button(text="Következő járatok keresése", background_color=(0.1, 0.6, 0.2, 1), size_hint_y=None, height=50)
        btn_search.bind(on_press=self.search_rides)
        root.add_widget(btn_search)

        # 3. Eredmények megjelenítése (Görgethető lista)
        root.add_widget(Label(text="Találatok:", font_size=14, size_hint_y=None, height=25))
        
        self.result_label = Label(text="Még nincs keresés indítva.", font_size=14, valign='top', halign='left')
        self.result_label.bind(size=self.result_label.setter('text_size'))
        
        root.add_widget(self.result_label)

        return root

    def load_data(self):
        try:
            with open("multitrans_tiszta.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return []

    def extract_stations(self):
        stations = set()
        for station in self.data:
            if "hu" in station:
                stations.add(station["hu"])
        return sorted(list(stations))

    def extract_destinations(self):
        destinations = set()
        for station in self.data:
            for line in station.get("lines", []):
                if "dest" in line:
                    destinations.add(line["dest"])
        return sorted(list(destinations))

    def search_rides(self, instance):
        from_station = self.spinner_from.text
        to_destination = self.spinner_to.text

        if from_station == 'Válassz megállót...' or to_destination == 'Válassz útirányt...':
            self.result_label.text = "Kérlek add meg a kiinduló és célállomást is!"
            return

        now = datetime.now()
        current_time_str = now.strftime("%H:%M")
        is_weekend = now.weekday() >= 5

        found_results = []

        for station in self.data:
            if station.get("hu", "").lower() == from_station.lower():
                for line in station.get("lines", []):
                    if to_destination.lower() in line.get("dest", "").lower():
                        vonal_szam = line.get("num")
                        cel_allomas = line.get("dest")
                        
                        for orare in line.get("orare", []):
                            title = orare.get("title", "").lower()
                            if is_weekend and ("szombat" not in title and "sâmbătă" not in title):
                                continue
                            if not is_weekend and ("munkanapok" not in title and "zile lucrătoare" not in title):
                                continue

                            for row in orare.get("rows", []):
                                ora = row.get("h")
                                for perc in row.get("m"):
                                    jarat_idopont = f"{ora}:{perc}"
                                    if jarat_idopont > current_time_str:
                                        found_results.append(f"Vonal {vonal_szam} -> Indul: {jarat_idopont}")

        if found_results:
            # Csak az első 10 legközelebbi járatot mutatjuk, hogy ne lógjon ki a képernyőről
            self.result_label.text = "\n".join(found_results[:10])
        else:
            self.result_label.text = "A megadott útvonalra mára már nincs közvetlen járat."

if __name__ == '__main__':
    SepsiszentgyorgyTravelApp().run()