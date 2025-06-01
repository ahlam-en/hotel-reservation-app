import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Gestion Hôtelière", layout="wide")
st.title("🏨 Système de Gestion Hôtelière")

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('hotel.db')
    conn.row_factory = sqlite3.Row
    return conn

# Fonctions principales
def get_reservations():
    conn = get_db_connection()
    query = '''
    SELECT r.id, c.nom AS client, h.ville AS ville_hotel,
           r.date_arrivee, r.date_depart, ch.numero AS chambre,
           tc.nom AS type_chambre
    FROM Reservation r
    JOIN Client c ON r.id_client = c.id
    JOIN Chambre ch ON r.id_chambre = ch.id
    JOIN Hotel h ON ch.id_hotel = h.id
    JOIN TypeChambre tc ON ch.id_type_chambre = tc.id
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_clients():
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT id, nom, email, telephone FROM Client', conn)
    conn.close()
    return df

def get_available_rooms(start_date, end_date):
    conn = get_db_connection()
    query = '''
    SELECT ch.id, ch.numero, ch.etage, tc.nom AS type, tc.prix_nuit, h.ville
    FROM Chambre ch
    JOIN TypeChambre tc ON ch.id_type_chambre = tc.id
    JOIN Hotel h ON ch.id_hotel = h.id
    WHERE ch.id NOT IN (
        SELECT id_chambre FROM Reservation
        WHERE (date_arrivee <= ? AND date_depart >= ?)
        OR (date_arrivee BETWEEN ? AND ?)
        OR (date_depart BETWEEN ? AND ?)
    )
    '''
    params = (end_date, start_date, start_date, end_date, start_date, end_date)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def add_client(nom, email, telephone, adresse, ville, code_postal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Client (nom, email, telephone, adresse, ville, code_postal) VALUES (?, ?, ?, ?, ?, ?)',
        (nom, email, telephone, adresse, ville, code_postal)
    )
    conn.commit()
    conn.close()

def add_reservation(id_client, id_chambre, date_arrivee, date_depart):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Reservation (id_client, id_chambre, date_arrivee, date_depart) VALUES (?, ?, ?, ?)',
        (id_client, id_chambre, date_arrivee, date_depart)
    )
    conn.commit()
    conn.close()

# Interface utilisateur
menu = st.sidebar.selectbox("Menu", [
    "📋 Liste des Réservations",
    "👥 Liste des Clients",
    "🛏️ Chambres Disponibles",
    "➕ Ajouter un Client",
    "📅 Ajouter une Réservation"
])

if menu == "📋 Liste des Réservations":
    st.header("📋 Liste des Réservations")
    reservations = get_reservations()
    if not reservations.empty:
        st.dataframe(reservations, hide_index=True)
    else:
        st.info("Aucune réservation trouvée")

elif menu == "👥 Liste des Clients":
    st.header("👥 Liste des Clients")
    clients = get_clients()
    if not clients.empty:
        st.dataframe(clients, hide_index=True)
    else:
        st.info("Aucun client enregistré")

elif menu == "🛏️ Chambres Disponibles":
    st.header("🛏️ Recherche de Chambres Disponibles")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Date d'arrivée", datetime.now())
    with col2:
        end_date = st.date_input("Date de départ", datetime.now() + pd.Timedelta(days=1))

    if st.button("Rechercher"):
        if start_date < end_date:
            rooms = get_available_rooms(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            if not rooms.empty:
                st.success(f"{len(rooms)} chambres disponibles trouvées")
                st.dataframe(rooms, hide_index=True)
            else:
                st.warning("Aucune chambre disponible pour cette période")
        else:
            st.error("❌ La date de départ doit être après la date d'arrivée")

elif menu == "➕ Ajouter un Client":
    st.header("➕ Ajouter un Nouveau Client")

    with st.form("client_form", clear_on_submit=True):
        nom = st.text_input("Nom complet*", placeholder="Jean Dupont")
        email = st.text_input("Email*", placeholder="jean.dupont@example.com")
        telephone = st.text_input("Téléphone*", placeholder="0612345678")
        adresse = st.text_input("Adresse", placeholder="12 Rue de Paris")
        ville = st.text_input("Ville", placeholder="Paris")
        code_postal = st.text_input("Code postal", placeholder="75001")

        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            if nom and email and telephone:
                add_client(nom, email, telephone, adresse, ville, code_postal)
                st.success("✅ Client ajouté avec succès!")
            else:
                st.error("⚠️ Les champs marqués d'un * sont obligatoires")

elif menu == "📅 Ajouter une Réservation":
    st.header("📅 Ajouter une Réservation")

    clients = get_clients()
    client_list = clients['nom'].tolist()

    if client_list:
        with st.form("reservation_form", clear_on_submit=True):
            client_name = st.selectbox("Client*", client_list)

            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Date d'arrivée*", datetime.now())
            with col2:
                end_date = st.date_input("Date de départ*", datetime.now() + pd.Timedelta(days=1))

            if start_date < end_date:
                rooms = get_available_rooms(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                if not rooms.empty:
                    room_options = [f"N°{row['numero']} (Étage {row['etage']}, {row['type']}, {row['ville']})"
                                  for _, row in rooms.iterrows()]
                    selected_room = st.selectbox("Chambre disponible*", room_options)
                else:
                    st.warning("Aucune chambre disponible pour cette période")
            else:
                st.error("❌ La date de départ doit être après la date d'arrivée")

            submitted = st.form_submit_button("Enregistrer la réservation")
            if submitted:
                if start_date >= end_date:
                    st.error("❌ Dates invalides")
                elif rooms.empty:
                    st.error("❌ Aucune chambre sélectionnée")
                else:
                    client_id = clients[clients['nom'] == client_name].iloc[0]['id']
                    room_id = rooms.iloc[room_options.index(selected_room)]['id']

                    add_reservation(client_id, room_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                    st.success("✅ Réservation enregistrée avec succès!")
    else:
        st.warning("Aucun client disponible. Ajoutez d'abord un client.")
