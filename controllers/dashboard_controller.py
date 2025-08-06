from flask import render_template
from models.evento import Evento
from models.restaurante import Restaurante

class DashboardController:
    
    def index(self):
        """Exibe o dashboard principal"""
        try:
            # Estatísticas gerais
            total_eventos = Evento.get_count()
            total_restaurantes = Restaurante.get_count()
            eventos_hoje = Evento.get_eventos_hoje()
            locais_unicos = Evento.get_locais_unicos()
            
            # Próximos eventos
            proximos_eventos = Evento.get_proximos_eventos(5)
            
            return render_template('dashboard/index.html',
                                 total_eventos=total_eventos,
                                 total_restaurantes=total_restaurantes,
                                 eventos_hoje=eventos_hoje,
                                 locais_unicos=locais_unicos,
                                 proximos_eventos=proximos_eventos)
        except Exception as e:
            # Em caso de erro, retorna valores padrão
            return render_template('dashboard/index.html',
                                 total_eventos=0,
                                 total_restaurantes=0,
                                 eventos_hoje=0,
                                 locais_unicos=0,
                                 proximos_eventos=[])

