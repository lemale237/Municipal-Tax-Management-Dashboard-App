from flask import Flask
from flask_restful import Resource, Api
import mysql.connector
import decimal
import datetime
import json

app = Flask(__name__)
api = Api(app)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mairiedouala3e_bd"
    )
def complex_serializer(o):
    if isinstance(o, decimal.Decimal):
        return float(o)
    elif isinstance(o, datetime.date):
        return o.isoformat()
    raise TypeError(repr(o) + " n'est pas sérialisable en JSON")

# Taxes payees 
class TaxesPayees(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Paiements WHERE defaut_paiement = FALSE")
        taxes_payees = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return json.loads(json.dumps(taxes_payees, default=complex_serializer))
    
# Historique des paiements
class HistoriquePaiements(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT DATE(p.date_paiement) as date, SUM(p.montant_paye) as montant_total, u.nom, u.prenom
        FROM Paiements p
        INNER JOIN Usagers u ON p.id_usager = u.id_usager
        GROUP BY DATE(p.date_paiement), u.nom, u.prenom
        ORDER BY DATE(p.date_paiement)
        """
        cursor.execute(query)
        historique = cursor.fetchall()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(historique, default=complex_serializer))

# Défauts de paiement par mois
class DefautsPaiement(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT MONTH(date_limite) as mois, YEAR(date_limite) as annee, COUNT(*) as nombre_defauts
        FROM Paiements
        WHERE defaut_paiement = TRUE
        GROUP BY MONTH(date_limite), YEAR(date_limite)
        ORDER BY YEAR(date_limite), MONTH(date_limite)
        """
        cursor.execute(query)
        defauts = cursor.fetchall()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(defauts, default=complex_serializer))

# Taux de paiement par type de taxe
class TauxPaiementTaxe(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT nom_taxe as taxe, COUNT(*) as nombre_paiements
        FROM Paiements
        JOIN Taxes ON Paiements.id_taxe = Taxes.id_taxe
        WHERE Paiements.defaut_paiement = FALSE
        GROUP BY nom_taxe
        """
        cursor.execute(query)
        taux = cursor.fetchall()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(taux, default=complex_serializer))


# Efficacité des campagnes de recouvrement
class EfficaciteCampagnes(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT 
            Campagnes.nom_campagne, 
            Campagnes.date_debut, 
            Campagnes.date_fin, 
            SUM(Recouvrements.montant_recouvre) as montant_recupere
        FROM Recouvrements
        JOIN Campagnes ON Recouvrements.id_campagne = Campagnes.id_campagne
        GROUP BY Campagnes.id_campagne
        """
        cursor.execute(query)
        efficacite = cursor.fetchall()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(efficacite, default=complex_serializer))

# Répartition des modes de paiement
class RepartitionModesPaiement(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT mode_paiement, COUNT(*) as nombre_paiements
        FROM Paiements
        GROUP BY mode_paiement
        """
        cursor.execute(query)
        repartition = cursor.fetchall()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(repartition, default=complex_serializer))

# Montants impayés par usager
class MontantsImpayes(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT 
            CONCAT(Usagers.nom, ' ', Usagers.prenom) AS nom_complet_usager,
            SUM(Taxes.montant_fixe) - SUM(Paiements.montant_paye) as montant_impaye
        FROM Paiements
        JOIN Usagers ON Paiements.id_usager = Usagers.id_usager
        JOIN Taxes ON Paiements.id_taxe = Taxes.id_taxe
        WHERE Paiements.defaut_paiement = TRUE
        GROUP BY Usagers.id_usager
        """
        cursor.execute(query)
        montants_impayes = cursor.fetchall()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(montants_impayes, default=complex_serializer))

# Tendance des paiements et des recouvrements
class TendancePaiementsRecouvrements(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Montants des paiements par date
        query_paiements = """
        SELECT date_paiement, SUM(montant_paye) as montant_paiement
        FROM Paiements
        GROUP BY date_paiement
        """
        cursor.execute(query_paiements)
        paiements = cursor.fetchall()
        
        # Montants des recouvrements par date
        query_recouvrements = """
        SELECT date_recouvrement, SUM(montant_recouvre) as montant_recouvre
        FROM Recouvrements
        GROUP BY date_recouvrement
        """
        cursor.execute(query_recouvrements)
        recouvrements = cursor.fetchall()
        
        cursor.close()
        conn.close()

        # Fusion des deux listes en une seule basée sur les dates
        tendance = {}
        for p in paiements:
            date_p = p['date_paiement'].isoformat()
            if date_p not in tendance:
                tendance[date_p] = {'montant_paiement': 0, 'montant_recouvre': 0}
            tendance[date_p]['montant_paiement'] = p['montant_paiement']
        
        for r in recouvrements:
            date_r = r['date_recouvrement'].isoformat()
            if date_r not in tendance:
                tendance[date_r] = {'montant_paiement': 0, 'montant_recouvre': 0}
            tendance[date_r]['montant_recouvre'] = r['montant_recouvre']

        return json.loads(json.dumps(list(tendance.items()), default=complex_serializer))

# Localisation des défauts de paiement
# class LocalisationDefautsPaiement(Resource):
#     def get(self):
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         query = """
#         SELECT Usagers.nom, Usagers.prenom, Usagers.adresse
#         FROM Paiements
#         JOIN Usagers ON Paiements.id_usager = Usagers.id_usager
#         WHERE Paiements.defaut_paiement = TRUE
#         GROUP BY Usagers.id_usager
#         """
#         cursor.execute(query)
#         localisation_defauts = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return json.loads(json.dumps(localisation_defauts, default=complex_serializer))


# Localisation des défauts de paiement
class LocalisationDefautsPaiement(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT Usagers.nom, Usagers.prenom, Localisation.latitude, Localisation.longitude
        FROM Paiements
        JOIN Usagers ON Paiements.id_usager = Usagers.id_usager
        JOIN Localisation ON Usagers.id_usager = Localisation.id_usager
        WHERE Paiements.defaut_paiement = TRUE
        GROUP BY Usagers.id_usager
        """
        cursor.execute(query)
        localisation_defauts = cursor.fetchall()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(localisation_defauts, default=complex_serializer))


# Nombre total de taxes payées
class TotalTaxesPayees(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT COUNT(*) as total_taxes_payees
        FROM Paiements
        WHERE defaut_paiement = FALSE
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(result, default=complex_serializer))

# Nombre total de taxes non payées
class TotalTaxesNonPayees(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT COUNT(*) as total_taxes_non_payees
        FROM Paiements
        WHERE defaut_paiement = TRUE
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(result, default=complex_serializer))

# Montant total des taxes payées
class MontantTotalTaxesPayees(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT SUM(montant_paye) as montant_total_paye
        FROM Paiements
        WHERE defaut_paiement = FALSE
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(result, default=complex_serializer))

# Montant total des taxes non payées
class MontantTotalTaxesNonPayees(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT SUM(Paiements.montant_paye) as montant_total_non_paye
        FROM Paiements
        WHERE Paiements.defaut_paiement = 1

        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return json.loads(json.dumps(result, default=complex_serializer))



# Ajout des routes à l'API
api.add_resource(TaxesPayees, '/taxes_payees')
api.add_resource(HistoriquePaiements, '/historique_paiements')
api.add_resource(DefautsPaiement, '/defauts_paiement')
api.add_resource(TauxPaiementTaxe, '/taux_paiement_taxe')    
api.add_resource(EfficaciteCampagnes, '/efficacite_campagnes')
api.add_resource(RepartitionModesPaiement, '/repartition_modes_paiement')
api.add_resource(MontantsImpayes, '/montants_impayes')
api.add_resource(TendancePaiementsRecouvrements, '/tendance_paiements_recouvrements')
api.add_resource(LocalisationDefautsPaiement, '/localisation_defauts_paiement')
api.add_resource(TotalTaxesPayees, '/total_taxes_payees')
api.add_resource(TotalTaxesNonPayees, '/total_taxes_non_payees')
api.add_resource(MontantTotalTaxesPayees, '/montant_total_taxes_payees')
api.add_resource(MontantTotalTaxesNonPayees, '/montant_total_taxes_non_payees')



if __name__ == "__main__":
    app.run(debug=True)