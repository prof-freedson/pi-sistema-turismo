from flask import request, flash, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename
from models.evento import Evento
from datetime import datetime
import os


class EventoController:

    def index(self):
        """Lista todos os eventos"""
        try:
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

    def create(self):
        """Exibe o formulário de criação de novo evento"""
        try:
            tipos = ['Show', 'Evento', 'Festival', 'Teatro', 'Exposição']
            return render_template('eventos/create.html', tipos=tipos)
        except Exception as e:
            flash(f'Erro ao carregar formulário: {str(e)}', 'error')
            return redirect(url_for('eventos'))

    def store(self):
        """Salva novo evento enviado pelo formulário"""
        try:
            data_inicio_raw = request.form.get('data_inicio')
            data_fim_raw = request.form.get('data_fim')
            horario_raw = request.form.get('horario')

            evento_data = {
                'nome_evento': request.form.get('nome_evento'),
                'tipo': request.form.get('tipo'),
                'descricao': request.form.get('descricao'),
                'data_inicio': datetime.strptime(data_inicio_raw, '%Y-%m-%d').date() if data_inicio_raw else None,
                'data_fim': datetime.strptime(data_fim_raw, '%Y-%m-%d').date() if data_fim_raw else None,
                'horario': datetime.strptime(horario_raw, '%H:%M').time() if horario_raw else None,
                'local': request.form.get('local'),
                'endereco': request.form.get('endereco'),
                'preco': float(request.form.get('preco', 0)),
                'capacidade': int(request.form.get('capacidade', 0)),
                'organizador': request.form.get('organizador'),
                'contato': request.form.get('contato'),
                'url_imagem': request.form.get('url_imagem')
            }

            if request.form.get('gratuito'):
                evento_data['preco'] = 0.0

            imagem = request.files.get('imagem_evento')
            if imagem and imagem.filename != '':
                ext = imagem.filename.rsplit('.', 1)[-1].lower()
                if ext in current_app.config['ALLOWED_EXTENSIONS']:
                    filename = secure_filename(imagem.filename)
                    caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    imagem.save(caminho)
                    evento_data['url_imagem'] = f"/{caminho.replace(os.path.sep, '/')}"
                else:
                    flash('Formato de imagem não permitido. Use PNG, JPG, JPEG ou GIF.', 'error')
                    return redirect(url_for('evento_create'))

            if not evento_data['nome_evento']:
                flash('Nome do evento é obrigatório.', 'error')
                return redirect(url_for('evento_create'))

            if evento_data['data_inicio'] and evento_data['data_fim']:
                if evento_data['data_inicio'] > evento_data['data_fim']:
                    flash('A data de início não pode ser posterior à data de fim.', 'error')
                    return redirect(url_for('evento_create'))

            result = Evento.create(evento_data)
            if result:
                flash('Evento criado com sucesso!', 'success')
                return redirect(url_for('eventos'))
            else:
                flash('Erro ao criar evento.', 'error')
                return redirect(url_for('evento_create'))

        except Exception as e:
            flash(f'Erro ao criar evento: {str(e)}', 'error')
            return redirect(url_for('evento_create'))

    def edit(self, evento_id):
        """Carrega dados do evento para edição"""
        try:
            evento = Evento.get_by_id(evento_id)
            if not evento:
                flash('Evento não encontrado.', 'error')
                return redirect(url_for('eventos'))

            tipos = ['Show', 'Evento', 'Festival', 'Teatro', 'Exposição']
            return render_template('eventos/edit.html', evento=evento, tipos=tipos)

        except Exception as e:
            flash(f'Erro ao carregar evento para edição: {str(e)}', 'error')
            return redirect(url_for('eventos'))

    def update(self, evento_id):
        """Atualiza um evento com suporte a upload de imagem"""
        try:
            data_inicio_raw = request.form.get('data_inicio')
            data_fim_raw = request.form.get('data_fim')
            horario_raw = request.form.get('horario')

            evento_data = {
                'nome_evento': request.form.get('nome_evento'),
                'tipo': request.form.get('tipo'),
                'descricao': request.form.get('descricao'),
                'data_inicio': datetime.strptime(data_inicio_raw, '%Y-%m-%d').date() if data_inicio_raw else None,
                'data_fim': datetime.strptime(data_fim_raw, '%Y-%m-%d').date() if data_fim_raw else None,
                'horario': datetime.strptime(horario_raw, '%H:%M').time() if horario_raw else None,
                'local': request.form.get('local'),
                'endereco': request.form.get('endereco'),
                'preco': float(request.form.get('preco', 0)),
                'capacidade': int(request.form.get('capacidade', 0)),
                'organizador': request.form.get('organizador'),
                'contato': request.form.get('contato'),
                'url_imagem': request.form.get('url_imagem')
            }

            if request.form.get('gratuito'):
                evento_data['preco'] = 0.0

            imagem = request.files.get('imagem_evento')
            if imagem and imagem.filename != '':
                ext = imagem.filename.rsplit('.', 1)[-1].lower()
                if ext in current_app.config['ALLOWED_EXTENSIONS']:
                    filename = secure_filename(imagem.filename)
                    caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    imagem.save(caminho)
                    evento_data['url_imagem'] = f"/{caminho.replace(os.path.sep, '/')}"
                else:
                    flash('Formato de imagem não permitido. Use PNG, JPG, JPEG ou GIF.', 'error')
                    return redirect(url_for('evento_edit', evento_id=evento_id))

            if not evento_data['nome_evento']:
                flash('Nome do evento é obrigatório.', 'error')
                return redirect(url_for('evento_edit', evento_id=evento_id))

            if evento_data['data_inicio'] and evento_data['data_fim']:
                if evento_data['data_inicio'] > evento_data['data_fim']:
                    flash('A data de início não pode ser posterior à data de fim.', 'error')
                    return redirect(url_for('evento_edit', evento_id=evento_id))

            result = Evento.update(evento_id, evento_data)
            if result:
                flash('Evento atualizado com sucesso!', 'success')
                return redirect(url_for('eventos'))
            else:
                flash('Erro ao atualizar evento.', 'error')
                return redirect(url_for('evento_edit', evento_id=evento_id))

        except Exception as e:
            flash(f'Erro ao atualizar evento: {str(e)}', 'error')
            return redirect(url_for('evento_edit', evento_id=evento_id))

    def show(self, evento_id):
        """Exibe os detalhes de um evento específico"""
        try:
            evento = Evento.get_by_id(evento_id)
            if not evento:
                flash("Evento não encontrado.", "error")
                return redirect(url_for("eventos"))
            return render_template("eventos/show.html", evento=evento)
        except Exception as e:
            flash(f"Erro ao carregar evento: {str(e)}", "error")
            return redirect(url_for("eventos"))
