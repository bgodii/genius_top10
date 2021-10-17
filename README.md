# Genius-Top10

### Objetivo
Aplicação para listar as 10 musicas mais populares de um determinado artista.

### Requisitos
 - Docker
 - Docker-Compose

### Execução
Para executar o projeto, primeiro temos que adicionar as variaveis de ambiente que serão consumidas pelo aplicação.
No arquivo `.env` temos as seguintes variaveis:
- GENIUS_AUTH_TOKEN: Variaves responsavel pela autenticação na API Genius
- AWS_ACCESS_KEY_ID: Chave de acesso aos serviços da Amazon
- AWS_SECRET_ACCESS_KEY: Chave para acesso aos serviços da Amazon
- REGION_NAME: Opcional, região onde está hospedado o DynamoDB na Amazon.

Após adicionar as variáveis de ambiente, na pasta raiz do projeto, executar o comando: `docker-compose up -d --build genius-top10`. Este comando irá subir o container da aplicação e também o container do `Redis`.

### Instruções da API
API esta exposta na porta `8080`, logo é acessavel a partir do endereço `localhost:8080/`. Ela possui apenas um `endpoint`.
`top10`: Neste endpoint podemos consultar as musicas mais populares de um determinado artista. Ela aceita dois parametros via `query string` sendo eles:
- artist: Parametro string obrigatorio, onde será usado para consultar nas apis externas o artista desejado, e assim retornar suas musicas mais populares.
- cache: Parametro bool opcional. Utilizado para utilizar os dados que estão em cache caso o mesmo exista. O não envio do parametro indica que será utilizado os dados em cache.

Exemplo de requisição:
`GET http://localhost:8080/top10?artist=michel%20telo&cache=false`

`
{
  "artist": "michel telo",
  "top_songs": {
    "1": "ai se eu te pego",
    "2": "michel teló - ai se eu te pego (english translation)",
    "3": "bara bará bere berê",
    "4": "ai se eu te pego (kojak version)",
    "5": "fugidinha",
    "6": "if i catch you",
    "7": "humilde residência",
    "8": "modão duído",
    "9": "pai, mãe",
    "10": "eu te amo e open bar"
  }
}
`

### Testes
A aplicação também possui alguns testes unitarios, para garantir o funcionamento de seus serviços, para executa-los utilize o comando: `docker container exec genius_top10 make tests`

### Tecnologias utilizadas
- [Python3](https://www.python.org/downloads/): Linguagem a qual a API foi escrita.
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) e [Flask_Restful](https://flask-restful.readthedocs.io/en/latest/): Frameworks Python para criação de Apis REST
- [pipenv](https://pypi.org/project/pipenv/): Gerenciador de pacotes do python 
- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/): Container para receber e executar a aplicação, dessa forma tornando mais facil execução por outros ambiente e adição de novas ferramentas.
- [DynamoDB](https://aws.amazon.com/pt/dynamodb/): Banco de dados não relacional dos serviços de cloud da AWS
- [Redis](https://redis.io/): Banco chave valor usado como banco de dados em memória cache


