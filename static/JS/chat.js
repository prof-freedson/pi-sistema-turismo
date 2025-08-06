document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('map-container').setView([-2.530731, -44.306396], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);
    
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const placesContainer = document.getElementById('places-container');
    const imagesContainer = document.getElementById('images-container');
    
    let markers = [];
    let routePolyline = null;
    
    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('alert', isUser ? 'alert-primary' : 'alert-secondary');
        msgDiv.innerHTML = `<strong>${isUser ? 'Você' : 'Assistente'}:</strong> ${text}`;
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    function updatePlaces(places) {
        placesContainer.innerHTML = '';
        if (!places || places.length === 0) {
            placesContainer.innerHTML = '<p class="text-muted">Nenhum local recomendado</p>';
            return;
        }
        
        places.forEach(place => {
            const card = document.createElement('div');
            card.className = 'card mb-2 location-card';
            card.innerHTML = `
                <div class="card-body">
                    <h6>${place.name}</h6>
                    <p class="small mb-1">${place.address}</p>
                    <p class="small text-muted">Tipo: ${place.type}</p>
                </div>
            `;
            
            const marker = L.marker([place.lat, place.lon]).addTo(map)
                .bindPopup(`<b>${place.name}</b><br>${place.address}`);
            markers.push(marker);
            
            card.addEventListener('click', () => {
                map.setView([place.lat, place.lon], 16);
                marker.openPopup();
            });
            
            placesContainer.appendChild(card);
        });
    }
    
    function updateImages(images) {
        imagesContainer.innerHTML = '';
        if (!images || images.length === 0) {
            imagesContainer.innerHTML = '<p class="text-muted">Nenhuma imagem disponível</p>';
            return;
        }
        
        images.forEach(imgUrl => {
            const img = document.createElement('img');
            img.src = imgUrl;
            img.className = 'img-fluid mb-2';
            img.style.maxHeight = '150px';
            imagesContainer.appendChild(img);
        });
    }
    
    function clearMarkers() {
        markers.forEach(marker => map.removeLayer(marker));
        markers = [];
        
        if (routePolyline) {
            map.removeLayer(routePolyline);
            routePolyline = null;
        }
    }
    
    function drawItinerary(points) {
        if (routePolyline) {
            map.removeLayer(routePolyline);
        }
        
        const latlngs = points.map(p => [p.lat, p.lon]);
        routePolyline = L.polyline(latlngs, {color: 'blue'}).addTo(map);
        map.fitBounds(latlngs);
    }
    
    sendBtn.addEventListener('click', function() {
        const message = userInput.value.trim();
        if (!message) return;
        
        addMessage(message, true);
        userInput.value = '';
        
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('alert', 'alert-warning');
        loadingDiv.innerHTML = '<strong>Assistente:</strong> Processando sua pergunta...';
        chatContainer.appendChild(loadingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        })
        .then(response => response.json())
        .then(data => {
            chatContainer.removeChild(loadingDiv);
            addMessage(data.response);
            
            clearMarkers();
            
            if (data.main_location) {
                const mainMarker = L.marker([
                    data.main_location.lat, 
                    data.main_location.lon
                ]).addTo(map)
                .bindPopup(`<b>${data.main_location.name}</b>`)
                .openPopup();
                
                markers.push(mainMarker);
                map.setView([data.main_location.lat, data.main_location.lon], 14);
                
                updatePlaces(data.nearby_places);
                updateImages(data.images);
            }
            
            if (data.itinerary) {
                drawItinerary(data.itinerary.points);
            }
        })
        .catch(error => {
            chatContainer.removeChild(loadingDiv);
            addMessage('Desculpe, ocorreu um erro. Tente novamente.');
            console.error('Erro:', error);
        });
    });
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendBtn.click();
    });
});