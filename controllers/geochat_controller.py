import os
import logging
import re
import requests
import json
import math
import random
from datetime import datetime
from functools import lru_cache
from flask import jsonify, request, session, redirect, url_for, render_template
from langchain_groq import ChatGroq
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import great_circle
from config.database import execute_query, execute_query_one
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from bs4 import BeautifulSoup  # Para web scraping

logger = logging.getLogger(__name__)

class GeoChatController:
    def __init__(self):
        try:
            self.groq_api_key = os.getenv("GROQ_API_KEY")
            if not self.groq_api_key:
                raise RuntimeError("GROQ_API_KEY não configurada")
            
            self.llm = ChatGroq(
                temperature=0.5,
                model_name="llama3-70b-8192",
                api_key=self.groq_api_key,
                max_retries=3,
                request_timeout=60
            )
            
            # Configura RAG com ChromaDB
            self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            self.vector_store = self._setup_vector_store()
            
            # Configurações de geolocalização
            self.geolocator = Nominatim(user_agent="encantos_da_ilha_turismo")
            self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)
            self.reverse_geocode = RateLimiter(self.geolocator.reverse, min_delay_seconds=1)
            
            # Cache de localizações
            self.location_cache = {}
            
            # Configurações de segurança
            self.blocked_terms = ["senha", "admin", "sql", "delete", "drop", "insert", "update", "alter", "grant"]
            self.allowed_topics = ["restaurante", "evento", "turismo", "ponto turístico", "roteiro", "itinerário", "rota", "distância", "preço", "custo", "imagem", "foto"]
            
            logger.info("GeoChatController inicializado")
        except Exception as e:
            logger.critical(f"Falha crítica na inicialização: {str(e)}")
            raise

    def _setup_vector_store(self):
        """Configura o ChromaDB com dados do banco"""
        try:
            # Carrega dados do banco para o RAG
            events = execute_query("SELECT * FROM eventos")
            restaurants = execute_query("SELECT * FROM restaurantes")
            
            documents = []
            for event in events:
                doc = f"Evento: {event['nome_evento']}. Tipo: {event['tipo']}. Descrição: {event['descricao']}. "
                doc += f"Local: {event['local']}, {event['endereco']}. Data: {event['data_inicio']} a {event['data_fim']}. "
                doc += f"Preço: {event['preco'] or 'Grátis'}. Capacidade: {event['capacidade']} pessoas."
                documents.append(doc)
            
            for restaurant in restaurants:
                doc = f"Restaurante: {restaurant['nome_restaurante']}. Culinária: {restaurant['tipo_culinaria']}. "
                doc += f"Endereço: {restaurant['endereco']}, {restaurant['bairro']}. Preço: {restaurant['faixa_preco']}. "
                doc += f"Abre às: {restaurant['horario_funcionamento']}. Capacidade: {restaurant['capacidade']} lugares."
                documents.append(doc)
            
            # Divide documentos e cria vetores
            texts = self.text_splitter.split_text("\n\n".join(documents))
            return Chroma.from_texts(texts, self.embeddings)
        except Exception as e:
            logger.error(f"Erro ao configurar ChromaDB: {str(e)}")
            return None

    def _rag_search(self, query):
        """Busca contexto relevante usando RAG"""
        if not self.vector_store:
            return ""
        
        try:
            docs = self.vector_store.similarity_search(query, k=5)
            context = "\n\n".join([doc.page_content for doc in docs])
            return f"### Contexto do banco de dados:\n{context}\n\n"
        except Exception as e:
            logger.error(f"Erro na busca RAG: {str(e)}")
            return ""

    def _validate_input(self, user_input):
        """Valida a entrada do usuário para segurança"""
        user_input_lower = user_input.lower()
        
        # Verificar termos bloqueados
        for term in self.blocked_terms:
            if term in user_input_lower:
                return False, "Desculpe, não posso responder a essa solicitação."
        
        # Verificar se o tópico é permitido
        if not any(topic in user_input_lower for topic in self.allowed_topics):
            return False, "Só posso responder sobre turismo em São Luís (eventos, restaurantes, pontos turísticos, rotas, etc.)."
        
        return True, ""

    def _get_precise_coordinates(self, address):
        """Obtém coordenadas precisas com múltiplas estratégias"""
        try:
            # Cache
            if address in self.location_cache:
                return self.location_cache[address]
            
            # Tenta encontrar no banco de dados
            event = execute_query_one("SELECT latitude, longitude FROM eventos WHERE endereco LIKE %s", (f"%{address}%",))
            if event and event.get('latitude'):
                coords = (event['latitude'], event['longitude'])
                self.location_cache[address] = coords
                return coords
            
            restaurant = execute_query_one("SELECT latitude, longitude FROM restaurantes WHERE endereco LIKE %s", (f"%{address}%",))
            if restaurant and restaurant.get('latitude'):
                coords = (restaurant['latitude'], restaurant['longitude'])
                self.location_cache[address] = coords
                return coords
            
            # OpenStreetMap Nominatim
            location = self.geocode(f"{address}, São Luís, MA, Brasil", exactly_one=True)
            if location:
                coords = (location.latitude, location.longitude)
                self.location_cache[address] = coords
                return coords
            
            # API alternativa (Photon)
            photon_url = f"https://photon.komoot.io/api/?q={address}, São Luís, Brasil&limit=1"
            response = requests.get(photon_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['features']:
                    coords = (
                        data['features'][0]['geometry']['coordinates'][1],
                        data['features'][0]['geometry']['coordinates'][0]
                    )
                    self.location_cache[address] = coords
                    return coords
            
            # Fallback: Centro de São Luís
            return (-2.530731, -44.306396)
        
        except Exception as e:
            logger.error(f"Erro na geocodificação de '{address}': {str(e)}")
            return (-2.530731, -44.306396)

    def _get_location_details(self, lat, lon):
        """Obtém detalhes ricos de uma localização"""
        try:
            location = self.reverse_geocode((lat, lon), language='pt', exactly_one=True)
            if location:
                return {
                    "name": location.raw.get('display_name', '').split(',')[0],
                    "address": location.address,
                    "type": self._determine_location_type(location.raw),
                    "lat": lat,
                    "lon": lon
                }
            return {
                "name": "Local desconhecido",
                "address": "São Luís, Maranhão",
                "type": "ponto turístico",
                "lat": lat,
                "lon": lon
            }
        except Exception as e:
            logger.error(f"Erro ao obter detalhes da localização: {str(e)}")
            return {
                "name": "Local desconhecido",
                "address": "São Luís, Maranhão",
                "type": "ponto turístico",
                "lat": lat,
                "lon": lon
            }

    def _determine_location_type(self, raw_data):
        """Determina o tipo de localização com base nos dados do OSM"""
        if 'tourism' in raw_data:
            return raw_data['tourism']
        if 'amenity' in raw_data:
            return raw_data['amenity']
        if 'historic' in raw_data:
            return "monumento histórico"
        if 'shop' in raw_data:
            return "comércio local"
        return "ponto turístico"

    def _get_local_recommendations(self, reference_location, radius=2000, limit=10):
        """Obtém recomendações locais baseadas na localização"""
        try:
            # Busca lugares próximos com Overpass API
            overpass_url = "https://overpass-api.de/api/interpreter"
            query = f"""
                [out:json];
                (
                  node(around:{radius},{reference_location[0]},{reference_location[1]})["tourism"];
                  node(around:{radius},{reference_location[0]},{reference_location[1]})["amenity"="restaurant"];
                  node(around:{radius},{reference_location[0]},{reference_location[1]})["historic"];
                );
                out body {limit};
            """
            response = requests.post(overpass_url, data=query, timeout=20)
            elements = response.json().get('elements', [])
            
            # Processa resultados
            places = []
            for element in elements:
                lat = element.get('lat')
                lon = element.get('lon')
                if not lat or not lon:
                    continue
                    
                places.append(self._get_location_details(lat, lon))
            
            return places
        
        except Exception as e:
            logger.error(f"Erro ao buscar recomendações locais: {str(e)}")
            return []

    def _extract_location_entities(self, text):
        """Extrai entidades geográficas do texto usando heurísticas avançadas"""
        # Lista de locais conhecidos em São Luís
        sao_luis_landmarks = [
            "centro histórico", "praia grande", "lagoa da jansen", "palácio dos leões",
            "teatro arthur azevedo", "fonte do ribeirão", "catedral de são luís",
            "convento das mercês", "museu histórico", "cafua das mercês",
            "praça dom pedro ii", "praça maria aragão", "feira da praia grande",
            "parque do bom menino", "ponte josé sarney", "avenida litorânea",
            "reviver", "rua portugal", "rua da estrela", "são francisco", "ribeirão"
        ]
        
        # Padrões para detecção
        patterns = [
            r"(?:perto|próximo|próxima|nas proximidades|perto de|ao lado do?|vizinho ao?)\s+([\w\s]+)",
            r"(?:em|no|na|no bairro)\s+([\w\s]+)",
            r"(?:rua|avenida|praça|travessa|alameda|viaduto)\s+([\w\s]+)",
            r"centro histórico|centro de são luís",
            r"praia\s+([\w\s]+)"
        ]
        
        # Verificação contra lista de locais conhecidos
        text_lower = text.lower()
        for landmark in sao_luis_landmarks:
            if landmark in text_lower:
                return [landmark]
        
        # Aplicação de expressões regulares
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return [match.group(1).strip()]
        
        # Fallback: Nomear todas as palavras capitalizadas
        return re.findall(r'\b[A-Z][a-z]+\b', text)

    def _search_web(self, query):
        """Busca informações na web sobre um local"""
        try:
            search_url = f"https://www.google.com/search?q={query}+São+Luís+turismo"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extrai snippets de resultados
            results = []
            for g in soup.find_all('div', class_='tF2Cxc'):
                title = g.find('h3').text if g.find('h3') else "Sem título"
                snippet = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else "Sem descrição"
                results.append(f"{title}: {snippet}")
            
            return "\n".join(results[:3])  # Limita a 3 resultados
        except Exception as e:
            logger.error(f"Erro na busca web: {str(e)}")
            return ""

    def _get_place_images(self, place_name, max_images=3):
        """Busca imagens relacionadas a um local"""
        try:
            search_url = f"https://www.google.com/search?tbm=isch&q={place_name}+São+Luís"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extrai URLs de imagens
            image_urls = []
            for img in soup.find_all('img', limit=max_images+2)[2:]:  # Ignora os dois primeiros (logos)
                if 'src' in img.attrs:
                    image_urls.append(img['src'])
            
            return image_urls[:max_images]
        except Exception as e:
            logger.error(f"Erro ao buscar imagens: {str(e)}")
            return []

    def _calculate_distance(self, point1, point2):
        """Calcula a distância em metros entre dois pontos (lat, lon)"""
        return great_circle(point1, point2).meters

    def _generate_itinerary(self, points):
        """Gera um itinerário otimizado entre pontos"""
        # Algoritmo simples para ordenar pontos (poderia usar TSP em implementação real)
        optimized_points = [points[0]]
        remaining_points = points[1:]
        
        while remaining_points:
            closest_point = min(
                remaining_points, 
                key=lambda p: self._calculate_distance(optimized_points[-1], p)
            )
            optimized_points.append(closest_point)
            remaining_points.remove(closest_point)
        
        # Calcula distâncias totais
        total_distance = 0
        for i in range(len(optimized_points) - 1):
            total_distance += self._calculate_distance(optimized_points[i], optimized_points[i+1])
        
        return {
            "points": optimized_points,
            "total_distance": total_distance
        }

    def chat_page(self):
        """Renderiza a página do chat"""
        if 'user_id' not in session:
            return redirect(url_for('chat/index.html'))
        return render_template('chat/index.html')
    
    def handle_chat(self):
        """Processa as mensagens do chat com foco em geolocalização e RAG"""
        try:
            data = request.get_json()
            user_query = data.get('message', '').strip()[:500]
            
            if not user_query:
                return jsonify({
                    "response": "Por favor, digite uma pergunta.", 
                    "places": [],
                    "itinerary": None,
                    "images": []
                })
            
            # Validação de entrada
            is_valid, error_msg = self._validate_input(user_query)
            if not is_valid:
                return jsonify({
                    "response": error_msg, 
                    "places": [],
                    "itinerary": None,
                    "images": []
                })
            
            # Identificar se o usuário quer criar um itinerário
            itinerary_request = any(word in user_query.lower() for word in ["itinerário", "roteiro", "sequência", "ordem", "visitar"])
            if itinerary_request:
                # Extrair locais mencionados
                location_entities = self._extract_location_entities(user_query)
                if not location_entities or len(location_entities) < 2:
                    return jsonify({
                        "response": "Por favor, mencione pelo menos dois locais para criar um itinerário.",
                        "places": [],
                        "itinerary": None,
                        "images": []
                    })
                
                # Obter coordenadas para cada local
                locations = []
                for entity in location_entities:
                    coords = self._get_precise_coordinates(entity)
                    location_details = self._get_location_details(*coords)
                    locations.append({
                        "name": entity,
                        "coords": coords,
                        "details": location_details
                    })
                
                # Gerar itinerário otimizado
                itinerary = self._generate_itinerary([loc["coords"] for loc in locations])
                
                # Formatando resposta
                response_lines = [
                    "### Itinerário Otimizado:",
                    f"Distância total estimada: {itinerary['total_distance']/1000:.2f} km",
                    "\n**Ordem recomendada de visitação:**"
                ]
                
                for i, point in enumerate(itinerary["points"]):
                    loc = next(loc for loc in locations if loc["coords"] == point)
                    response_lines.append(f"{i+1}. {loc['name']}")
                
                response_lines.append("\nDeseja que eu mostre esta rota no mapa?")
                
                return jsonify({
                    "response": "\n".join(response_lines),
                    "places": [loc["details"] for loc in locations],
                    "itinerary": {
                        "points": [{"lat": p[0], "lon": p[1]} for p in itinerary["points"]],
                        "total_distance": itinerary["total_distance"]
                    },
                    "images": []
                })
            
            # Busca contexto com RAG
            rag_context = self._rag_search(user_query)
            
            # Busca informações na web
            web_context = self._search_web(user_query)
            
            # Identifica entidades geográficas
            location_entities = self._extract_location_entities(user_query)
            
            # Obtém coordenadas
            target_coords = (-2.530731, -44.306396)  # Centro de São Luís
            if location_entities:
                target_coords = self._get_precise_coordinates(location_entities[0])
            
            # Obtém detalhes do local principal
            main_location = self._get_location_details(*target_coords)
            
            # Busca recomendações próximas
            nearby_places = self._get_local_recommendations(target_coords)
            
            # Busca imagens do local principal
            images = self._get_place_images(main_location["name"])
            
            # Construir prompt com contexto RAG e web
            prompt = (
                "Você é um guia turístico especializado em São Luís, Maranhão. "
                "Responda de forma detalhada, acolhedora e precisa sobre locais turísticos. "
                "Forneça informações históricas e culturais quando relevante. "
                "Se o usuário perguntar sobre rotas, forneça um plano de viagem com os pontos turísticos em ordem, "
                "estimativas de distância e tempo. Se perguntar sobre preços, forneça faixas de valores quando possível.\n\n"
                f"### Contexto do banco de dados local:\n{rag_context}\n\n"
                f"### Contexto da web:\n{web_context}\n\n"
                f"### Pergunta do turista:\n{user_query}\n\n"
                "Resposta completa (em português brasileiro):"
            )
            
            # Gera resposta com o modelo
            llm_response = self.llm.invoke(prompt)
            response_text = llm_response.content
            
            return jsonify({
                "response": response_text,
                "main_location": main_location,
                "nearby_places": nearby_places,
                "itinerary": None,
                "images": images
            })
            
        except Exception as e:
            logger.exception("Falha no processamento do chat")
            return jsonify({
                "response": "Desculpe, estou com dificuldades técnicas. Tente novamente mais tarde.",
                "main_location": {
                    "name": "São Luís, MA",
                    "address": "São Luís, Maranhão",
                    "type": "cidade",
                    "lat": -2.530731,
                    "lon": -44.306396
                },
                "nearby_places": [],
                "itinerary": None,
                "images": []
            })