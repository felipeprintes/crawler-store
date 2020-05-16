from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from sqlalchemy import *

"""String de conexão com o banco"""
engine = create_engine('postgresql://postgres@localhost/crawler_book',echo=True)

def main():
    # url de pesquisa
    for pag in range(1,3):
        url = 'http://books.toscrape.com/catalogue/'+'page-'+str(pag)+'.html'

        """Tratamento de erro"""
        try:
            #lendo a URL com a urllopen
            html = urlopen(url)
        except HTTPError as e:
        # Erros HTTP
            print(e)
        except URLError as e:
            # URL errada
            print('The server could not be found!')

        """Instância do BeautifulSoup"""
        bs = BeautifulSoup(html, 'html.parser')

        """Captura Livros"""
        livros_site = bs.select('.product_pod')
        preco = []
        stock = []
        nome_livro = []

        for livro in livros_site:
            preco.append(livro.find('p', class_='price_color').text[1:])
            stock.append(livro.find('p', class_='instock availability').text.strip())
            nome_livro.append(livro.find('h3').text)

        """Chamada da função para insert no banco"""
        banco_insert(preco, nome_livro, stock)

def banco_insert(preco, nome_livro, stock):
    for i in range(len(preco)):
        engine.execute(
            "INSERT INTO livro(nome, preco, stock) VALUES('{}', '{}', '{}')". \
                format(nome_livro[i].replace("'","''"), preco[i], stock[i])
        )

if __name__=='__main__':
    main()