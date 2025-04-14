import copy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._meteo_dao = MeteoDao()

        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []


    def get_umidita_media_dal_DAO(self, mese):
        return self._meteo_dao.get_umidita_media(mese)




    def calcola_sequenza(self, mese):
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []
        situazioni = MeteoDao().get_situazioni_meta_mese(mese)
        self._ricorsione([], situazioni)
        return self.soluzione_ottima, self.costo_ottimo

    def torva_possibili_step(self, parziale, lista_situazioni):
        giorno = len(parziale)+1
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati

    def is_admissible(self, candidate, parziale): # qui definisco i miei vincoli
        # vincolo su 6 giorni
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidate.localita:
                counter += 1
        if counter >= 6:
            return False
        # vincolo su permanenza
        # 1) lunghezza di parziale minore di 3
        if len(parziale) == 0:
            return True
        if len(parziale) < 3:
            if candidate.localita != parziale[0].localita:
                return False
        # 2) le ultime tre situazioni precedenti non sono tutte uguali
        else:
            if (parziale[-1].localita != parziale[-2].localita
                    or parziale[-1].localita != parziale[-3].localita
                    or parziale[-3].localita != parziale[-2].localita):
                if parziale[-1].localita != candidate.localita:
                    return False
        # altrimenti ok
        return True

    def _calcola_costo(self, parziale):
        costo = 0
        # per ogni giorno ho un costo pari all'umidità
        for situazione in parziale:
            costo += situazione.umidita

        # se cambio città ho un costo aggiuntivo di 100 per i due giorni successivi
        for i in range(len(parziale)):
            if (i >= 2 and
                    (parziale[i-1].localita != parziale[i].localita or
                     parziale[i-2].localita != parziale[i].localita)):
                costo += 100
        return costo

    def _ricorsione(self, parziale, lista_situazioni):
        # condizione terminale
        if len(parziale) == 15:
            # print(parziale)
            self.n_soluzioni += 1
            costo = self._calcola_costo(parziale)
            if self.costo_ottimo == -1 or self.costo_ottimo > costo:
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)

        # condizione ricorsiva
        else:
            # cerco le città per il giorno che mi serve
            candidates = self.torva_possibili_step(parziale, lista_situazioni)
            # provo ad aggiungere una di queste città e vado avanti
            for candidate in candidates:
                # verifico vincoli
                if self.is_admissible(candidate, parziale):
                    parziale.append(candidate)
                    self._ricorsione(parziale, lista_situazioni)
                    parziale.pop()

if __name__ == '__main__':
    my_model = Model()
    print(my_model.calcola_sequenza(2))
    print(my_model.n_soluzioni)




