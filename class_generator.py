import requests
import json
from bs4 import BeautifulSoup


URL = 'https://nepalilanguage.org/alphabet/'
numbers = {
        '36': ['०', 'sunna'],
        '37': ['१', 'ek'],
        '38': ['२', 'dui'],
        '39': ['३', 'tin'],
        '40': ['४', 'char'],
        '41': ['५', 'pach'],
        '42': ['६', 'chha'],
        '43': ['७', 'sat'],
        '44': ['८', 'aath'],
        '45': ['९', 'nau'],
    }


def upload_class_index():
    """
    Import character data and create class index file.
    Source for class data: https://nepalilanguage.org/alphabet/
    File source: "dataset/dhcd_class_index.json"
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')

    alpha_elems = soup.find('h4').next_sibling.find_all('span', class_='letter-box')
    alphabets = [[str(al.contents[1]), str(al.contents[0].text)] for al in alpha_elems]

    # create alphabet dict
    char_class = dict()
    for i in range(len(alphabets)):
        char_class[str(i)] = alphabets[i]
   
    # add number dict
    char_class.update(numbers)

    # write to file
    with open('dataset/dhcd_class_index.json', 'w') as fd:
            json.dump(char_class, fd)
