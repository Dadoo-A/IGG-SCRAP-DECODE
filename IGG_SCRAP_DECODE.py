import subprocess
import pyfiglet

# Fonction pour afficher du texte en ASCII
def print_ascii_intro(text):
    # Génération du texte ASCII stylé
    ascii_art = pyfiglet.figlet_format(text, font="starwars")
    print(ascii_art)

def main():
    # Afficher le texte stylé en ASCII
    print_ascii_intro("IGG SCRAP & DECODE")
    print("by DADOO (et chatgpt ce fou la)")
    
    # Lancer IGG_SCRAPER.py
    print("Lancement de IGG_SCRAPER.py...")
    try:
        subprocess.run(["python", "IGG_SCRAPER.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de l'exécution de IGG_SCRAPER.py : {e}")
    
    # Lancer DECODE_URL.py
    print("Lancement de DECODE_URL.py...")
    try:
        subprocess.run(["python", "DECODE_URL.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de l'exécution de DECODE_URL.py : {e}")

if __name__ == "__main__":
    main()
