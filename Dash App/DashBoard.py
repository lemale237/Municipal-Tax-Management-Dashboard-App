import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import requests
import plotly.graph_objs as go
from dash import dash_table
import plotly.express as px




# Initialisez l'application avec Bootstrap DARK THEME
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, FA])
server = app.server

# Fonction pour générer une carte pour une statistique
def generate_card(content, title, color="primary"):
    card_content = [
        html.H4(content, className=f"text-{color} card-title"),
        html.P(title, className="card-text")
    ]
    return dbc.Card(dbc.CardBody(card_content, className="text-center"), className="mb-3 shadow-lg p-3 mb-5 bg-dark rounded")

def fetch_data_from_api(endpoint):
    try:
        response = requests.get(f'http://localhost:5000/{endpoint}')
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error fetching data from {endpoint}. Status code: {response.status_code}")
    except Exception as e:
        print(e)
        return []

# Cartes initiales (les valeurs seront remplies par le rappel)
montant_paye_card = generate_card("0 FCFA", "Montant total des taxes payées", color="success")
nombre_paye_card = generate_card("0", "Nombre total de taxes payées", color="warning")
montant_non_paye_card = generate_card("0 FCFA", "Montant total des taxes non payées", color="danger")
nombre_non_paye_card = generate_card("0", "Nombre total de taxes non payées", color="info")

# Mettre les cartes dans une ligne
cards_row = dbc.Row([
    dbc.Col(id='montant-paye-card', children=montant_paye_card, md=3),
    dbc.Col(id='nombre-paye-card', children=nombre_paye_card, md=3),
    dbc.Col(id='montant-non-paye-card', children=montant_non_paye_card, md=3),
    dbc.Col(id='nombre-non-paye-card', children=nombre_non_paye_card, md=3)
], className="mb-4")

# Descriptions pour les graphiques
desc_paiement = html.P("Répartition des modes de paiement", style={"textAlign": "center", "color": "white"})
desc_defauts = html.P("Défauts de paiement par mois", style={"textAlign": "center", "color": "white"})

graphs_row_2 = dbc.Row([
    dbc.Col([desc_paiement, dbc.Card(dcc.Graph(id='modes-paiement-graph'), className="shadow-lg p-3 mb-5 bg-dark rounded")], md=6),
    dbc.Col([desc_defauts, dbc.Card(dcc.Graph(id='defauts-paiement-graph'), className="shadow-lg p-3 mb-5 bg-dark rounded")], md=6)
], className="mb-4")

# Mise à jour des graphiques en temps réel
@app.callback(
    [Output('modes-paiement-graph', 'figure'),
     Output('defauts-paiement-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    # Graphique circulaire des modes de paiement
    modes_data = fetch_data_from_api("repartition_modes_paiement")
    labels = [entry['mode_paiement'] for entry in modes_data]
    values = [entry['nombre_paiements'] for entry in modes_data]
    paiement_figure = {
        'data': [go.Pie(labels=labels, values=values)],
        'layout': {
            'title': 'Modes de paiement',
            'hovermode': 'closest'
        }
    }
    
    # Graphique des défauts de paiement par mois
    defauts_data = fetch_data_from_api("defauts_paiement")
    labels = [f"{entry['mois']} - {entry['annee']}" for entry in defauts_data]
    values = [entry['nombre_defauts'] for entry in defauts_data]
    defauts_figure = {
        'data': [go.Bar(x=labels, y=values)],
        'layout': {
            'title': 'Défauts de paiement par mois',
            'xaxis': {'title': 'Mois'},
            'yaxis': {'title': 'Nombre de défauts'},
            'hovermode': 'closest'
        }
    }

    return paiement_figure, defauts_figure

# Mise à jour des cartes en temps réel
def format_amount(amount):
    return '{:,.2f}'.format(amount).replace(", ", " ").replace(".",",") + " FCFA"

@app.callback(
    [Output('montant-paye-card', 'children'),
     Output('nombre-paye-card', 'children'),
     Output('montant-non-paye-card', 'children'),
     Output('nombre-non-paye-card', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_cards(n):
    montant_paye = fetch_data_from_api("montant_total_taxes_payees")["montant_total_paye"]
    nombre_paye = fetch_data_from_api("total_taxes_payees")["total_taxes_payees"]
    montant_non_paye = fetch_data_from_api("montant_total_taxes_non_payees")["montant_total_non_paye"]
    nombre_non_paye = fetch_data_from_api("total_taxes_non_payees")["total_taxes_non_payees"]

    montant_paye_card = generate_card(format_amount(montant_paye), "Montant total des taxes payées", color="success")
    nombre_paye_card = generate_card(nombre_paye, "Nombre total de taxes payées", color="warning")
    montant_non_paye_card = generate_card(format_amount(montant_non_paye), "Montant total des taxes non payées", color="danger")
    nombre_non_paye_card = generate_card(nombre_non_paye, "Nombre total de taxes non payées", color="info")
    
    print (montant_paye_card)
    return montant_paye_card, nombre_paye_card, montant_non_paye_card, nombre_non_paye_card
   


def fetch_taux_paiement_taxe_data():
    return fetch_data_from_api("taux_paiement_taxe")

def fetch_efficacite_campagnes_data():
    return fetch_data_from_api("efficacite_campagnes")

# Descriptions pour les nouveaux graphiques
desc_taux_taxe = html.P("Taux de paiement par type de taxe", style={"textAlign": "center", "color": "white"})
desc_efficacite = html.P("Efficacité des campagnes de recouvrement", style={"textAlign": "center", "color": "white"})

graphs_row_3 = dbc.Row([
    dbc.Col([desc_taux_taxe, dbc.Card(dcc.Graph(id='taux-paiement-taxe-graph'), className="shadow-lg p-3 mb-5 bg-dark rounded")], md=6),
    dbc.Col([desc_efficacite, dbc.Card(dcc.Graph(id='efficacite-campagnes-graph'), className="shadow-lg p-3 mb-5 bg-dark rounded")], md=6)
], className="mb-4")

@app.callback(
    [Output('taux-paiement-taxe-graph', 'figure'),
     Output('efficacite-campagnes-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_new_graphs(n):
    # Graphique du taux de paiement par type de taxe
    taux_data = fetch_taux_paiement_taxe_data()

    # Vérification des clés nécessaires
    if taux_data and all(key in taux_data[0] for key in ['taxe', 'nombre_paiements']):
        taxe_labels = [entry['taxe'] for entry in taux_data]
        taxe_values = [entry['nombre_paiements'] for entry in taux_data]
    else:
        taxe_labels = []
        taxe_values = []

    taux_taxe_figure = {
    'data': [go.Bar(
        x=taxe_labels,
        y=taxe_values,
        marker_color='rgb(51, 51, 204)',
        text=taxe_labels,  # Ajoutez cette ligne
        textposition='inside',  # Et cette ligne
        insidetextanchor='start',  # Pour aligner le texte au début (gauche) de la barre
        orientation='v'  # Ceci assure que les barres sont verticales
    )],
    'layout': {
        'title': 'Taux de paiement par type de taxe',
        'xaxis': {'title': 'Type de taxe', 'tickangle': -90, 'showticklabels': False},  # Cacher les étiquettes des axes x car elles sont maintenant à l'intérieur des barres
        'yaxis': {'title': 'Nombre de paiements'},
        'hovermode': 'closest'
    }
}
    
    # Graphique de l'efficacité des campagnes de recouvrement
    efficacite_data = fetch_efficacite_campagnes_data()
    
    # Graphique de l'efficacité des campagnes de recouvrement en tant que graphique à barres
    efficacite_data = fetch_efficacite_campagnes_data()
    efficacite_dates = [entry['date_debut'] for entry in efficacite_data]
    montants_recuperes = [entry['montant_recupere'] for entry in efficacite_data]
    
    efficacite_figure = {
        'data': [go.Bar(x=efficacite_dates, y=montants_recuperes)],
        'layout': {
            'title': 'Efficacité des campagnes de recouvrement (Graphique à barres)',
            'xaxis': {'title': 'Date de la campagne'},
            'yaxis': {'title': 'Montant récupéré'},
            'hovermode': 'closest'
        }
    }

    return taux_taxe_figure, efficacite_figure



# Descriptions pour les nouveaux graphiques
desc_tendance = html.P("Tendance des paiements et des recouvrements", style={"textAlign": "center", "color": "white"})
desc_historique = html.P("Historique des paiements", style={"textAlign": "center", "color": "white"})

graphs_row_4 = dbc.Row([
    dbc.Col([desc_tendance, dbc.Card(dcc.Graph(id='tendance-graph'), className="shadow-lg p-3 mb-5 bg-dark rounded")], md=6),
    dbc.Col([desc_historique, dbc.Card(dash_table.DataTable(
        id='historique-table',
        columns=[
            {'name': 'Nom', 'id': 'nom'},
            {'name': 'Prénom', 'id': 'prenom'},
            {'name': 'Montant total', 'id': 'montant_total'},
            {'name': 'Date', 'id': 'date'}
        ],
        page_size=10,  # Afficher 10 lignes par page
        style_table={'overflowX': 'auto'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'fontWeight': 'bold'
        }
    ), className="shadow-lg p-3 mb-5 bg-dark rounded")], md=6)
], className="mb-4")



@app.callback(
    [Output('tendance-graph', 'figure'),
     Output('historique-table', 'data')],
    [Input('interval-component', 'n_intervals')]
)
def update_tendance_historique(n):
    # Graphique de tendance des paiements et recouvrements
    tendance_data = fetch_data_from_api("tendance_paiements_recouvrements")
    dates = [entry[0] for entry in tendance_data]
    paiements = [entry[1]['montant_paiement'] for entry in tendance_data]
    recouvrements = [entry[1]['montant_recouvre'] for entry in tendance_data]

    tendance_figure = {
        'data': [
            go.Bar(x=dates, y=paiements, name='Paiements', marker=dict(color='blue')),
            go.Bar(x=dates, y=recouvrements, name='Recouvrements', marker=dict(color='red'))
        ],
        'layout': {
            'title': 'Tendance des paiements et recouvrements',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Montant'},
            'hovermode': 'closest',
            'barmode': 'group'
        }
    }

    # Données pour le tableau historique des paiements
    historique_data = fetch_data_from_api("historique_paiements")

    return tendance_figure, historique_data




# Configuration de la clé MapBox
px.set_mapbox_access_token("pk.eyJ1IjoibGVtYWxlMjM3IiwiYSI6ImNsbGp6dDdheTJpM2kza24xbmVyejdrZXEifQ.JgpmmsRpwibEZN1D7-r4Pg")

def fetch_localisation_defauts_paiement_data():
    return fetch_data_from_api("localisation_defauts_paiement")

@app.callback(
    Output('localisation-defauts-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_localisation_graph(n):
    # Récupération des données
    localisation_data = fetch_localisation_defauts_paiement_data()

    # Calcul du point médian pour centrer la carte
    median_lat = sum(item['latitude'] for item in localisation_data) / len(localisation_data)
    median_lon = sum(item['longitude'] for item in localisation_data) / len(localisation_data)

    # Création du graphique
    fig = px.scatter_mapbox(localisation_data,
                            lat='latitude',
                            lon='longitude',
                            hover_name='nom',
                            hover_data=['prenom'],
                            color_discrete_sequence=["red"],  # Ajustez la couleur comme vous le souhaitez
                            size_max=15,
                            zoom=15,  # Ajustez le zoom pour voir les rues clairement
                            center=dict(lat=median_lat, lon=median_lon)  # Centrer la carte
                            )
    
    # Réglage de la hauteur du graphique
    fig.update_layout(height=630)  # Ajustez la hauteur selon vos besoins

    return fig


# Ajout du graphique à l'interface
localisation_desc = html.P("Localisation des défauts de paiement", style={"textAlign": "center", "color": "white"})
graphs_row_5 = dbc.Row([
    dbc.Col([localisation_desc, dbc.Card(dcc.Graph(id='localisation-defauts-graph'), className="shadow-lg p-3 mb-5 bg-dark rounded")], md=12)
], className="mb-4")



app.layout = dbc.Container([
    dcc.Interval(
        id='interval-component',
        interval=10*1000,
        n_intervals=0
    ),
    html.Div([
        html.Img(src="assets/logo.png", height="100px", style={"position": "absolute", "left": "20px", "top": "10px"}),
        html.H1("Tableau de Bord Taxes Municipales", style={"textAlign": "center", "color": "white", "marginBottom": "30px"}),
    ]),
    cards_row,
    graphs_row_2,
    graphs_row_3,
    graphs_row_4,
    graphs_row_5
    
], className="mt-5", fluid=True)

if __name__ == "__main__":
   app.run_server(debug=False)


