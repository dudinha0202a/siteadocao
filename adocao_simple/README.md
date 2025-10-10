# AdoCão (versão simplificada)

Estrutura reduzida para facilitar manutenção.
- `app.py`: app Flask + todas as rotas principais (público, auth e admin).
- `models.py`, `extensions.py`, `utils.py`: reutilizados do projeto original.
- `templates/` e `static/`: mantidos com o mesmo design.
- `config.py` e `requirements.txt`: copiados do original.
- `instance/adocao.sqlite`: banco sqlite (opcional).

## Como rodar
```bash
pip install -r requirements.txt
python app.py
```
