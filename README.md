Desafio: Data Science Agro
==============================

Organização
------------

```
root
├── data
│   ├── interim   -> Dados intermediários  
│   ├── processed -> Dados finais para modelagem  
│   └── raw       -> Fonte de dados iniciais e IMUTÁVEIS
|
├── docs -> Documentações de código, projeto, metadados e afins  
|
├── Makefile -> Makefiles para automação e registro de comandos manuais  
|
├── models -> Arquivos de modelos treinados, escalonadores e afins  
|
├── notebooks -> Jupyter notebooks. 
|
├── reports -> Saídas dos estágios finais do pipeline, como métricas e gráficos.
│   ├── features -> Salvar lista de features e seu feature importance
│   ├── figures -> Salvar gráfico de predição, matriz de confusão...
│   └── metrics -> Salvar métricas de avaliação de modelos, como acurácia, MAE, MSE...
|
├── README.md  
│  
└── src -> Armazena .py de códigos base  
    │  
    ├── \_\_init\_\_.py -> Torna src um módulo python  
    │  
    └── utils -> Armazena código base  
        │  
        ├── data -> Funções/classes para processamento de dados  
        │  
        ├── features -> Funções/classes para engenharia de features  
        │  
        ├── models -> Funções/classes para treinamento e inferência de modelos  
        │  
        ├── evaluation -> Funções/classes para avaliação de modelos, dados, artefatos, etc.  
        │  
        └── visualization -> Funções/classes para visualização  
```