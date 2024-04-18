# API Correlation

Este projeto faz parte da Disciplina **Desenvolvimento Full Stack Básico** da pós graduação em Engenharia de Software da PUC-RIO.

O objetivo é criar uma aplicação no padrão MVC composta de API e. um front-end.

A aplicação escolhida para este projeto é o Correlation. Uma ferramenta útil para correlação de IDs entre diferentes bases de dados.

Grandes empresas possuem diversos desafios para gerenciar seus dados master, pois muitas vezes temos mais de uma aplicação gerenciando um domínio de informação. Uma forma de resolver este problema é fazer a correlação entre as entidades dessas aplicações em um sistema externo, como é o caso do **Correlation** . Uma vez feita esta correlação podemos consultar a base e buscar as informações corretamente.


## Como executar
Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

 É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Para criação de ambiente virtual, execute o seguinte comando:

```
python3 -m venv nome_do ambiente_virtual
```
Para ativar o ambiente virtual execute o seguinte comando:
```
source env/bin/activate
```
O comando a seguir instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.
```
(env)$ pip install -r requirements.txt
```
Após a criação do ambiente virtual e instalar os arquivos/bibliotecas de requirements.txt, basta executar a API com o seguinte comando:
```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução. Você será redirecionado para Swagger, onde terá acesso às documentações das APIs.

## Como funciona o Back end

O Back end é composto por um banco de dados Sqlite3 com um tabela chamada **correlacao**. Ela guarda todas as correlações e os grupos.
Existe uma etapa de normalização do atributo grupo, transformando todos os caracteres em maiúsculos e colocando separadores para os espaços. Desta forma evitaremos que um grupo de memso nome seja duplicado por conta das diferentes formas de escrita.
Para operações de leitura e escrita no banco foram criadas rotas, que estão escritas no arquivo principal do código (app.py).
foram criadas as seguintes rotas:

-  **get correlacoes**: Retorna uma representação da listagem de correlações;
- **get correlacao**: Faz a busca por uma correlação a partir do ID de correlação.
- **get correlacoes/grupo**: Faz a busca pelas correlações a partir de um grupo.
- **get correlacoes/sistema_origem**: Faz a busca pelas correlações a partir de um sistema de origem.
- **get correlacoes/sistema_destino**: Faz a busca pelas correlações a partir de um grupo.
- **post correlacao**: Adiciona uma nova correlacao no banco de dados.
- **delete correlacao**: Exclui uma correlação a partir do ID de correlação.
- **delete correlacao del_full**: Exclui uma correlação a partir dos atributos da correlacao.

## Melhoria Contínua  
  
Este trabalho é um MVP de pós-graduação. O objetivo principal aqui é aplicar os conhecimentos adquiridos no módulo de desenvolvimento full stack básico, em que foram tratados os temas de Programação Orientada a Objetos (POO), utilizando a linguagem python como base, Bancos de Dados e tópicos de desenvolvimento.

Alguns pontos foram identificados mas não foram tratados neste projetos. Segue proposta de melhorias para o correlation:

- Página de login.
- Página de Admin para gestão de acessos e perfis.
- Divisão da tabela nas tabelas de itens de correlação (sistema / entidade / id) e indicação se os itens são relativos à origem ou ao destino. Desta forma podemos habilitar o envio dos itens de maneira separada, e a correlação pode ser feita via front-end. 
- Criação da tabela Grupo para melhorar o tratamento dos grupos e realizar levantamentos diversos a partir da entidade grupo. 

## Sobre o autor 

O autor deste projeto é Wellington Melo (Ton Melo), Global MBA, engenheiro eletricista com especialização em engenharia de automação. No momento da criação deste projeto atuo como especialista de arquitetura de tecnologia na Globo e estou buscando conhecimento mais profundo em arquitetura e desenvolvimento de sistemas de TI.