import requests
from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup
from model.headline import headline

NUMERO_MAX_TAGS = 1

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/consultaNoticias', methods=['GET'])
def consultaNoticias():
    content = requests.get('https://www.eltiempo.com/tecnosfera/novedades-tecnologia')
    soup = BeautifulSoup(content.text, 'lxml')

    headlines = []
    contador = 1

    sectionsClass = ["apertura-seccion","nota listing"]
    for sectionClass in sectionsClass:
        sections = soup.find_all("div", {"class": sectionClass})
        
        for section in sections:
            title = section.find("h3", {"itemprop": "headline"}).a.string
            datePublished = section.find("meta", {"itemprop": "datePublished"})['content']
            description = section.find("div", {"itemprop": "description"}).a.string
            
            link = 'https://www.eltiempo.com' + section.find("h3", {"itemprop": "headline"}).a['href']
            
            subcontent = requests.get(link)
            soupLink = BeautifulSoup(subcontent.text, 'lxml')
            tags = soupLink.find_all("h2", {"class": "tags-en-articulo-tag"})
            tagsHeadline = []
            for tag in tags:
                if len(tagsHeadline) < NUMERO_MAX_TAGS:
                    tagsHeadline.append(tag.a.string)
                else:
                    break        
                    
            resume = soupLink.find("p", {"class": "contenido"})  
            for a in resume.findAll('a', href=True):
                a.extract()        
            resume = resume.get_text()
            headlines.append(headline(contador, title, datePublished, description, tagsHeadline, resume))
            contador += 1 
    
    return jsonify({'code': 'OK', 'rows': [headline.serialize() for headline in headlines]})

if __name__ == '__main__':
    app.run()
