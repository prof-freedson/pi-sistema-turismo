from flask import request, flash, redirect, url_for, render_template, session
from models.usuario import Usuario
from models.administrador import Administrador

class AuthController:
    
    def login_form(self):
        """Exibe formulário de login"""
        return render_template('auth/login.html')
    
    def login(self):
        """Processa login"""
        try:
            email = request.form.get('email')
            senha = request.form.get('senha')
            tipo_usuario = request.form.get('tipo_usuario', 'usuario')
            
            if not email or not senha:
                flash('Email e senha são obrigatórios', 'error')
                return redirect(url_for('login_form'))
            
            # Verificar se é admin ou usuário
            if tipo_usuario == 'admin':
                user = Administrador.authenticate(email, senha)
                user_type = 'admin'
            else:
                user = Usuario.authenticate(email, senha)
                user_type = 'usuario'
            
            if user:
                session['user_id'] = user['id']
                session['user_name'] = user['nome']
                session['user_email'] = user['email']
                session['user_type'] = user_type
                flash(f'Bem-vindo, {user["nome"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Email ou senha incorretos', 'error')
                return redirect(url_for('login_form'))
                
        except Exception as e:
            flash(f'Erro ao fazer login: {str(e)}', 'error')
            return redirect(url_for('login_form'))
    
    def logout(self):
        """Faz logout"""
        session.clear()
        flash('Logout realizado com sucesso', 'success')
        return redirect(url_for('login_form'))
    
    def register_usuario_form(self):
        """Exibe formulário de cadastro de usuário"""
        return render_template('auth/register_usuario.html')
    
    def register_usuario(self):
        """Processa cadastro de usuário"""
        try:
            usuario_data = {
                'nome': request.form.get('nome'),
                'email': request.form.get('email'),
                'senha': request.form.get('senha')
            }
            
            # Validações
            if not usuario_data['nome'] or not usuario_data['email'] or not usuario_data['senha']:
                flash('Todos os campos são obrigatórios', 'error')
                return redirect(url_for('register_usuario_form'))
            
            # Verificar se email já existe
            if Usuario.email_exists(usuario_data['email']):
                flash('Este email já está cadastrado', 'error')
                return redirect(url_for('register_usuario_form'))
            
            result = Usuario.create(usuario_data)
            if result:
                flash('Usuário cadastrado com sucesso! Faça login para continuar.', 'success')
                return redirect(url_for('login_form'))
            else:
                flash('Erro ao cadastrar usuário', 'error')
                return redirect(url_for('register_usuario_form'))
                
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {str(e)}', 'error')
            return redirect(url_for('register_usuario_form'))
    
    def register_admin_form(self):
        """Exibe formulário de cadastro de administrador"""
        return render_template('auth/register_admin.html')
    
    def register_admin(self):
        """Processa cadastro de administrador"""
        try:
            admin_data = {
                'nome': request.form.get('nome'),
                'email': request.form.get('email'),
                'senha': request.form.get('senha')
            }
            
            # Validações
            if not admin_data['nome'] or not admin_data['email'] or not admin_data['senha']:
                flash('Todos os campos são obrigatórios', 'error')
                return redirect(url_for('register_admin_form'))
            
            # Verificar se email já existe
            if Administrador.email_exists(admin_data['email']):
                flash('Este email já está cadastrado', 'error')
                return redirect(url_for('register_admin_form'))
            
            result = Administrador.create(admin_data)
            if result:
                flash('Administrador cadastrado com sucesso! Faça login para continuar.', 'success')
                return redirect(url_for('login_form'))
            else:
                flash('Erro ao cadastrar administrador', 'error')
                return redirect(url_for('register_admin_form'))
                
        except Exception as e:
            flash(f'Erro ao cadastrar administrador: {str(e)}', 'error')
            return redirect(url_for('register_admin_form'))

