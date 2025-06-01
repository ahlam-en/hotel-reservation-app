# -*- coding: utf-8 -*-
import sqlite3

def create_database():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    
    # Création des tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Hotel (
        id INTEGER PRIMARY KEY,
        ville TEXT,
        pays TEXT,
        code_postal INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Client (
        id INTEGER PRIMARY KEY,
        adresse TEXT,
        ville TEXT,
        code_postal TEXT,
        email TEXT,
        telephone TEXT,
        nom TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prestation (
        id INTEGER PRIMARY KEY,
        prix REAL,
        description TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TypeChambre (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        prix_nuit REAL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Chambre (
        id INTEGER PRIMARY KEY,
        numero INTEGER,
        etage INTEGER,
        disponible INTEGER,
        id_hotel INTEGER,
        id_type_chambre INTEGER,
        FOREIGN KEY (id_hotel) REFERENCES Hotel(id),
        FOREIGN KEY (id_type_chambre) REFERENCES TypeChambre(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservation (
        id INTEGER PRIMARY KEY,
        date_arrivee TEXT,
        date_depart TEXT,
        id_client INTEGER,
        id_chambre INTEGER,
        FOREIGN KEY (id_client) REFERENCES Client(id),
        FOREIGN KEY (id_chambre) REFERENCES Chambre(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Evaluation (
        id INTEGER PRIMARY KEY,
        date_evaluation TEXT,
        note INTEGER,
        commentaire TEXT,
        id_reservation INTEGER,
        FOREIGN KEY (id_reservation) REFERENCES Reservation(id)
    )
    ''')
    
    # Insertion des données
    hotels = [
        (1, 'Paris', 'France', 75001),
        (2, 'Lyon', 'France', 69002)
    ]
    
    clients = [
        (1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
        (2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
        (3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
        (4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
        (5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')
    ]
    
    prestations = [
        (1, 15, 'Petit-déjeuner'),
        (2, 30, 'Navette aéroport'),
        (3, 0, 'Wi-Fi gratuit'),
        (4, 50, 'Spa et bien-être'),
        (5, 20, 'Parking sécurisé')
    ]
    
    types_chambre = [
        (1, 'Simple', 80),
        (2, 'Double', 120)
    ]
    
    chambres = [
        (1, 201, 2, 0, 1, 1),
        (2, 502, 5, 1, 1, 2),
        (3, 305, 3, 0, 2, 1),
        (4, 410, 4, 0, 2, 2),
        (5, 104, 1, 1, 2, 2),
        (6, 202, 2, 0, 1, 1),
        (7, 307, 3, 1, 1, 2),
        (8, 101, 1, 0, 1, 1)
    ]
    
    reservations = [
        (1, '2025-06-15', '2025-06-18', 1, 1),
        (2, '2025-07-01', '2025-07-05', 2, 2),
        (7, '2025-11-12', '2025-11-14', 2, 7),
        (10, '2026-02-01', '2026-02-05', 2, 5),
        (3, '2025-08-10', '2025-08-14', 3, 3),
        (4, '2025-09-05', '2025-09-07', 4, 4),
        (9, '2026-01-15', '2026-01-18', 4, 6),
        (5, '2025-09-20', '2025-09-25', 5, 8)
    ]
    
    evaluations = [
        (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
        (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
        (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
        (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
        (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
    ]
    
    cursor.executemany('INSERT INTO Hotel VALUES (?, ?, ?, ?)', hotels)
    cursor.executemany('INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)', clients)
    cursor.executemany('INSERT INTO Prestation VALUES (?, ?, ?)', prestations)
    cursor.executemany('INSERT INTO TypeChambre VALUES (?, ?, ?)', types_chambre)
    cursor.executemany('INSERT INTO Chambre VALUES (?, ?, ?, ?, ?, ?)', chambres)
    cursor.executemany('INSERT INTO Reservation VALUES (?, ?, ?, ?, ?)', reservations)
    cursor.executemany('INSERT INTO Evaluation VALUES (?, ?, ?, ?, ?)', evaluations)
    
    conn.commit()
    conn.close()
    print("Base de données créée et peuplée avec succès!")

if __name__ == '__main__':
    create_database()
