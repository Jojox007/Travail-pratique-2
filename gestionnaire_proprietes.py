"""
Ce module est responsable de la gestion des propriétés dans l'application IFT-1004 DuProprio,
incluant l'ajout de nouvelles propriétés, la liste et le filtrage des propriétés disponibles.

Fonctions:
- `lister_proprietes()`: Liste toutes les propriétés disponibles.
- `filtrer_proprietes()`: Filtre les propriétés en fonction des critères de l'utilisateur.
- `ajouter_propriete()`: Ajoute une nouvelle propriété si l'utilisateur est connecté.

Dépendances:
- `gestionnaire_donnees`: Pour lire et écrire dans le fichier des propriétés.
- `gestionnaire_utilisateurs`: Pour vérifier si un utilisateur est connecté.
- `utilitaires`: Pour des fonctions auxiliaires comme l'affichage de tableaux formatés,
et le formatage de montants en dollars.
"""
from gestionnaire_donnees import charger_proprietes, sauvegarder_propriete
from gestionnaire_utilisateurs import utilisateur_est_connecte
from utilitaires import afficher_tableau

# from gestionnaire_donnees import charger_proprietes, sauvegarder_propriete
# from gestionnaire_utilisateurs import utilisateur_est_connecte
# from utilitaires import afficher_tableau, formater_argent


TYPES_DE_PROPRIETE = ["Maison", "Appartement", "Condo", "Studio"]
VILLES = ["Québec", "Montréal", "Toronto", "Ottawa"]


def lister_proprietes():
    """Liste toutes les propriétés disponibles.

    Récupère les propriétés à partir du fichier de données et les affiche dans un tableau formaté.
    Si aucune propriété n'est disponible, affiche un message approprié.
    """
    # Charger les propriétés du ficheirs proprietes.json
    proprietes = charger_proprietes()
    # transformer propriete en liste de liste
    proprietes_list = [list(propriete.values()) for propriete in proprietes]

    afficher_tableau (proprietes_list, ["prix", "ville", "type", "chambres", "salles_de_bain"])
    return proprietes






def filtrer_proprietes():
    """Filtre les propriétés en fonction des critères de l'utilisateur.

    Affiche un menu permettant de choisir les critères de filtrage (prix, ville, type de propriété, chambres,
    salles de bains) et affiche les propriétés correspondant aux critères choisis. Si aucune propriété ne correspond,
    affiche un message approprié.
    """
    #afficher un menu permettant de choisir les critères de filtrage

    print("Choisissez les critères de filtrage:")
    prix_minimum, prix_maximum = demander_plage_de_prix(True)
    ville = demander_ville(True)
    type_de_propriete = demander_type_de_propriete(True)
    nombre_chambre = demander_nombre("Nombre de chambres minimum", True)
    nombre_salle_de_bain = demander_nombre("Nombre de salles de bain minimum", True)

    # afficher les proprietes correspondant aux criteres choisis

    proprietes = charger_proprietes()
    proprietes_filtrees = []

    for propriete in proprietes:
        if (
                (prix_minimum is None or propriete["prix"] >= prix_minimum)
                and (prix_maximum is None or propriete["prix"] <= prix_maximum)
                and (ville is None or propriete["ville"] == ville)
                and (type_de_propriete is None or propriete["type"] == type_de_propriete)
                and (nombre_chambre is None or propriete["chambres"] >= nombre_chambre)
                and (nombre_salle_de_bain is None or propriete["salles de bains"] >= nombre_salle_de_bain)
        ):
            proprietes_filtrees.append(list(propriete.values()))
    if proprietes_filtrees:
        afficher_tableau(proprietes_filtrees, ["prix", "ville", "type", "chambres", "salles_de_bain"])
    else:
        print("Aucune propriété ne correspond aux critères de filtrage.")


def ajouter_propriete():
    """Ajoute une nouvelle propriété si l'utilisateur est connecté.

    Demande à l'utilisateur de saisir les détails de la nouvelle propriété (prix, ville, type, chambres,
    salles de bains) et les enregistre dans le fichier de propriétés. Si la fonction est appelée alors qu'il n'y a pas
    d'utilisateur connecté, un message approprié est affiché.
    """

    #Demander àa l'utilisateur les détails

    if utilisateur_est_connecte() is True :
        prix = int(input("Prix: "))
        ville = demander_ville()
        type_de_propriete = demander_type_de_propriete()
        nombre_chambre = demander_nombre("Nombre de chambres: ")
        nombre_salle_de_bain = demander_nombre("Nombre de salles de bain: ")

        propriete_à_sauvegarder = {
                                    "prix": {prix},
                                    "ville": {ville},
                                    "type": {type_de_propriete},
                                    "chambres": {nombre_chambre},
                                    "salles de bains": {nombre_salle_de_bain}}

        propriete_à_sauvegarder_list= list(propriete_à_sauvegarder.values())

        sauvegarder_propriete(propriete_à_sauvegarder_list)

    else:
        print ("Aucun utilisateur est connecté, veuillez-vous connecter!")


def demander_plage_de_prix(optionnel=False):
    """Demande à l'utilisateur de saisir une plage de prix.

    Args:
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        tuple: (prix_minimum, prix_maximum)
    """
    while True:
        try:
            prix_minimum = input("Prix minimum: ")
            prix_maximum = input("Prix maximum: ")
            if optionnel and not prix_minimum and not prix_maximum:
                return None, None
            prix_minimum = int(prix_minimum) if prix_minimum else None
            prix_maximum = int(prix_maximum) if prix_maximum else None
            if (
                prix_minimum is not None
                and prix_maximum is not None
                and prix_minimum > prix_maximum
            ):
                raise ValueError(
                    "Le prix minimum doit être inférieur ou égal au prix maximum."
                )
            return prix_minimum, prix_maximum
        except ValueError as e:
            print(e)


def demander_ville(optionnel=False):
    """Demande à l'utilisateur de choisir une ville parmi les choix définis.

    Args:
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        str: La ville choisie.
    """
    print(f"Choisissez une ville parmi les suivantes: {', '.join(VILLES)}")
    while True:
        ville = input("Ville: ")
        if optionnel and not ville:
            return None
        if ville in VILLES:
            return ville
        print(f"Ville invalide. Choisissez parmi: {', '.join(VILLES)}")


def demander_type_de_propriete(optionnel=False):
    """Demande à l'utilisateur de choisir un type de propriété parmi les choix définis.

    Args:
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        str: Le type de propriété choisi.
    """
    print(
        f"Choisissez un type de propriété parmi les suivants: {', '.join(TYPES_DE_PROPRIETE)}"
    )
    while True:
        type_de_propriete = input("Type de propriété: ")
        if optionnel and not type_de_propriete:
            return None
        if type_de_propriete in TYPES_DE_PROPRIETE:
            return type_de_propriete
        print(
            f"Type de propriété invalide. Choisissez parmi: {', '.join(TYPES_DE_PROPRIETE)}"
        )


def demander_nombre(prompt, optionnel=False):
    """Demande à l'utilisateur de saisir un nombre.

    Args:
        prompt (str): Le message à afficher pour la saisie.
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        int: Le nombre saisi.
    """
    while True:
        nombre = input(f"{prompt}: ")
        if optionnel and not nombre:
            return None
        try:
            return int(nombre)
        except ValueError:
            print("Valeur invalide. Veuillez saisir un nombre.")
