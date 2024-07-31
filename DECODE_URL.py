import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def bluemediafiles_decode_key(encoded):
    key = ''
    for i in range(int(len(encoded) / 2) - 5, -1, -2):
        key += encoded[i]
    for i in range(int(len(encoded) / 2) + 4, len(encoded), 2):
        key += encoded[i]
    return key

def bypass_igg_games(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails

        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script')

        for script in scripts:
            if script.string:  # Vérifier que script.string n'est pas None
                match = re.search(r'Goroi_n_Create_Button\("(?P<encoded>.+?)"\);', script.string)
                if match:
                    encoded_key = match.group('encoded')
                    decoded_key = bluemediafiles_decode_key(encoded_key)
                    base_url = url.split('/url-generator')[0]
                    redirect_url = urljoin(base_url, f'get-url.php?url={decoded_key}')
                    return redirect_url

    except requests.exceptions.RequestException as e:
        print(f"Error processing URL {url}: {e}")
    
    return None

def resolve_final_url(redirect_url):
    try:
        response = requests.get(redirect_url)
        response.raise_for_status()  # Raise an error if the request fails

        # Check if there's a redirection
        if response.history:
            return response.url
        else:
            # No redirection, return the content URL directly
            return redirect_url
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return "Le fichier a été supprimé"
        else:
            return f"Error: {e.response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

def process_urls(input_file, output_file):
    with open(input_file, 'r') as infile:
        urls = infile.readlines()

    results = []
    for url in urls:
        url = url.strip()  # Remove any surrounding whitespace or newline characters
        if url:
            print(f"Processing URL: {url}")
            redirect_url = bypass_igg_games(url)
            if redirect_url:
                final_url = resolve_final_url(redirect_url)
                results.append(f'{final_url}')
            else:
                results.append(f'No matching script found.')

    with open(output_file, 'w') as outfile:
        for result in results:
            outfile.write(result + '\n')
    print ('L\'ensemble des URLs sont sauvegardé dans le fichier : output_urls.txt')

# Utilisation
input_file = 'input_urls.txt'  # Nom du fichier contenant les URL à traiter
output_file = 'output_urls.txt'  # Nom du fichier pour les résultats
process_urls(input_file, output_file)
