import os
import logging
from flask import request, flash, redirect, url_for, render_template, current_app as app
from werkzeug.utils import secure_filename
from models.restaurante import Restaurante
from config.database import execute_query

# Configurar logging
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class RestauranteController:
    
    def index(self):
        """Lista todos os restaurantes com filtros opcionais"""
        try:
            busca = request.args.get('busca', '').strip()
            culinaria_filtro = request.args.get('culinaria', 'Todas')
            preco_filtro = request.args.get('preco', 'Todas')
            
            # Consulta segura com parâmetros
            query_params = []
            query = "SELECT * FROM restaurantes WHERE 1=1"
            
            if busca:
                query += " AND (nome_restaurante LIKE %s OR descricao LIKE %s OR endereco LIKE %s)"
                query_params.extend([f"%{busca}%", f"%{busca}%", f"%{busca}%"])
            
            if culinaria_filtro != 'Todas':
                query += " AND tipo_culinaria = %s"
                query_params.append(culinaria_filtro)
            
            if preco_filtro != 'Todas':
                # Mapeia descrição para símbolos
                preco_map = {
                    '$ - Economico': '$',
                    '$$ - Moderado': '$$',
                    '$$$ - Caro': '$$$',
                    '$$$$ - Muito Caro': '$$$$'
                }
                if preco_filtro in preco_map:
                    query += " AND faixa_preco = %s"
                    query_params.append(preco_map[preco_filtro])
            
            query += " ORDER BY nome_restaurante ASC"
            restaurantes = execute_query(query, tuple(query_params))
            
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
            logger.error(f"Erro ao carregar restaurantes: {str(e)}", exc_info=True)
            flash('Erro interno ao carregar restaurantes. Por favor, tente novamente.', 'error')
            return render_template('restaurantes/index.html', restaurantes=[])
    
    def show(self, restaurante_id):
        """Mostra detalhes de um restaurante específico"""
        try:
            # Validação de ID
            if not restaurante_id or not restaurante_id.isdigit():
                flash('ID de restaurante inválido', 'error')
                return redirect(url_for('restaurantes'))
            
            restaurante = Restaurante.get_by_id(int(restaurante_id))
            if not restaurante:
                flash('Restaurante não encontrado', 'error')
                return redirect(url_for('restaurantes'))
            
            return render_template('restaurantes/show.html', restaurante=restaurante)
            
        except Exception as e:
            logger.error(f"Erro ao carregar restaurante {restaurante_id}: {str(e)}", exc_info=True)
            flash('Erro interno ao carregar detalhes do restaurante', 'error')
            return redirect(url_for('restaurantes'))
    
    def create(self):
        """Exibe o formulário de criação de restaurante"""
        try:
            tipos_culinaria = ['Brasileira', 'Maranhense', 'Italiana', 'Japonesa', 'Mexicana', 'Francesa']
            faixas_preco = ['$ - Economico', '$$ - Moderado', '$$$ - Caro', '$$$$ - Muito Caro']
            return render_template('restaurantes/create.html', 
                                   tipos_culinaria=tipos_culinaria,
                                   faixas_preco=faixas_preco)
        except Exception as e:
            logger.error(f"Erro ao carregar formulário de criação: {str(e)}", exc_info=True)
            flash('Erro interno ao carregar formulário', 'error')
            return redirect(url_for('restaurantes'))
    
    def store(self):
        """Processa a criação de um novo restaurante"""
        try:
            # Coleta e valida dados do formulário
            nome = request.form.get('nome_restaurante', '').strip()
            tipo_culinaria = request.form.get('tipo_culinaria')
            endereco = request.form.get('endereco', '').strip()
            bairro = request.form.get('bairro', '').strip()
            telefone = request.form.get('telefone', '').strip()
            capacidade = request.form.get('capacidade', '0')
            
            # Validações básicas
            errors = []
            if not nome:
                errors.append('Nome do restaurante é obrigatório')
            if not tipo_culinaria or tipo_culinaria == 'Selecione':
                errors.append('Tipo de culinária é obrigatório')
            if not endereco:
                errors.append('Endereço é obrigatório')
            if not bairro:
                errors.append('Bairro é obrigatório')
            
            # Valida capacidade
            try:
                capacidade = int(capacidade)
                if capacidade < 0:
                    errors.append('Capacidade deve ser um número positivo')
            except ValueError:
                errors.append('Capacidade deve ser um número válido')
            
            if errors:
                for error in errors:
                    flash(error, 'error')
                return redirect(url_for('restaurante_create'))
            
            # Prepara dados para inserção
            restaurante_data = {
                'nome_restaurante': nome,
                'tipo_culinaria': tipo_culinaria,
                'descricao': request.form.get('descricao', '').strip(),
                'endereco': endereco,
                'bairro': bairro,
                'telefone': telefone,
                'horario_funcionamento': request.form.get('horario_funcionamento', '').strip(),
                'faixa_preco': request.form.get('faixa_preco'),
                'capacidade': capacidade,
                'url_imagem': '',
                'aceita_reservas': 'aceita_reservas' in request.form,
                'tem_delivery': 'tem_delivery' in request.form,
                'tem_estacionamento': 'tem_estacionamento' in request.form
            }

            # Processa upload de imagem
            imagem = request.files.get('imagem')
            if imagem and imagem.filename:
                if allowed_file(imagem.filename):
                    filename = secure_filename(imagem.filename)
                    upload_dir = app.config['UPLOAD_FOLDER']
                    
                    # Garante que o diretório de upload existe
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    caminho = os.path.join(upload_dir, filename)
                    imagem.save(caminho)
                    
                    # Verifica se o arquivo foi salvo
                    if not os.path.exists(caminho):
                        logger.warning(f"Falha ao salvar imagem: {caminho}")
                        flash('Erro ao salvar imagem do restaurante', 'warning')
                    else:
                        restaurante_data['url_imagem'] = f"/static/img/{filename}"
                else:
                    flash('Tipo de arquivo não permitido. Use apenas imagens (PNG, JPG, JPEG)', 'error')
                    return redirect(url_for('restaurante_create'))
            else:
                restaurante_data['url_imagem'] = '/static/default.jpg'

            # Cria o restaurante no banco de dados
            result = Restaurante.create(restaurante_data)
            if result:
                flash('Restaurante criado com sucesso!', 'success')
                return redirect(url_for('restaurantes'))
            else:
                flash('Erro ao criar restaurante no banco de dados', 'error')
                return redirect(url_for('restaurante_create'))

        except Exception as e:
            logger.error(f"Erro ao criar restaurante: {str(e)}", exc_info=True)
            flash('Erro interno ao criar restaurante. Por favor, tente novamente.', 'error')
            return redirect(url_for('restaurante_create'))
    
    def edit(self, restaurante_id):
        """Exibe o formulário de edição de restaurante"""
        try:
            # Validação de ID
            if not restaurante_id or not restaurante_id.isdigit():
                flash('ID de restaurante inválido', 'error')
                return redirect(url_for('restaurantes'))
            
            restaurante = Restaurante.get_by_id(int(restaurante_id))
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
            logger.error(f"Erro ao carregar formulário de edição: {str(e)}", exc_info=True)
            flash('Erro interno ao carregar formulário de edição', 'error')
            return redirect(url_for('restaurantes'))
    
    def update(self, restaurante_id):
        """Processa a atualização de um restaurante"""
        try:
            # Validação de ID
            if not restaurante_id or not restaurante_id.isdigit():
                flash('ID de restaurante inválido', 'error')
                return redirect(url_for('restaurantes'))
            
            restaurante_id = int(restaurante_id)
            restaurante_existente = Restaurante.get_by_id(restaurante_id)
            if not restaurante_existente:
                flash('Restaurante não encontrado', 'error')
                return redirect(url_for('restaurantes'))
            
            # Coleta e valida dados do formulário
            nome = request.form.get('nome_restaurante', '').strip()
            tipo_culinaria = request.form.get('tipo_culinaria')
            endereco = request.form.get('endereco', '').strip()
            bairro = request.form.get('bairro', '').strip()
            telefone = request.form.get('telefone', '').strip()
            capacidade = request.form.get('capacidade', '0')
            
            # Validações básicas
            errors = []
            if not nome:
                errors.append('Nome do restaurante é obrigatório')
            if not tipo_culinaria or tipo_culinaria == 'Selecione':
                errors.append('Tipo de culinária é obrigatório')
            if not endereco:
                errors.append('Endereço é obrigatório')
            if not bairro:
                errors.append('Bairro é obrigatório')
            
            # Valida capacidade
            try:
                capacidade = int(capacidade)
                if capacidade < 0:
                    errors.append('Capacidade deve ser um número positivo')
            except ValueError:
                errors.append('Capacidade deve ser um número válido')
            
            if errors:
                for error in errors:
                    flash(error, 'error')
                return redirect(url_for('restaurante_edit', restaurante_id=restaurante_id))
            
            # Prepara dados para atualização
            restaurante_data = {
                'nome_restaurante': nome,
                'tipo_culinaria': tipo_culinaria,
                'descricao': request.form.get('descricao', '').strip(),
                'endereco': endereco,
                'bairro': bairro,
                'telefone': telefone,
                'horario_funcionamento': request.form.get('horario_funcionamento', '').strip(),
                'faixa_preco': request.form.get('faixa_preco'),
                'capacidade': capacidade,
                'aceita_reservas': 'aceita_reservas' in request.form,
                'tem_delivery': 'tem_delivery' in request.form,
                'tem_estacionamento': 'tem_estacionamento' in request.form
            }

            # Processa upload de imagem
            imagem = request.files.get('imagem')
            if imagem and imagem.filename:
                if allowed_file(imagem.filename):
                    filename = secure_filename(imagem.filename)
                    upload_dir = app.config['UPLOAD_FOLDER']
                    
                    # Garante que o diretório de upload existe
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    caminho = os.path.join(upload_dir, filename)
                    imagem.save(caminho)
                    
                    # Verifica se o arquivo foi salvo
                    if os.path.exists(caminho):
                        restaurante_data['url_imagem'] = f"/static/img/{filename}"
                        
                        # Remove imagem antiga se não for a padrão
                        if restaurante_existente['url_imagem'] and not restaurante_existente['url_imagem'].endswith('default.jpg'):
                            try:
                                old_path = os.path.join(app.root_path, restaurante_existente['url_imagem'].lstrip('/'))
                                if os.path.exists(old_path):
                                    os.remove(old_path)
                            except Exception as e:
                                logger.warning(f"Erro ao remover imagem antiga: {str(e)}")
                    else:
                        logger.warning(f"Falha ao salvar imagem: {caminho}")
                        flash('Erro ao salvar nova imagem do restaurante', 'warning')
                        restaurante_data['url_imagem'] = restaurante_existente['url_imagem']
                else:
                    flash('Tipo de arquivo não permitido. Use apenas imagens (PNG, JPG, JPEG)', 'error')
                    return redirect(url_for('restaurante_edit', restaurante_id=restaurante_id))
            else:
                restaurante_data['url_imagem'] = restaurante_existente['url_imagem']

            # Atualiza o restaurante no banco de dados
            result = Restaurante.update(restaurante_id, restaurante_data)
            if result:
                flash('Restaurante atualizado com sucesso!', 'success')
                return redirect(url_for('restaurantes'))
            else:
                flash('Erro ao atualizar restaurante no banco de dados', 'error')
                return redirect(url_for('restaurante_edit', restaurante_id=restaurante_id))

        except Exception as e:
            logger.error(f"Erro ao atualizar restaurante {restaurante_id}: {str(e)}", exc_info=True)
            flash('Erro interno ao atualizar restaurante. Por favor, tente novamente.', 'error')
            return redirect(url_for('restaurante_edit', restaurante_id=restaurante_id))
    
    def delete(self, restaurante_id):
        """Exclui um restaurante"""
        try:
            # Validação de ID
            if not restaurante_id or not restaurante_id.isdigit():
                flash('ID de restaurante inválido', 'error')
                return redirect(url_for('restaurantes'))
            
            restaurante_id = int(restaurante_id)
            restaurante = Restaurante.get_by_id(restaurante_id)
            if not restaurante:
                flash('Restaurante não encontrado', 'error')
                return redirect(url_for('restaurantes'))
            
            # Remove imagem associada se não for a padrão
            if restaurante['url_imagem'] and not restaurante['url_imagem'].endswith('default.jpg'):
                try:
                    img_path = os.path.join(app.root_path, restaurante['url_imagem'].lstrip('/'))
                    if os.path.exists(img_path):
                        os.remove(img_path)
                except Exception as e:
                    logger.warning(f"Erro ao remover imagem: {str(e)}")
            
            # Exclui do banco de dados
            result = Restaurante.delete(restaurante_id)
            if result:
                flash('Restaurante deletado com sucesso!', 'success')
            else:
                flash('Erro ao deletar restaurante', 'error')
                
        except Exception as e:
            logger.error(f"Erro ao deletar restaurante {restaurante_id}: {str(e)}", exc_info=True)
            flash('Erro interno ao deletar restaurante', 'error')
        
        return redirect(url_for('restaurantes'))