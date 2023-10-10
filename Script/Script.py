import pymysql
import random
from faker import Faker

# Configuration de la connexion à la base de données
host = 'localhost'
user = 'root'
password = ''
database = 'mairiedouala3e_bd'

# Création d'une instance de Faker
fake = Faker()

def generate_douala_3e_coordinates():
    central_latitude = 4.0511
    central_longitude = 9.7085
    # Générer une petite variation pour les coordonnées
    delta_lat = random.uniform(-0.09, 0.09)  # variation de latitude
    delta_lon = random.uniform(-0.09, 0.09)  # variation de longitude
    return central_latitude + delta_lat, central_longitude + delta_lon

# Connexion à la base de données
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

# Dictionnaire des taxes et leurs montants respectifs
taxes_montants = {
    'Taxe hygiène et Salubrité': 45000.00,
    'Droits de fourrière': 15000.00,
    'Droits de place marchés': 10000.00,
    'Produits certificat urbanisme': 20000.00,
    'Produits du certificat de Lotis': 25000.00,
    'Produit permis de construire': 30000.00,
    'Droits occupation parkings': 1000.00,
    'Droits de stade': 5000.00,
    'Loyers immeubles': 60000.00,
    'Location salles de fêtes': 20000.00,
    'Amendes liées aux déchêts': 5000.00
}

# Récupérer les IDs des taxes à partir de leurs noms
taxe_ids = {}
for taxe, montant in taxes_montants.items():
    cursor.execute("SELECT ID_taxe FROM Taxes WHERE Nom_taxe = %s", (taxe,))
    taxe_id = cursor.fetchone()[0]
    taxe_ids[taxe] = taxe_id


noms_camerounais = ['Aboudi', 'Aboubakar', 'Acha', 'Adamou', 'Adjobi', 'Adolphe', 'Adrienne', 'Afi', 'Agnes', 'Ahmadou', 'Aicha', 'Aime', 'Aisha', 'Aissatou', 'Aja', 'Akono', 'Alain', 'Albate', 'Albine', 'Alphonse', 'Amadou', 'Aminata', 'Andre', 'Anicet', 'Annette', 'Antoine', 'Antonin', 'Arlette', 'Arnaud', 'Arsene', 'Asonganyi', 'Assoumou', 'Ateba', 'Augustin', 'Aurelien', 'Awa', 'Ayissi', 'Aziz', 'Babila', 'Badel', 'Bah', 'Bakary', 'Balla', 'Bapoupary', 'Barth', 'Basile', 'Bassong', 'Baya', 'Beatrice', 'Bello', 'Bengondo', 'Benjamin', 'Bernadette', 'Bernard', 'Berthe', 'Bienvenu', 'Biloa', 'Blaise', 'Bonaventure', 'Boris', 'Botoy', 'Brice', 'Bruno', 'Calvin', 'Carine', 'Cedric', 'Celestin', 'Celine', 'Charles', 'Charlotte', 'Christian', 'Christine', 'Claire', 'Clarisse', 'Claude', 'Clovis', 'Coco', 'Comba', 'Come', 'Cyprien', 'Cyrille', 'Dada', 'Dakole', 'Dange', 'Daniel', 'Danielle', 'David', 'Deborah', 'Dedou', 'Delphine', 'Denise', 'Desire', 'Djacbou', 'Dolvine', 'Donald', 'Dorette', 'Douala', 'Edith', 'Edouard', 'Efon', 'Ekani', 'Ekene', 'El Hadj', 'Eliane', 'Elisabeth', 'Elise', 'Elodie', 'Eloundou', 'Elvis', 'Emanuel', 'Emilia', 'Emilie', 'Emmanuel', 'Emmauelle', 'Enock', 'Enow', 'Eric', 'Ernest', 'Esperance', 'Esther', 'Etienne', 'Eugene', 'Eve', 'Evelyn', 'Ewang', 'Fabrice', 'Falone', 'Fankem', 'Faustin', 'Fende', 'Fernand', 'Fidele', 'Fideline', 'Flore', 'Florence', 'Florent', 'Fogue', 'Fomen', 'Fon', 'Fonkoua', 'Fosso', 'Fotso', 'France', 'Francine', 'Francis', 'Franck', 'Francois', 'Frank', 'Frida', 'Fuh', 'Gabriel', 'Gaetan', 'Gaelle', 'Georges', 'Gerard', 'Germaine', 'Ghislain', 'Gilbert', 'Gisele', 'Gloria', 'Godlove', 'Grace', 'Gregoire', 'Guy', 'Hamadou', 'Hawa', 'Helene', 'Henri', 'Henriette', 'Herbert', 'Herve', 'Honore', 'Hortense', 'Idriss', 'Irene', 'Irma', 'Isaac', 'Issa', 'Iyawa', 'Jacob', 'Jacques', 'Jean', 'Jeannette', 'Jeremie', 'Jerome', 'Joel', 'Johanna', 'John', 'Jolie', 'Jonathan', 'Jordan', 'Jose', 'Joseph', 'Josiane', 'Josue', 'Jude', 'Judith', 'Julien', 'Julienne', 'Juliette', 'Justin', 'Kadia', 'Kane', 'Karl', 'Kenza', 'Kevin', 'Kouam', 'Koumkoa', 'Kouomegni', 'Landry', 'Larissa', 'Laure', 'Laurence', 'Laurent', 'Lea', 'Leandre', 'Leopold', 'Leon', 'Leonard', 'Leonie', 'Leopoldine', 'Letitia', 'Limbing', 'Lionel', 'Loic', 'Lolo', 'Lontum', 'Louise', 'Luc', 'Lucas', 'Lucien', 'Lucie', 'Ludovic', 'Luis', 'Lydie', 'Mado', 'Magloire', 'Mahamat', 'Maite', 'Malcom', 'Mamadou', 'Mancel', 'Marcellin', 'Marcelle', 'Marco', 'Margaret', 'Margueritte', 'Mariam', 'Marie', 'Marielle', 'Mariette', 'Marlene', 'Marot', 'Martin', 'Mary', 'Mathy', 'Maud', 'Maurice', 'Max', 'Maxime', 'Mballa', 'Mbami', 'Mbanka', 'Mbango', 'Mbatchou', 'Mbede', 'Mbida', 'Mbinglo', 'Mbog', 'Mbom', 'Mbongo', 'Mbono', 'Mbotto', 'Mbula', 'Mengue', 'Merlin', 'Messi', 'Michel', 'Michelle', 'Mireille', 'Moise', 'Moki', 'Mone', 'Mongo', 'Monique', 'Mouafo', 'Moumi', 'Mounjim', 'Moustapha', 'Moussa', 'Moyo', 'Nadia', 'Nadine', 'Nadja', 'Narcisse', 'Nathalie', 'Natcho', 'Nde', 'Ndip', 'Ndjie', 'Ndjomo', 'Ndom', 'Ndoumbe', 'Ndoumbou', 'Ndzana', 'Ndzana', 'Ndzene', 'Ndzomo', 'Nedjo', 'Nelson', 'Neri', 'Nestor', 'Ngassa', 'Ngene', 'Ngenge', 'Ngo', 'Ngome', 'Ngono', 'Ngoungoure', 'Ngouopo', 'Nguini', 'Nguini', 'Nguiock', 'Ngula', 'Nguini', 'Nguissou', 'Nguivoum', 'Ngwala']
prenoms_camerounais = ['Aboubakar', 'Achille', 'Adèle', 'Adolphine', 'Adrienne', 'Afi', 'Agnès', 'Ahmadou', 'Aimé', 'Aïcha', 'Aïssatou', 'Aja', 'Alain', 'Albate', 'Alphonse', 'Amadou', 'Aminata', 'André', 'Anicet', 'Annette', 'Antoine', 'Antonin', 'Arlette', 'Armand', 'Armelle', 'Arsène', 'Assoumou', 'Augustin', 'Aurélien', 'Awa', 'Ayissi', 'Aziz', 'Babila', 'Bah', 'Bakary', 'Balla', 'Barthélémy', 'Basile', 'Baya', 'Béatrice', 'Bella', 'Bello', 'Benjamin', 'Bernadette', 'Bernard', 'Berthe', 'Bienvenu', 'Blaise', 'Bonaventure', 'Boris', 'Brice', 'Bruno', 'Calvin', 'Carine', 'Cédric', 'Célestin', 'Céline', 'Charles', 'Charlotte', 'Christian', 'Christine', 'Claire', 'Clarisse', 'Claude', 'Clémence', 'Clotaire', 'Coco', 'Cyprien', 'Cyrille', 'Dada', 'Daniel', 'Danielle', 'David', 'Déborah', 'Delphine', 'Denise', 'Désiré', 'Diane', 'Didier', 'Dieudonné', 'Dina', 'Djibril', 'Dolvine', 'Donald', 'Dorothée', 'Douala', 'Ebenezer', 'Edgard', 'Edith', 'Edouard', 'Efon', 'El Hadj', 'Éliane', 'Élisabeth', 'Élise', 'Élodie', 'Elvis', 'Émanuel', 'Émile', 'Émilia', 'Émilie', 'Emma', 'Emmanuel', 'Emmauelle', 'Éric', 'Ernest', 'Esperance', 'Estelle', 'Esther', 'Étienne', 'Eugène', 'Ève', 'Evelyne', 'Fabrice', 'Faustin', 'Félicien', 'Félicité', 'Fernand', 'Fidèle', 'Florence', 'Florent', 'Francine', 'Francis', 'Franck', 'François', 'Frida', 'Fulbert', 'Gabin', 'Gabriel', 'Gaël', 'Gaëlle', 'Gaëtan', 'Gauthier', 'Gérald', 'Gérard', 'Germaine', 'Ghislain', 'Gilbert', 'Gisèle', 'Gloria', 'Grace', 'Grégoire', 'Guy', 'Hamadou', 'Hawa', 'Hélène', 'Henri', 'Henriette', 'Hermine', 'Hervé', 'Honoré', 'Hortense', 'Hubert', 'Idriss', 'Igor', 'Irène', 'Irma', 'Isaac', 'Issa', 'Iyawa', 'Jacques', 'Jean', 'Jeannette', 'Jérémie', 'Jérôme', 'Joël', 'Johanna', 'John', 'Jonathan', 'Jordan', 'Joseph', 'Josué', 'Jules', 'Julien', 'Juliette', 'Justin', 'Karl', 'Kenza', 'Kevin', 'Kouadio', 'Kouamé', 'Koumba', 'Landry', 'Laure', 'Laurence', 'Laurent', 'Léa', 'Léandre', 'Léonie', 'Léticia', 'Lionel', 'Loïc', 'Lolo', 'Louise', 'Lucas', 'Lucien', 'Lucie', 'Ludovic', 'Luis', 'Lydie', 'Magloire', 'Mahamat', 'Maïté', 'Malcom', 'Mamadou', 'Marcellin', 'Marcelle', 'Margaux', 'Margot', 'Mariam', 'Marie', 'Marielle', 'Mariette', 'Marlène', 'Martin', 'Maryse', 'Mathieu', 'Maud', 'Maurice', 'Maxime', 'Médard', 'Mélanie', 'Michel', 'Michelle', 'Mireille', 'Modeste', 'Mohamed', 'Monique', 'Moussa', 'Moumi', 'Mourad', 'Nadia', 'Nadège', 'Nadine', 'Narcisse', 'Nassim', 'Nathalie', 'Nathanaël', 'Ndiaw', 'Nestor', 'Ngouda', 'Nicolas', 'Nicole', 'Noé', 'Noël', 'Olivia', 'Omar', 'Ousmane', 'Pascale', 'Patrice', 'Patrick', 'Paul', 'Pauline', 'Paulette', 'Philippe', 'Pierre', 'Prudence', 'Rachel', 'Raphaël', 'Raoul', 'Raymond', 'Rebecca', 'René', 'Richard', 'Robert', 'Roger', 'Roland', 'Romain', 'Rosa', 'Rosalie', 'Rose', 'Ruben', 'Safi', 'Salomon', 'Samuel', 'Sandra', 'Sarah', 'Sébastien', 'Simon', 'Sofia', 'Sophie', 'Stéphane', 'Steve', 'Suzanne', 'Sylvain', 'Sylvie', 'Théophile', 'Thérèse', 'Thierry', 'Thomas', 'Timothée', 'Tita', 'Ulrich', 'Urbain', 'Valentin', 'Valérie', 'Vanessa', 'Victor', 'Vincent', 'Vivien', 'Wenceslas', 'Willy', 'Yann', 'Yannick', 'Yasmine', 'Yves', 'Zacharie']
domaines_email = ['gmail.com', 'yahoo.com', 'outlook.com']

# Génération et insertion d'usagers fictifs
usagers_ids = []
for _ in range(10):
    nom = random.choice(noms_camerounais)
    prenom = random.choice(prenoms_camerounais)
    latitude, longitude = generate_douala_3e_coordinates()
    adresse = f"{latitude}, {longitude}, Douala 3e"  # Vous pouvez formater ceci comme vous le souhaitez
    numero_telephone = f"+237 6{random.randint(10000000, 99999999)}"
    email = fake.email(domain=random.choice(domaines_email))
    
    sql = "INSERT INTO Usagers (Nom, Prenom, Adresse, Numero_telephone, Email) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (nom, prenom, adresse, numero_telephone, email))
    usagers_ids.append(cursor.lastrowid)

# Génération et insertion de localisations fictives
for uid in usagers_ids:
    latitude = 4.0 + random.random() * 0.1
    longitude = 9.7 + random.random() * 0.1
    description = random.choice(['Maison', 'Boutique', 'Comptoir', 'marche',])
    
    sql = "INSERT INTO Localisation (ID_usager, Latitude, Longitude, Description) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (uid, latitude, longitude, description))

# Génération et insertion de paiements fictifs
modes_paiement = ['Mobile money', 'Virement', 'Espèces']
for uid in usagers_ids:
    taxe_nom = random.choice(list(taxes_montants.keys()))
    taxe_id = taxe_ids[taxe_nom]
    montant_paye = taxes_montants[taxe_nom]
    mode = random.choice(modes_paiement)
    date_paiement = fake.date_this_year()
    
    sql = "INSERT INTO Paiements (ID_usager, ID_taxe, Date_paiement, Montant_paye, Mode_paiement) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (uid, taxe_id, date_paiement, montant_paye, mode))

# Génération et insertion de défauts de paiement fictifs
defauts_ids = []
for uid in random.sample(usagers_ids, 5):  # Seulement certains usagers auront des défauts de paiement
    taxe_nom = random.choice(list(taxes_montants.keys()))
    taxe_id = taxe_ids[taxe_nom]
    date_defaut = fake.date_this_year()
    
    sql = "INSERT INTO Defauts_de_paiement (ID_usager, ID_taxe, Date_defaut) VALUES (%s, %s, %s)"
    cursor.execute(sql, (uid, taxe_id, date_defaut))
    defauts_ids.append(cursor.lastrowid)

# Génération et insertion de recouvrements fictifs
for did in defauts_ids:
    date_recouvrement = fake.date_this_year()
    montant_recouvert = taxes_montants[random.choice(list(taxes_montants.keys()))]
    
    sql = "INSERT INTO Recouvrements (ID_defaut, Date_recouvrement, Montant_recouvert) VALUES (%s, %s, %s)"
    cursor.execute(sql, (did, date_recouvrement, montant_recouvert))

# Génération et insertion de campagnes de recouvrement fictives
for _ in range(3):  # Création de 3 campagnes fictives
    date_debut = fake.date_this_year(before_today=True, after_today=False)
    date_fin = fake.date_between_dates(date_start=date_debut)  # Assurer que la date de fin est après la date de début
    mois_debut = date_debut.strftime('%B')  # Obtenir le nom du mois à partir de la date de début
    annee_debut = date_debut.strftime('%Y')  # Obtenir l'année de la date de début
    description = f"Campagne {mois_debut} {annee_debut}"
    
    sql = "INSERT INTO Campagnes_de_recouvrement (Date_debut, Date_fin, Description) VALUES (%s, %s, %s)"
    cursor.execute(sql, (date_debut, date_fin, description))

# Valider les changements et fermer la connexion
connection.commit()
cursor.close()
connection.close()
