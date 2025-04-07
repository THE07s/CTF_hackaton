# Script d'initialisation pour l'utilisateur niveau29

import os
import random
import CTF_lib
import subprocess

def main():
    NIVEAU = 29
    SUIVANT = 30

    mdp_suivant = CTF_lib.get_mdp_hash(SUIVANT)
    dossier = f"/home/niveau{NIVEAU}"

    # Générer un code PIN à 4 chiffres
    pin = f"{random.randint(0, 9999):04d}"
    print(f"[DEBUG] Niveau {NIVEAU}: PIN utilisé pour OpenSSL = {pin}")

    chemin_clair = "/tmp/clair.txt"
    chemin_chiffre = os.path.join(dossier, "motdepasse.enc")

    # Écrire le mot de passe en clair temporairement
    with open(chemin_clair, "w") as f:
        f.write(mdp_suivant + "\n")

    # Chiffrer avec openssl
    subprocess.run([
        "openssl", "enc", "-aes-256-cbc",
        "-salt", "-in", chemin_clair, "-out", chemin_chiffre,
        "-pass", f"pass:{pin}"
    ], check=True)

    os.remove(chemin_clair)

    os.system(f"chown niveau{NIVEAU}:niveau{NIVEAU} {chemin_chiffre}")
    os.system(f"chmod 640 {chemin_chiffre}")

    # Readme
    contenu_readme = f"""Bienvenue dans le niveau {NIVEAU} du CTF hackathon.

L'objectif de ce niveau :
Déchiffrer un fichier protégé par un mot de passe (un code PIN à 4 chiffres).

Pour t'aider :
Un fichier a été chiffré , et un PIN à 4 chiffres (ex : 1234).

ℹ️ :
Tu peux utiliser un script pour essayer chaque PIN.

Bonne chance, et n’oublie pas : ouvre les 👀
"""
    chemin_readme = os.path.join(dossier, "readme")
    with open(chemin_readme, "w") as f:
        f.write(contenu_readme)

    os.system(f"chown niveau{NIVEAU}:niveau{NIVEAU} {chemin_readme}")
    os.system(f"chmod 640 {chemin_readme}")

    # Restreindre le home
    CTF_lib.dossier_home_lecture(NIVEAU)

    # Lancer niveau suivant
    import niveau30
    niveau30.main()

if __name__ == '__main__':
    main()
