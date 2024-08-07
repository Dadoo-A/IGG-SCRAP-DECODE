try:
    from bs4 import BeautifulSoup
    import urllib.request
    import re
except ImportError:
    print("Some modules are not installed. Run \n python -m pip install -r requirements.txt")
    exit()

# credit tingtingths https://greasyfork.org/en/scripts/423435-igg-games-bluemediafiles-bypass/code
# Decryption process of the Goroi_n_Create_Button token
def _bluemediafiles_decodeKey(encoded):
    key = ''
    i = int(len(encoded) / 2 - 5)
    while i >= 0:
        key += encoded[i]
        i = i - 2
    i = int(len(encoded) / 2 + 4)
    while i < len(encoded):
        key += encoded[i]
        i = i + 2
    return key

def url_generator_link_decode(link):
    sec_req = urllib.request.Request(
        link,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    try:
        request = urllib.request.urlopen(sec_req)
    except urllib.error.URLError:
        return "URL could not be opened."

    soup = BeautifulSoup(request, "lxml")

    for script in soup.find_all("script"):
        matches = re.findall(r"Goroi_n_Create_Button\(\"(.*?)\"\)", str(script))
        if len(matches) > 0:
            string = 'https://bluemediafiles.com/get-url.php?url=' + _bluemediafiles_decodeKey(matches[0])
            third_req = urllib.request.Request(
                string,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            try:
                request = urllib.request.urlopen(third_req)
            except urllib.error.URLError:
                print("URL could not be opened.")
                return None
            result_url = request.geturl()
            if "mega.nz" in result_url:
                result_url = result_url.replace("%23", "#")
            return result_url

def main():
    url_choice = input("IGG-Games Link: ")
    if not (url_choice.startswith("http://") or url_choice.startswith("https://")):
        url_choice = "http://" + url_choice
    req = urllib.request.Request(
        url_choice,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    try:
        request = urllib.request.urlopen(req)
    except urllib.error.URLError:
        print("URL could not be opened.")
        exit()

    soup = BeautifulSoup(request, "lxml")
    source_list = []

    # Iterate through all sources
    for source in soup.find_all("b"):
        source_list += re.findall(
            r"Link [0-9]*[a-zA-Z]+\.* *[0-9]*[a-zA-Z]+\.*[a-zA-Z]*", str(source))
        # Remove torrent link if available
        if str(source).__contains__("TORRENT"):
            source_list.pop(0)

    # Remove 'Link' text from source_list
    for count in range(len(source_list)):
        item = source_list[count]
        source_list[count] = item[5:]

    if not source_list:
        print("No Link sources found.")
        exit()
    
    for counter, value in enumerate(source_list):
        print(str(counter + 1) + ") " + value)
    
    source_choice = input("Choose download source: ")
    while not isinstance(source_choice, int):
        try:
            source_choice = int(source_choice)
            if source_choice > len(source_list):
                raise ValueError
        except ValueError:
            source_choice = input(
                "Please enter a number between 1 and " + str(len(source_list)) + ": ")

    finalOutput = []
    isUpdate = False

    for paragraph in soup.find_all("p"):
        if isUpdate:
            for hyperlink in paragraph("a"):
                link = hyperlink.get("href")
                if "url-generator" in link:
                    link = url_generator_link_decode(link)
                if link:
                    finalOutput.append(link)
            isUpdate = False
        for span in paragraph("span"):
            if "UPDATE" in span.text:
                print(span.text)
                isUpdate = True

        if source_list[source_choice - 1] in paragraph.text:
            print("\n")
            for hyperlink in paragraph("a"):
                string = hyperlink.get('href')
                # Check if button is already redirecting to direct link
                if "http://bluemediafiles.com" not in string:
                    sec_req = urllib.request.Request(
                        string,
                        data=None,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                        }
                    )
                    try:
                        request = urllib.request.urlopen(sec_req)
                    except urllib.error.URLError:
                        print("URL could not be opened.")
                        continue
                    link = request.geturl()
                else:
                    sec_req = urllib.request.Request(
                        string,
                        data=None,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                        }
                    )
                    try:
                        request = urllib.request.urlopen(sec_req)
                    except urllib.error.URLError:
                        print("URL could not be opened.")
                        continue

                    soup = BeautifulSoup(request, "lxml")

                    for script in soup.find_all("script"):
                        matches = re.findall(
                            r"Goroi_n_Create_Button\(\"(.*?)\"\)", str(script))
                        if len(matches) > 0:
                            string = 'https://bluemediafiles.com/get-url.php?url=' + \
                                _bluemediafiles_decodeKey(matches[0])
                            third_req = urllib.request.Request(
                                string,
                                data=None,
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                                }
                            )
                            try:
                                request = urllib.request.urlopen(third_req)
                            except urllib.error.URLError:
                                print("URL could not be opened.")
                                continue
                            link = request.geturl()
                            if "mega.nz" in link:
                                link = link.replace("%23", "#")
                if link:
                    finalOutput.append(link)

            print("\n")

    # Write finalOutput to file
    with open('input_urls.txt', 'w') as f:
        for item in finalOutput:
            f.write(f"{item}\n")
    
    print("Links have been written to input_urls.txt")

main()
