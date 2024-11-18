from bs4 import BeautifulSoup
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

class WikiChatbot:
    def __init__(self, wiki_url):
        self.wiki_url = "https://wiki.testing.losa0.com"
        self.pages = {}
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        
    def extract_content(self):
        """Extrae el contenido de las páginas de Wiki.js"""
        # Aquí deberías implementar la lógica para extraer el contenido
        # Este es un ejemplo básico usando requests y BeautifulSoup
        response = requests.get(f"{self.wiki_url}/sitemap")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encuentra todos los enlaces a páginas
        for link in soup.find_all('a', href=True):
            page_url = link['href']
            if page_url.startswith('/'):
                page_content = self._get_page_content(page_url)
                self.pages[page_url] = page_content
    
    def _get_page_content(self, page_url):
        """Obtiene el contenido de una página específica"""
        response = requests.get(f"{self.wiki_url}{page_url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        # Ajusta el selector según la estructura de tu Wiki.js
        content = soup.find('div', class_='content')
        return content.text if content else ""
    
    def train(self):
        """Prepara los vectores TF-IDF para la búsqueda"""
        documents = list(self.pages.values())
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
    
    def find_answer(self, question, threshold=0.3):
        """Encuentra la respuesta más relevante para una pregunta"""
        question_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, self.tfidf_matrix)
        
        best_match_idx = np.argmax(similarities[0])
        best_match_score = similarities[0][best_match_idx]
        
        if best_match_score < threshold:
            return "Lo siento, no encontré una respuesta relevante. Por favor, reformula tu pregunta."
        
        # Devuelve el contenido de la página más relevante
        return list(self.pages.values())[best_match_idx]
    
    def save_knowledge(self, filename='wiki_knowledge.json'):
        """Guarda el contenido extraído en un archivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.pages, f, ensure_ascii=False, indent=4)
    
    def load_knowledge(self, filename='wiki_knowledge.json'):
        """Carga el contenido desde un archivo JSON"""
        with open(filename, 'r', encoding='utf-8') as f:
            self.pages = json.load(f)

# Ejemplo de uso
def setup_chatbot(wiki_url):
    chatbot = WikiChatbot(wiki_url)
    try:
        # Intenta cargar conocimiento existente
        chatbot.load_knowledge()
    except FileNotFoundError:
        # Si no existe, extrae y guarda nuevo conocimiento
        chatbot.extract_content()
        chatbot.save_knowledge()
    
    chatbot.train()
    return chatbot

# Función simple para interfaz de línea de comandos
def run_cli_interface(chatbot):
    print("¡Bienvenido al Chatbot de Wiki! (escribe 'salir' para terminar)")
    while True:
        question = input("\nTu pregunta: ")
        if question.lower() == 'salir':
            break
        answer = chatbot.find_answer(question)
        print("\nRespuesta:", answer)