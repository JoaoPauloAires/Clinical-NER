# Clinical-NER
Este repositório contém os códigos referentes às primeiras atividades do projeto da AWS.
Nele, temos dois scripts; um que pré-processa dados orindos de conjuntos de dados existentes e (2) um que realiza a anotação de entidades nomeadas combinando dois modelos pré-treinados.

Para executar os scripts é necessário obter acesso e a pelo menos um dos dois conjuntos de dados utilizados, chamado [2014 - Deidentification & Heart Disease](https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/).
Além disso, recomendamos criar um ambiente para instalar as bibliotecas utilizadas.

```
pip install -r requirements.txt
```

O comando para executar a anotação e avaliação dos anotadores é:

```
python connect_models.py
```

Para mais informações, contactar: João Paulo Aires (joao.souza91@edu.pucrs.br) e Maurício Magnaguagno (mauricio.magnaguagno@acad.pucrs.br)