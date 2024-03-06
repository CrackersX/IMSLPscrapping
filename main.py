from bs4 import BeautifulSoup
import requests
import re
import urllib.request

def imslpdownload(link):
    L=[]
    result = requests.get(link)
    soup = BeautifulSoup(result.text, 'html.parser')
    for link in soup.find_all('a'):
        L.append(link.get('href'))
    # Expression régulière pour le modèle de lien
    pattern = r"https://imslp\.org/wiki/Special:ImagefromIndex/\d+$"
    print(L)
# Filtrer les liens valides
    liens_valides = [lien for lien in L if isinstance(lien, str) and re.match(pattern, lien) or lien == "/wiki/IMSLP:Public_Domain"]

    print(liens_valides)



#imslpdownload("https://imslp.org/wiki/Bol%C3%A9ro,_M.81_(Ravel,_Maurice)")

def imslpgetcode(link):
    result = requests.get(link)
    soup = BeautifulSoup(result.text, 'html.parser')
    # Find the <textarea> tag
    textarea_tag = soup.find('textarea')
    # Extract the text content
    text_content = textarea_tag.get_text()

    # Utilisation d'expressions régulières pour extraire les liens des fichiers PDF entre *****FILES***** et la prochaine balise ===
    matches = re.search(r'\| \*\*\*\*\*FILES\*\*\*\*\* =\s*(.*?)\n===', text_content, re.DOTALL)

    # Si des correspondances sont trouvées
    if matches:
        # Extraire le texte entre *****FILES***** et la prochaine balise ===
        files_text = matches.group(1)
        
        # Extraire les liens des fichiers PDF
        file_links = re.findall(r'\{\{#fte:imslpfile\s*\|File Name 1=(.*?)\.pdf', files_text)
        
        # Affichage des liens des fichiers PDF
        print(file_links)
    else:
        print("Aucune correspondance trouvée entre '*****FILES*****' et la prochaine balise '==='.")

    return file_links

imslpgetcode("https://imslp.org/index.php?title=Bol%C3%A9ro,_M.81_(Ravel,_Maurice)&action=edit")

def imslptruelink(file_links):
    link=file_links[0]
    formatedlink="https://imslp.org/wiki/File:"+link+".pdf"
    print(formatedlink)
    return formatedlink

imslptruelink(imslpgetcode("https://imslp.org/index.php?title=Bol%C3%A9ro,_M.81_(Ravel,_Maurice)&action=edit"))

def getlastlink(file_links):
    # URL de la page que vous souhaitez analyser
    url = file_links

    # Obtenir le contenu de la page
    response = requests.get(url)
    html_content = response.text

    # Utiliser BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Trouver tous les liens dans la page
    all_links = soup.find_all("a", href=True)

    # Filtrer les liens qui commencent par "/images/"
    image_links = [link['href'] for link in all_links if link['href'].startswith("/images/")]

    # Afficher les liens trouvés
    linkfinal="https://imslp.org/"+image_links[0]
    print(linkfinal)

    return linkfinal

getlastlink(imslptruelink(imslpgetcode("https://imslp.org/index.php?title=Bol%C3%A9ro,_M.81_(Ravel,_Maurice)&action=edit")))

def downloadsheet(image_url):
    response = requests.get(image_url)

    with open("myfile.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    return

downloadsheet(getlastlink(imslptruelink(imslpgetcode("https://imslp.org/index.php?title=Bol%C3%A9ro,_M.81_(Ravel,_Maurice)&action=edit"))))
