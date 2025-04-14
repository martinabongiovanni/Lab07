import flet as ft

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        mese = self._mese
        if not mese:
            self._view.create_alert("Attenzione! Selezionare un mese.")
            return

        lista_ricerca = self._model.get_umidita_media_dal_DAO(mese)
        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è:", italic=True))
        for i in lista_ricerca:
            self._view.lst_result.controls.append(ft.Text(f"{i[0]}: {i[1]}"))
        self._view.lst_result.controls.append(ft.Divider(thickness=2, color="black"))
        self._view.update_page()

    def handle_sequenza(self, e):
        mese = self._mese
        if not mese:
            self._view.create_alert("Attenzione! Selezionare un mese.")
            return
        risultati = self._model.calcola_sequenza(mese)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo: {risultati[1]}", italic=True))
        for situazione in risultati[0]:
            self._view.lst_result.controls.append(ft.Text(f"{situazione.__str__()}"))
        self._view.lst_result.controls.append(ft.Divider(thickness=2, color="black"))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)