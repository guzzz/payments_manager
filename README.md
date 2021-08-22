**Sistema baseado em arquitetura EDA**

- Sistema que permite o cadastro de pessoas, contas e transações.

---

# PAYMENTS MANAGER SYSTEM

As funcionalidades principais do sistema são:

1. Criação de usuários. Os inputs da chamada de criar usuários são: name, cpf, birth_date.
2. Criação de uma conta. Os inputs da chamada de criar conta são: balance, max_daily_withdraw, active, type, person.
3. Bloquear uma conta. 
4. Consultar o saldo de uma determinada conta.
5. Realizar uma transação de crédito em uma conta.
6. Realizar uma transação de débito em uma conta.
7. Ter acesso ao extrato de uma conta.

Obs.: Além destas, algumas outras funcionalidades foram inclusas, como: ativar uma conta; exibir detalhes da conta, de pessoas, das transações...

---

## Particularidades

A fim de criar um sistema "loosely coupled", busquei criar uma arquitetura orientada a eventos (EDA). 

O sistema é composto por:

1. API Python (DRF) + MySQL.
2. API Python (Flask) + MySQL.
3. Broker RabbitMQ.
4. O sistema foi feito utilizando Docker.

Separação:

1. Django:
Na API em Django, o foco foi para chamadas de leitura e filtros. Há escritas, porém de baixa intensidade.
2. A parte do Flask utilizei para as transações.

---

## Swagger

A API **Django** está utilizando o Swagger como ferramenta de documentação.

* Nesse projeto, o root está redirecionando para a documentação do swagger, que pode ser acessada em http://localhost:8000/

---

## Endpoints DJANGO

1. **(GET)** **_"/accounts/"_** - *Chamada que lista todas as contas do sistema.*
2. **(POST)** **_"/accounts/"_** - *Chamada para criar uma conta no sistema.*
3. **(GET)** **_"/accounts/{id}/"_** - *Retorna uma conta específica.*
4. **(GET)** **_"/accounts/{id}/activate/"_** - *Ativa uma conta.*
5. **(POST)** **_"/accounts/{id}/balance/"_** - *Retorna o saldo de uma conta.*
6. **(GET)** **_"/accounts/{id}/inactivate/"_** - *Inativa uma conta.*
7. **(GET)** **_"/extract/{account_id}/"_** - *Retorna o extrato de uma conta.*
8. **(GET)** **_"/persons/"_** - *Retorna todas as pessoas cadastradas.*
9. **(POST)** **_"/persons/"_** - *Registra uma pessoa (usuário).*
10. **(GET)** **_"/persons/{id}/"_** - *Retorna os detalhes de uma pessoa específica.*

_Obs._: Nos endpoints 4 e 6, abri mão do "patch" para tornar mais fácil a utilização da ativação e inativação.


#### Extratos por período

Alguns filtros foram implementados no endpoint: **(GET)** **_"/extract/{account_id}/"_**

Filtro por uma data específica ou por intervalos de datas:

_fomato da data: 2021-01-01_

* created
* created_before
* created_after 

_É possível utilizar esses filtros dentro do **Swagger UI**._

---

## Endpoints FLASK

1. **(GET)** **_"/"_** - *Chamada que dá um alou!.*
2. **(POST)** **_"/api/accounts/{account_id}/debit/"_** - *Chamada que debita um valor de uma conta.*
3. **(POST)** **_"/api/accounts/{account_id}/credit/"_** - *Chamada que credita um valor de uma conta.*

_Obs. 1_: Está rodando em: http://localhost:8001/
_Obs. 2_: Foi inserido um "/api/" nos endpoints para evitar confusão com o Django.


#### Body das chamadas

1. Os dois **POST** exigem o mesmo body. Porém, nos dois casos o campo "created" é **opcional**. Caso não seja enviado esse atributo, o created levará em consideração o horário atual.
2. Essa chamada só aceita valores maiores que zero. Em chamadas de débito, o sistema levará em consideração o endpoint para lidar com valores positivos ou negativos.
3. O campo "value" aceita valores decimais com mais casas decimais, porém sempre irá arredondar para duas casas decimais.

```
{
    "value": 0.01,
    "created": "2021-01-01 10:00:00"
}
```

---

## Makefile

Foi criado um _Makefile_ tanto para o **Django** quanto para o **Flask**. Segue abaixo alguns comandos:

* **_make setup_**: Coomando para setar a configuração inicial dos proejtos.
* **_make start_**: Sobe os containers dos projetos.
* **_make stop_**: Para os containers dos projetos.
* **_make tests_**: Rodas os testes dos projetos. Explicações sobre os testes no final do arquivo.
* **_make clean_**: Limpa os containers, imagens, volumes e networks. Para utilizar esse comando, é recomendável dar uma olhada no _Makefile_ primeiro, para não correr o risco de limpar outras entidades do seu ambiente que possuam os mesmos nomes que eu utilizo nesse projeto.

---

## Rodar localmente


1. Garantir que se tenha o Docker e o Docker-compose instalados.
2. Em uma aba do terminal, entrar no diretório "payments_manager_django".
3. Em outra aba do terminal, entrar no diretório "payments_manager_flask".
4. Dentro dos diretórios payments_manager_django e payments_manager_flask, utilizar como exemplo os arquivos .env-example e gerar os respectivos .env para cada projeto. Para setar algumas variáveis, é recomendado utilizar https://djecrety.ir e https://www.cloudamqp.com
5. Na primeira vez que rodar o projeto (e apenas na primeira) o comando _make setup_ deverá ser utilizado para iniciar a configuração inicial dos projetos. Este comando deverá ser rodado tanto na aba do Django quanto na aba do Flask.
6. A partir daí, em cada aba deverá ser rodado o comando _make start_ para iniciar o projeto. Para encerrar os dois projetos, há o comando _make stop_ .

* O Django roda em: http://localhost:8000/
* O Flask roda em: http://localhost:8001/

---

## Pontos a serem melhorados

1. Reorganizar a parte do Flask. Estudar e implementar uma estrutura mais organizada nessa parte do projeto.
2. Documentação da api do Flask.
3. Arquivos de configuração para ambientes diferentes, simulando produção e testing.
4. Utilização do coverage para analisar a abrangência dos testes no projeto.

---

## Tests

==> Os testes automatizados foram realizados, **porém**, ficaram de ser feitos ajustes para garantir que os testes não impactem no funcionamento do ambiente de "produção". O comando **_make tests_** atualmente é responsável por rodar os testes e em seguida resetar todo o ambiente.

Há 26 testes no sistema. 16 deles no Django, 10 no Flask.

1. [Django] Dois testes unitários no app persons.
2. [Django] Quatro testes de integração no app persons.
3. [Django] Quatro testes unitários no app accounts.
4. [Django] Seis testes de integração no app accounts.
5. [Flask] Dois testes unitários.
6. [Flask] Oito testes de integração.

_Obs._: No Django, os testes unitários e de integração foram divididos em arquivos separados e agrupados no diretório "test" de cada app.

---

## Requisitos

* **DOCKER-COMPOSE**: 1.28.5
* **DOCKER**: 20.10.05

