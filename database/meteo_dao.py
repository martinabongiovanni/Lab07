from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_umidita_media(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                    SELECT s.Localita , SUM(s.Umidita)/COUNT(*) as umidita_media
                    FROM situazione s 
                    WHERE MONTH (s.`Data`) = %s
                    GROUP BY s.Localita
            """
            cursor.execute(query, (mese, ))
            for row in cursor:
                result.append((row["Localita"], row["umidita_media"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_situazioni_meta_mese(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                        SELECT s.Localita, s.Umidita, s.Data
                        FROM situazione s 
                        WHERE MONTH (s.Data) = %s and DAY (s.Data) < 16
                        ORDER BY s.Data ASC
                    """
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"], row["Data"], row["Umidita"]))
            cursor.close()
            cnx.close()
        return result