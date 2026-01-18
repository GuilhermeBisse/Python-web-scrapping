import requests
from bs4 import BeautifulSoup
import sqlite3


url = 'https://www.idealsoftwares.com.br/indices/ipca_ibge.html'

response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find_all(
    name='table',
    attrs={'class': 'table table-bordered table-striped text-center'},
)[0]

dados_ipca = []

for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if cols:
        date = cols[0].text.strip()
        valor = cols[1].text.strip().replace(' ', '').replace('\n', '')
        if valor:
            dia, mes, ano = date.split('/')
            dados_ipca.append((float(valor), mes, int(ano)))

conn = sqlite3.connect('ipca.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS IPCA (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL,
    mes TEXT,
    ano INTEGER,
    UNIQUE(mes, ano)                
)
''')

for data in dados_ipca:
    valor, mes, ano = data
    cursor.execute('''
    INSERT INTO IPCA (valor, mes, ano)
    VALUES (?, ?, ?)
    ''', (valor, mes, ano))

conn.commit()
conn.close()

print("Web Scrapping da tabela foi realizada com sucesso!")