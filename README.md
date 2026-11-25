# Cadastro de Professores (Flask)

Aplicação acadêmica com apenas duas rotas: `/` e `/professores`. Os módulos ainda não implementados exibem “Não disponível” na página inicial, sem criar rotas adicionais. Os templates existentes foram reaproveitados; nenhum template novo foi criado.

## Executar localmente

1. Crie um ambiente virtual e instale `requirements.txt`.
2. Defina `FLASK_CONFIG=development`.
3. Execute `flask --app flasky run` (ou use o arquivo `wsgi.py` como referência).

O banco SQLite `data-dev.sqlite`/`data.sqlite` é criado automaticamente.

## Publicar no PythonAnywhere

1. Envie o conteúdo deste projeto para sua conta (por exemplo, em `/home/SEU_USUARIO/flasky-main`).
2. No console Bash, crie/ative um virtualenv e instale `pip install -r requirements.txt`.
3. Em **Web > Add a new web app**, selecione Flask e o mesmo virtualenv.
4. No arquivo WSGI da configuração Web, importe `application` de `wsgi.py`, usando o caminho correto do projeto. Exemplo:

```python
import sys
project_home = '/home/SEU_USUARIO/flasky-main'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
from wsgi import application
```

5. Em **Web > Environment variables**, defina `SECRET_KEY` com um valor secreto forte e `FLASK_CONFIG=production`.
6. Confirme que o diretório do projeto permite escrita para o usuário da aplicação, pois o SQLite precisa gravar `data.sqlite`; então recarregue o site.

## Dados do aluno

Edite `app/main/views.py` e substitua `SEU NOME` e `SEU PRONTUÁRIO` pelos seus dados antes da entrega.
