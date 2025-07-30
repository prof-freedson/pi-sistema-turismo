# Sistema de Ajuda ao Turista

## Sobre o projeto / Motivação
Escrever aqui

## Linguagens usadas
Escrever aqui

## 🛠️ Ferramentas
Escrever aqui

## Como usar
1. Instalar o Python. Acesse o link aqui:

### Configuração das variáveis de ambiente
1. Renomeie o arquivo `.env.example` na pasta raiz para `.env`
2. Acrescente os valores nas variáveis a seguir:
```
HOST = nome (podendo ser localhost) ou endereço do seu servidor de banco de dados (podendo ser 127.0.0.1)
USER = nome do usuário do banco de dados (podendo ser root ou outro nome)     
PASSWORD = senha do usuário do banco de dados  
DATABASE = nome do banco a ser manipulado
```

### Instalação das dependências
1. Abra o terminal na pasta raiz do projeto
2. Execute o seguinte comando para instalar as dependências:
```
pip install -r requirements.txt
```
3. Caso seja incluído um novo pacote no `requirements.txt`, execute o comando novamente para instalar as novas dependências.
4. Caso algum pacote for instalado e eles não estiver listado no `requirements.txt`, atualize o arquivo com o comando:
```
pip freeze > requirements.txt
```
5. Caso ocorra algum erro de instalação, verifique se o Python e o pip estão instalados corretamente.

### Configuração do banco de dados
Use, de preferência, o SGBD MySQL, para o uso do script no arquivo `banco.sql`

##### **OBS:** primeiramente, use a sua ferramenta de SGBD MySQL (podendo ser o MySQL Workbench) para a criação do banco de dados com a script a seguir:

```sql
CREATE DATABASE encantos_db;
```

## Créditos
Escrever aqui
