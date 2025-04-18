# Script d'initialisation pour l'utilisateur niveau5

import os
import random
import CTF_lib
import niveau6

def main():
    NIVEAU = 5
    SUIVANT = 6

    # Génère et enregistre le mot de passe du niveau suivant
    mdp_suivant = CTF_lib.get_mdp_hash(SUIVANT)
    CTF_lib.ecrire_fichier_mdp(SUIVANT, mdp_suivant)

    # Dossier racine contenant les sous-dossiers
    dossier_base = f"/home/niveau{NIVEAU}/jeSuisLa"
    os.makedirs(dossier_base, exist_ok=True)

    # Choix aléatoire du dossier contenant le fichier secret
    index_correct = random.randint(0, 19)

    for i in range(20):
        sous_dossier = f"{dossier_base}/peutEtreIci{str(i).zfill(2)}"
        os.makedirs(sous_dossier, exist_ok=True)

        if i == index_correct:
            chemin_fichier = f"{sous_dossier}/.fichier{random.randint(0, 99)}"
            with open(chemin_fichier, "w") as f:
                contenu = mdp_suivant + "\n" + "x" * (1033 - len(mdp_suivant) - 1)
                f.write(contenu)
        else:
            chemin_fichier = f"{sous_dossier}/.fichier{random.randint(0, 99)}"
            taille_random = random.choice([1020, 1040, 1100])
            with open(chemin_fichier, "wb") as f:
                f.write(os.urandom(taille_random))

        os.system(f"chown -R niveau{NIVEAU}:niveau{NIVEAU} '{sous_dossier}'")
        os.system(f"chmod 700 '{sous_dossier}'")

    # Fichier readme explicatif
    contenu_readme = f"""\
Bienvenue dans le niveau {NIVEAU} du CTF hackathon.

Objectif:
Pars en exploration ! Un fichier bien caché t’attend quelque part dans l’arborescence… \
Il renferme le précieux mot de passe pour passer au niveau suivant. \
À toi de le débusquer !

Pour t'aider :
Le fichier que tu recherches est différent des autres… Il est masqué, et possède une caractéristique unique. \
Retiens bien ceci : le fichier contenant le mot de passe est quelque part sous le répertoire inhere et il répond à tous les critères suivants :\
Il est lisible par un humain\
Il fait exactement 1033 octets\
Il n’est pas exécutable\
Alors, garde ton esprit en alerte parce que chaque détail compte.

ℹ️ :
Une commande spéciale entre ls, cd, cat, file, du, find, te permettra de révéler ce que l’œil ne voit pas et répérer le bon fichier. \
Mais sauras-tu t’en servir au bon moment ?

Bonne chance, et n’oublie pas : les secrets aiment se cacher là où personne ne regarde 👀
"""
    chemin_readme = f"/home/niveau{NIVEAU}/readme"
    with open(chemin_readme, "w") as f:
        f.write(contenu_readme)
    os.system(f"chown niveau{NIVEAU}:niveau{NIVEAU} {chemin_readme}")
    os.system(f"chmod 640 {chemin_readme}")

    # Restreint le home
    CTF_lib.dossier_home_lecture(NIVEAU)

    # Niveau suivant
    niveau6.main()

if __name__ == '__main__':
    main()
