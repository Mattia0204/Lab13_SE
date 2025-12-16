from database.DB_connect import DBConnect
from model.gene import Gene
from model.classificazione import Classificazione
from model.interazione import Interazione


class DAO:

    @staticmethod
    def get_gene() -> dict[str, Gene] | None:

        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM gene"
        try:
            cursor.execute(query)
            for row in cursor:
                gene = Gene(
                    id=row["id"],
                    funzione=row["funzione"],
                    essenziale=row["essenziale"],
                    cromosoma=row["cromosoma"],
                )
                result[gene.id] = gene
        except Exception as e:
            print(f"Errore durante la query get_gene: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_classificazione() -> dict[str, Classificazione] | None:

        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM classificazione"
        try:
            cursor.execute(query)
            for row in cursor:
                classificazione = Classificazione(
                    id_gene=row["id_gene"],
                    localizzazione=row["localizzazione"],
                )
                result[classificazione.id_gene] = classificazione
        except Exception as e:
            print(f"Errore durante la query get_classificazione: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_interazione() -> dict[str, Interazione] | None:

        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM interazione"
        try:
            cursor.execute(query)
            for row in cursor:
                interazione = Interazione(
                    id_gene1=row["id_gene1"],
                    id_gene2=row["id_gene2"],
                    tipo=row["tipo"],
                    correlazione=row["correlazione"],
                )
                result[(interazione.id_gene1, interazione.id_gene2)] = interazione
        except Exception as e:
            print(f"Errore durante la query get_interazione: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
