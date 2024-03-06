from bs4 import BeautifulSoup
import requests
import re
import imslp
import mwclient
from mwclient import Site

lien= "https://imslp.org/index.php?title=Bol%C3%A9ro,_M.81_(Ravel,_Maurice)&action=edit"
###NOT WORKING
user_agent = 'Crackers'
site = Site('en.imslp.org', clients_useragent=user_agent)


cookies = {
    "imslp_wikiLanguageSelectorLanguage": "en",
    "imslpdisclaimeraccepted": "yes",
}
### END

def imslp_getscore(link):
    result = requests.get(link)
    soup = BeautifulSoup(result.text, 'html.parser')
    # Find the <textarea> tag
    textarea_tag = soup.find('textarea')
    # Extract the text content
    text_content = textarea_tag.get_text()
    # Utilisation d'une expression régulière pour trouver tous les liens PDF si la description est "Complete Score"
    matches = re.findall(r'File Name \d+=(.*\.pdf)\n\|File Description \d+=Complete Score', text_content)
    return matches


def newpage(link,what):
    # Obtenir le contenu de la nouvelle page
    response = requests.get(link)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    # Trouver le nouveau lien
    all_links = soup.find_all("a", href=True)

    # Filtrer les liens qui commencent par "what"
    image_links = [link['href'] for link in all_links if link['href'].startswith(what)]
    # lien formaté
    linktformat="https://imslp.org"+image_links[0]
    return linktformat


def imslp_link_converter(file_links):
    #prend la premiere oeuvre complète de la page
    templink=imslp_getscore(file_links)[0]
    formatedlink="https://imslp.org/wiki/File:"+templink
    link2=newpage(formatedlink,"/images/")
    print(link2)

    return link2


imslp_link_converter(lien)
#(+ ajouter redirect)
###NOT WORKING

def downloadsheet(image_url):
    response = requests.get(image_url)

    with open("myfile.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    return
###END
