from bs4 import BeautifulSoup
import requests
import re

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


imslp_link_converter(("https://imslp.org/index.php?title=Consolations_and_Liebestr%C3%A4ume_for_the_Piano_(Liszt,_Franz)&action=edit"))



def downloadsheet(image_url):
    response = requests.get(image_url)

    with open("myfile.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    return
