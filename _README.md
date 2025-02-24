# Shape's Hard Skill Test - Machine Learning Engineer

## Descrição do Projeto

Este projeto é uma solução para o desafio de habilidades técnicas da Shape para engenheiros de Machine Learning. O objetivo é refatorar o script `job_test_challenge.py` em um código mais modularizado, implementar boas práticas, escrever documentação adequada e torná-lo mais adequado para um lançamento de produto. A solução deve ser capaz de lidar com grandes volumes de dados, como tabelas de gigabytes em um data lake.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:
shape/ 
├── artifacts/ 
│ ├── model.pkl 
│ └── pipeline.jsonc 
├── data/ 
│ └── dataset.parquet 
├── logs/ 
│ └── metrics.json 
├── src/ │ 
├── config.py 
│ ├── database/ 
│ │ ├── __init__.py 
│ │ ├── config.py 
│ │ ├── json.py 
│ │ └── postgres.py 
│ ├── engine/ 
│ │ ├── __init__.py 
│ │ └── spark_engine.py 
│ ├── exceptions.py 
│ ├── loader/ 
│ │ ├── __init__.py 
│ │ └── load.py 
│ ├── logger/ 
│ │ ├── __init__.py 
│ │ ├── logger.py 
│ │ └── schema.py 
│ ├── main.py 
│ ├── pipeline/ 
│ │ ├── __init__.py 
│ │ ├── builder.py 
│ │ ├── pipeline.py 
│ │ ├── steps/ 
│ │ │ ├── __init__.py 
│ │ │ ├── schemas.py 
│ │ │ ├── sklearn.py 
│ │ │ └── sparkml.py 
│ │ └── strategies/ 
│ │ ├── __init__.py 
│ │ ├── schemas.py 
│ │ ├── sklearn_pipeline.py 
│ │ └── sparkml_pipeline.py 
│ ├── settings.py 
│ ├── traceability/ 
│ │ ├── __init__.py 
│ │ ├── schema.py 
│ │ ├── services/ 
│ │ │ ├── __init__.py 
│ │ │ ├── dvc.py 
│ │ │ ├── mlflow.py 
│ │ │ ├── weights_biases.py 
│ │ └── traceability_creator.py 
│ │ └── traceability_recorder.py 
│ └── utils.py 
├── tests/ 
│ └── __init__.py 
├── .gitignore 
├── CHALLENGE.md
├── README.md  
├── LICENSE 
├── Pipfile 
└── setup.py

## Configuração do Ambiente

### Requisitos

- Python 3.13
- Pipenv

### Instalação

1. Clone o repositório:

```sh
git clone https://github.com/yourusername/shape.git
cd shape

2. Instale as dependências:

pipenv install
pipenv install --dev

3 . ative o ambiente virtual

pipenv shell

3. uso

Estrutura do codigo


main.py: Ponto de entrada principal do projeto.
pipeline: Contém a lógica do pipeline, incluindo estratégias e etapas e processamento de dados pelo sklearn, inicie a implementacao do sparkML, mas nao foi concluida.
traceability: Implementa a rastreabilidade usando diferentes serviços por hora temos o MLflow, mas existe possibilidade de implementar DVC e weights & biases
logger: Implementa o sistema de logging usando Kafka como producer e futuramente podemos implementar um consumer para armazenamento de logs, exemplo elastic.
database: Contém a lógica para salvar dados no PostgreSQL e em arquivos JSON local.
engine: Configura o Spark para processamento de dados em larga escala, tentei implementar tambem a logica de sparkML para melhor aproveitamento de recursos, mas devido a o deadline alguns bugs ainda existem, como a serializacao do sparkml nao aceitar um obj VectorAssembler.
loader: Carrega os dados e o modelo de forma escalavel e simples.
utils.py: Contém funções utilitárias.

Claro! Aqui está um exemplo de `README.md` para o seu projeto:

```md
# Shape's Hard Skill Test - Machine Learning Engineer

## Descrição do Projeto

Este projeto é uma solução para o desafio de habilidades técnicas da Shape para engenheiros de Machine Learning. O objetivo é refatorar o script `job_test_challenge.py` em um código mais modularizado, implementar boas práticas, escrever documentação adequada e torná-lo mais adequado para um lançamento de produto. A solução deve ser capaz de lidar com grandes volumes de dados, como tabelas de gigabytes em um data lake.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
shape/
├── artifacts/
│   ├── model.pkl
│   └── pipeline.jsonc
├── data/
│   └── dataset.parquet
├── logs/
│   └── metrics.json
├── src/
│   ├── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── json.py
│   │   └── postgres.py
│   ├── engine/
│   │   ├── __init__.py
│   │   └── spark_engine.py
│   ├── exceptions.py
│   ├── loader/
│   │   ├── __init__.py
│   │   └── load.py
│   ├── logger/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── schema.py
│   ├── main.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   ├── pipeline.py
│   │   ├── steps/
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py
│   │   │   ├── sklearn.py
│   │   │   └── sparkml.py (not fished)
│   │   └── strategies/
│   │       ├── __init__.py
│   │       ├── schemas.py
│   │       ├── sklearn_pipeline.py
│   │       └── sparkml_pipeline.py
│   ├── settings.py
│   ├── traceability/
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── dvc.py
│   │   │   ├── mlflow.py
│   │   │   ├── weights_biases.py
│   │   └── traceability_creator.py
│   │   └── traceability_recorder.py
│   └── utils.py
├── tests/
│   └── __init__.py
│   └── test_main.py (not fished)
├── .gitignore
├── CHALLENGE.md
├── LICENSE
├── Pipfile
└── setup.py
```

## Configuração do Ambiente

### Requisitos

- Python 3.13
- Pipenv

### Instalação

1. Clone o repositório:

```sh
git clone https://github.com/yourusername/shape.git
cd shape
```

2. Instale as dependências:

```sh
pipenv install
pipenv install --dev
```

3. Ative o ambiente virtual:

```sh
pipenv shell
```

## Uso

### Executando o Pipeline

Para executar o pipeline, utilize o comando:

```sh
python src/main.py
```

### Estrutura de Código

- main.py: Ponto de entrada principal do projeto.
- pipeline: Contém a lógica do pipeline, incluindo estratégias e etapas.
- traceability: Implementa a rastreabilidade usando diferentes serviços como MLflow.
- logger: Implementa o sistema de logging usando Kafka.
- database: Contém a lógica para salvar dados no PostgreSQL e em arquivos JSON.
- engine: Configura o Spark.
- loader: Carrega os dados e o modelo.
- utils.py: Contém funções utilitárias.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça um push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.

## Licença

Este projeto está licenciado sob a Licença Apache 2.0 - veja o arquivo LICENSE para mais detalhes.

## Contato

Carlos Eduardo Soares - [cadu_gold@hotmail.com](mailto:cadu_gold@hotmail.com)

Link do Projeto: [https://github.com/ceddard/shape/tree/main](https://github.com/ceddard/shape/tree/main)
```

Sinta-se à vontade para ajustar o conteúdo conforme necessário.


Estrutura do `main.py`
O arquivo main.py é o ponto de entrada principal do seu projeto. Ele é responsável por orquestrar a execução do pipeline de processamento de dados e machine learning.
Configuração do Logger:

    Configuração do Logger:
    Configura o logger para registrar informações durante a execução do pipeline.
    
    Inicialização do Spark:
    Utiliza a classe SparkEngine para obter uma sessão do Spark, que é usada para processamento de dados em larga escala.
    
    Carregamento dos Dados:
    Utiliza a classe DataLoader para carregar os dados do arquivo dataset.parquet.
    
    Criação do Pipeline:
    Utiliza a classe PipelineBuilder para construir o pipeline de processamento de dados e machine learning.

    Execução do Pipeline:
    Ajusta o modelo (fit) aos dados carregados e gera previsões (transform).
    
    Salvamento do Modelo e das Previsões:
    Utiliza o DataLoader para salvar as previsões e o modelo treinado em arquivos.
    
    Criação da Rastreabilidade:
    Utiliza a classe TraceabilityCreator para criar registros de rastreabilidade do modelo, dados e previsões.
    
    Execução do Script:
A função main é chamada quando o script é executado diretamente. Futuramente ela pode ser trigada por um pipeline personalizado, que armazene um template em yml, e seja executao pelo jenkins, ou por uma trigger mais simples, como o caso de um airflow ou job no control programado.

pipeline` contém a lógica mais importante do pipeline e machine learning:

1. **pipeline.py**:
    - Define a classe `PipelineHandler`, que gerencia o carregamento de dados, a criação do pipeline e a transformação dos dados.
    - Utiliza a classe `Load` para carregar os dados e o modelo.
    - Utiliza a classe `PipelineBuilder` para construir o pipeline com base nas especificações fornecidas.
    - Processa os dados e aplica transformações usando o pipeline.
    - Gera previsões e calcula métricas.

2. **builder.py**:
    - Define a classe `PipelineBuilder`, que lê as especificações do pipeline de um arquivo JSON e cria uma estratégia de pipeline (`SklearnPipelineStrategy` ou `SparkMLPipelineStrategy`) com base no framework especificado (scikit-learn ou SparkML).

3. **strategies/**:
    - Contém as estratégias de pipeline para diferentes frameworks.
    - **schemas.py**: Define a classe abstrata `PipelineStrategy`, que serve como base para as estratégias de pipeline.
    - **sklearn_pipeline.py**: Implementa a estratégia de pipeline para scikit-learn.
    - **sparkml_pipeline.py**: Implementa a estratégia de pipeline para SparkML (nao finalizado devido ao deadline).

4. **steps/**:
    - Contém as etapas do pipeline para diferentes frameworks.
    - **schemas.py**: Define a classe abstrata `StepStrategy`, que serve como base para as estratégias de etapas.
    - **sklearn.py**: Implementa as etapas do pipeline para scikit-learn, como `ReduceDimStrategy`, `QTransfStrategy`, `PolyFeatureStrategy` e `StdScalerStrategy`.
    - **sparkml.py**: Implementa as etapas do pipeline para SparkML, como `ReduceDimStrategy`, `QTransfStrategy`, `PolyFeatureStrategy` e `StdScalerStrategy`.

Esses arquivos trabalham juntos para criar um pipeline de processamento de dados e machine learning que pode ser configurado e executado de forma flexível, utilizando diferentes frameworks e estratégias.


Python 3.13: Linguagem de programação principal.
Pandas: Biblioteca para manipulação e análise de dados.
NumPy: Biblioteca para computação numérica.
    ambas foram pouco utilizadas neste projeto, para trazer mais escalabilidade. Ambas nao desempenham tao bem em bigdata, pandas nao foi projetado para isso e numpy nao tem paralelismo, talves o DASK poderia ter sido mais aproveitado, como alternativa.
MLflow: Plataforma para gerenciar o ciclo de vida de machine learning.
PySpark: Interface para Apache Spark em Python.
Scikit-learn: Biblioteca para machine learning, futuramente pode ser implementado tambem sparkML.
Kafka: Sistema de mensagens distribuído usado para logging.
PostgreSQL: Banco de dados relacional.
Pipenv: Gerenciador de ambientes virtuais e dependências para Python.

porque tanto codigo?
se a vida
nao e programada
e nem tem logica

