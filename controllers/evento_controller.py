from flask import request, flash, redirect, url_for, render_template
from models.evento import Evento
from datetime import datetime

class EventoController:
    
    def index(self):
        """Lista todos os eventos"""
        try:
            # Parâmetros de busca e filtros
            busca = request.args.get('busca', '')
            tipo_filtro = request.args.get('tipo', 'Todos')
            status_filtro = request.args.get('status', 'todos')
            
            if busca:
                eventos = Evento.search(busca)
            elif tipo_filtro != 'Todos':
                eventos = Evento.filter_by_type(tipo_filtro)
            elif status_filtro != 'todos':
                eventos = Evento.filter_by_status(status_filtro)
            else:
                eventos = Evento.get_all()
            
            # Tipos disponíveis para o filtro
            tipos = ['Show', 'Evento', 'Festival', 'Teatro', 'Exposição']
            
            return render_template('eventos/index.html', 
                                 eventos=eventos, 
                                 tipos=tipos,
                                 busca=busca,
                                 tipo_filtro=tipo_filtro,
                                 status_filtro=status_filtro)
        except Exception as e:
            flash(f'Erro ao carregar eventos: {str(e)}', 'error')
            return render_template('eventos/index.html', eventos=[])
    
    def show(self, evento_id):
        """Mostra um evento específico"""
        try:
            evento = Evento.get_by_id(evento_id)
            if not evento:
                flash('Evento não encontrado', 'error')
                return redirect(url_for('eventos'))
            
            return render_template('eventos/show.html', evento=evento)
        except Exception as e:
            flash(f'Erro ao carregar evento: {str(e)}', 'error')
            return redirect(url_for('eventos'))
    
    def create(self):
        """Exibe formulário de criação de evento"""
        tipos = ['Show', 'Evento', 'Festival', 'Teatro', 'Exposição']
        return render_template('eventos/create.html', tipos=tipos)
    
    def store(self):
        """Salva um novo evento"""
        try:
            evento_data = {
                'nome_evento': request.form.get('nome_evento'),
                'tipo': request.form.get('tipo'),
                'descricao': request.form.get('descricao'),
                'data_inicio': request.form.get('data_inicio'),
                'data_fim': request.form.get('data_fim'),
                'horario': request.form.get('horario'),
                'local': request.form.get('local'),
                'endereco': request.form.get('endereco'),
                'preco': float(request.form.get('preco', 0)),
                'capacidade': int(request.form.get('capacidade', 0)),
                'organizador': request.form.get('organizador'),
                'contato': request.form.get('contato'),
                'url_imagem': request.form.get('url_imagem')
            }
            
            # Validações básicas
            if not evento_data['nome_evento']:
                flash('Nome do evento é obrigatório', 'error')
                return redirect(url_for('evento_create'))
            
            if not evento_data['data_inicio'] or not evento_data['data_fim']:
                flash('Datas de início e fim são obrigatórias', 'error')
                return redirect(url_for('evento_create'))
            
            result = Evento.create(evento_data)
            if result:
                flash('Evento criado com sucesso!', 'success')
                return redirect(url_for('eventos'))
            else:
                flash('Erro ao criar evento', 'error')
                return redirect(url_for('evento_create'))
                
        except Exception as e:
            flash(f'Erro ao criar evento: {str(e)}', 'error')
            return redirect(url_for('evento_create'))
    
    def edit(self, evento_id):
        """Exibe formulário de edição de evento"""
        try:
            evento = Evento.get_by_id(evento_id)
            if not evento:
                flash('Evento não encontrado', 'error')
                return redirect(url_for('eventos'))
            
            tipos = ['Show', 'Evento', 'Festival', 'Teatro', 'Exposição']
            return render_template('eventos/edit.html', evento=evento, tipos=tipos)
        except Exception as e:
            flash(f'Erro ao carregar evento: {str(e)}', 'error')
            return redirect(url_for('eventos'))
    
    def update(self, evento_id):
        """Atualiza um evento"""
        try:
            evento_data = {
                'nome_evento': request.form.get('nome_evento'),
                'tipo': request.form.get('tipo'),
                'descricao': request.form.get('descricao'),
                'data_inicio': request.form.get('data_inicio'),
                'data_fim': request.form.get('data_fim'),
                'horario': request.form.get('horario'),
                'local': request.form.get('local'),
                'endereco': request.form.get('endereco'),
                'preco': float(request.form.get('preco', 0)),
                'capacidade': int(request.form.get('capacidade', 0)),
                'organizador': request.form.get('organizador'),
                'contato': request.form.get('contato'),
                'url_imagem': request.form.get('url_imagem')
            }
            
            # Validações básicas
            if not evento_data['nome_evento']:
                flash('Nome do evento é obrigatório', 'error')
                return redirect(url_for('evento_edit', evento_id=evento_id))
            
            result = Evento.update(evento_id, evento_data)
            if result:
                flash('Evento atualizado com sucesso!', 'success')
                return redirect(url_for('eventos'))
            else:
                flash('Erro ao atualizar evento', 'error')
                return redirect(url_for('evento_edit', evento_id=evento_id))
                
        except Exception as e:
            flash(f'Erro ao atualizar evento: {str(e)}', 'error')
            return redirect(url_for('evento_edit', evento_id=evento_id))
    
    def delete(self, evento_id):
        """Deleta um evento"""
        try:
            result = Evento.delete(evento_id)
            if result:
                flash('Evento deletado com sucesso!', 'success')
            else:
                flash('Erro ao deletar evento', 'error')
        except Exception as e:
            flash(f'Erro ao deletar evento: {str(e)}', 'error')
        
        return redirect(url_for('eventos'))

