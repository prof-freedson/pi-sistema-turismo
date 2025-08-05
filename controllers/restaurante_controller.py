import os
from flask import request, flash, redirect, url_for, render_template, current_app as app
from werkzeug.utils import secure_filename
from models.restaurante import Restaurante

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class RestauranteController:

    def listar_publicos(self):
        """Retorna uma lista simples de restaurantes para exibição pública"""
        try:
            restaurantes = Restaurante.get_all()
            return restaurantes
        except Exception as e:
            flash(f'Erro ao carregar restaurantes públicos: {str(e)}', 'error')
            return []

    def index(self):
        try:
            busca = request.args.get('busca', '')
            culinaria_filtro = request.args.get('culinaria', 'Todas')
            preco_filtro = request.args.get('preco', 'Todas')
            
            if busca:
                restaurantes = Restaurante.search(busca)
            elif culinaria_filtro != 'Todas':
                restaurantes = Restaurante.filter_by_culinaria(culinaria_filtro)
            elif preco_filtro != 'Todas':
                restaurantes = Restaurante.filter_by_preco(preco_filtro)
            else:
                restaurantes = Restaurante.get_all()
            
            tipos_culinaria = ['Brasileira', 'Maranhense', 'Italiana', 'Japonesa', 'Mexicana', 'Francesa']
            faixas_preco = ['$ - Economico', '$$ - Moderado', '$$$ - Caro', '$$$$ - Muito Caro']
            
            return render_template('restaurantes/index.html', 
                                   restaurantes=restaurantes,
                                   tipos_culinaria=tipos_culinaria,
                                   faixas_preco=faixas_preco,
                                   busca=busca,
                                   culinaria_filtro=culinaria_filtro,
                                   preco_filtro=preco_filtro)
        except Exception as e:
            flash(f'Erro ao carregar restaurantes: {str(e)}', 'error')
            return render_template('restaurantes/index.html', restaurantes=[])

    def show(self, restaurante_id):
        try:
            restaurante = Restaurante.get_by_id(restaurante_id)
            if not restaurante:
                flash('Restaurante não encontrado', 'error')
                return redirect(url_for('restaurantes'))
            return render_template('restaurantes/show.html', restaurante=restaurante)
        except Exception as e:
            flash(f'Erro ao carregar restaurante: {str(e)}', 'error')
            return redirect(url_for('restaurantes'))

    def create(self):
        tipos_culinaria = ['Brasileira', 'Maranhense', 'Italiana', 'Japonesa', 'Mexicana', 'Francesa']
        faixas_preco = ['$ - Economico', '$$ - Moderado', '$$$ - Caro', '$$$$ - Muito Caro']
        return render_template('restaurantes/create.html', 
                               tipos_culinaria=tipos_culinaria,
                               faixas_preco=faixas_preco)

    def store(self):
        try:
            restaurante_data = {
                'nome_restaurante': request.form.get('nome_restaurante'),
                'tipo_culinaria': request.form.get('tipo_culinaria'),
                'descricao': request.form.get('descricao'),
                'endereco': request.form.get('endereco'),
                'bairro': request.form.get('bairro'),
                'telefone': request.form.get('telefone'),
                'horario_funcionamento': request.form.get('horario_funcionamento'),
                'faixa_preco': request.form.get('faixa_preco'),
                'capacidade': int(request.form.get('capacidade', 0)),
                'url_imagem': '',
                'aceita_reservas': 'aceita_reservas' in request.form,
                'tem_delivery': 'tem_delivery' in request.form,
                'tem_estacionamento': 'tem_estacionamento' in request.form
            }

            imagem = request.files.get('imagem')
            if imagem and allowed_file(imagem.filename):
                filename = secure_filename(imagem.filename)
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagem.save(caminho)
                restaurante_data['url_imagem'] = '/' + os.path.join('static', 'img', filename).replace('\\', '/')
            else:
                restaurante_data['url_imagem'] = '/static/default.jpg'

            if not restaurante_data['nome_restaurante']:
                flash('Nome do restaurante é obrigatório', 'error')
                return redirect(url_for('restaurante_create'))

            if not restaurante_data['endereco']:
                flash('Endereço é obrigatório', 'error')
                return redirect(url_for('restaurante_create'))

            result = Restaurante.create(restaurante_data)
            if result:
                flash('Restaurante criado com sucesso!', 'success')
                return redirect(url_for('restaurantes'))
            else:
                flash('Erro ao criar restaurante', 'error')
                return redirect(url_for('restaurante_create'))

        except Exception as e:
            flash(f'Erro ao criar restaurante: {str(e)}', 'error')
            return redirect(url_for('restaurante_create'))

    def edit(self, restaurante_id):
        try:
            restaurante = Restaurante.get_by_id(restaurante_id)
            if not restaurante:
                flash('Restaurante não encontrado', 'error')
                return redirect(url_for('restaurantes'))

            tipos_culinaria = ['Brasileira', 'Maranhense', 'Italiana', 'Japonesa', 'Mexicana', 'Francesa']
            faixas_preco = ['$ - Economico', '$$ - Moderado', '$$$ - Caro', '$$$$ - Muito Caro']
            return render_template('restaurantes/edit.html', 
                                   restaurante=restaurante,
                                   tipos_culinaria=tipos_culinaria,
                                   faixas_preco=faixas_preco)
        except Exception as e:
            flash(f'Erro ao carregar restaurante: {str(e)}', 'error')
            return redirect(url_for('restaurantes'))

    def update(self, restaurante_id):
        try:
            restaurante_data = {
                'nome_restaurante': request.form.get('nome_restaurante'),
                'tipo_culinaria': request.form.get('tipo_culinaria'),
                'descricao': request.form.get('descricao'),
                'endereco': request.form.get('endereco'),
                'bairro': request.form.get('bairro'),
                'telefone': request.form.get('telefone'),
                'horario_funcionamento': request.form.get('horario_funcionamento'),
                'faixa_preco': request.form.get('faixa_preco'),
                'capacidade': int(request.form.get('capacidade', 0)),
                'url_imagem': '',
                'aceita_reservas': 'aceita_reservas' in request.form,
                'tem_delivery': 'tem_delivery' in request.form,
                'tem_estacionamento': 'tem_estacionamento' in request.form
            }

            imagem = request.files.get('imagem')
            if imagem and allowed_file(imagem.filename):
                filename = secure_filename(imagem.filename)
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagem.save(caminho)
                restaurante_data['url_imagem'] = '/' + os.path.join('static', 'img', filename).replace('\\', '/')
            else:
                restaurante_data['url_imagem'] = Restaurante.get_by_id(restaurante_id).url_imagem

            if not restaurante_data['nome_restaurante']:
                flash('Nome do restaurante é obrigatório', 'error')
                return redirect(url_for('restaurante_edit', restaurante_id=restaurante_id))

            result = Restaurante.update(restaurante_id, restaurante_data)
            if result:
                flash('Restaurante atualizado com sucesso!', 'success')
                return redirect(url_for('restaurantes'))
            else:
                flash('Erro ao atualizar restaurante', 'error')
                return redirect(url_for('restaurante_edit', restaurante_id=restaurante_id))

        except Exception as e:
            flash(f'Erro ao atualizar restaurante: {str(e)}', 'error')
            return redirect(url_for('restaurante_edit', restaurante_id=restaurante_id))

    def delete(self, restaurante_id):
        try:
            result = Restaurante.delete(restaurante_id)
            if result:
                flash('Restaurante deletado com sucesso!', 'success')
            else:
                flash('Erro ao deletar restaurante', 'error')
        except Exception as e:
            flash(f'Erro ao deletar restaurante: {str(e)}', 'error')

        return redirect(url_for('restaurantes'))
