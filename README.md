# wally-ips
Wally é uma aplicação baseada em IPS para mapa interativo e agregação de dados.

### Painel

O painel está na pasta Panel. Para o desenvolvimento foi utilizado um ambiente para que pudesse ser replicado facilmente. Ele foi exportado e encontra-se na pasta **env**. Portanto, para instalar as dependências, o Conda pode ser utilizado:

```
conda env create -f wally-panel-env.yml
```  

Além disso, na mesma pasta, os dados utilizados para a demonstração foram exportados e estão na pasta **wally-db**. Os dados de conexão com o banco devem ser modificados em app.py.

Para rodar a aplicação, basta rodar o arquivo app:

```
python app.py
```  
