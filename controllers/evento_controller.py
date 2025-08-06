from flask import request, flash, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename
from models.evento import Evento
from models.restaurante import Restaurante
from datetime import datetime
import os

class EventoController:

    # 🔹 Método para exibir a lista de eventos internos (admin/usuário)
    def index(self):
        try:
            eventos = Evento.get_all()
            return render_template("eventos/index.html", eventos=eventos)
        except Exception as e:
            flash(f"Erro ao carregar eventos: {str(e)}", "error")
            return render_template("eventos/index.html", eventos=[])

    # 🔹 Página pública que mostra eventos + restaurantes
    def index_visitante(self):
        try:
            eventos = Evento.get_all()
            restaurantes = Restaurante.get_all()
            return render_template("visitantes.html",
                                   eventos=eventos,
                                   restaurantes=restaurantes,
                                   esconder_menu=True)
        except Exception as e:
            flash(f'Erro ao carregar dados públicos: {str(e)}', 'error')
            return render_template("visitantes.html",
                                   eventos=[],
                                   restaurantes=[],
                                   esconder_menu=True)

    # 🔹 Página de criação de evento (GET)
    def create(self):
        tipos = ['Show', 'Evento', 'Festival', 'Teatro', 'Exposição']
        return render_template('eventos/create.html', tipos=tipos)

    # 🔹 Criação de evento (POST)
    def store(self):
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

    # 🔹 Página de edição de evento (GET)
    def edit(self, evento_id):
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

    # 🔹 Atualização de evento (POST)
    def update(self, evento_id):
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

    # 🔹 Exibição de evento específico
    def show(self, evento_id):
        try:
            evento = Evento.get_by_id(evento_id)
            if not evento:
                flash("Evento não encontrado.", "error")
                return redirect(url_for("eventos"))
            return render_template("eventos/show.html", evento=evento)
        except Exception as e:
            flash(f"Erro ao carregar evento: {str(e)}", "error")
            return redirect(url_for("eventos"))

    # 🔹 Deleção de evento
    def delete(self, evento_id):
        try:
            evento = Evento.get_by_id(evento_id)
            if not evento:
                flash("Evento não encontrado.", "error")
                return redirect(url_for("eventos"))

            Evento.delete(evento_id)
            flash("Evento deletado com sucesso!", "success")
            return redirect(url_for("eventos"))

        except Exception as e:
            flash(f"Erro ao deletar evento: {str(e)}", "error")
            return redirect(url_for("eventos"))
