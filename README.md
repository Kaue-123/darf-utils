# DARF Utils

Utilitário de desktop que renomeia em lote as guias **DAS do Simples Nacional**
em PDF, lendo o próprio conteúdo do documento.

Cada arquivo é copiado para o diretório de saída com o nome padronizado:

```
12345678000199 - ACME Comércio de Peças LTDA - Janeiro-2024.pdf
   CNPJ                 Razão Social             Período de Apuração
```

O diretório de origem nunca é alterado: os PDFs são copiados, não movidos.

## Instalação

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

Selecione o diretório com as guias, o diretório de saída e clique em
**Processar PDF's**. Ao final, um resumo informa quantos arquivos foram
renomeados e quais foram ignorados, com o motivo de cada um.

## Arquitetura

O projeto segue uma separação MVC clássica: a *view* não conhece regra de
negócio, o *model* não conhece interface gráfica, e o *controller* é o único
ponto onde os dois se encontram.

```
darf_utils/
├── models/              # Domínio e regras de negócio
│   ├── darf.py          # Entidade Darf e a formação do nome do arquivo
│   ├── parser.py        # Texto do PDF -> Darf
│   ├── pdf_reader.py    # Adaptador do PyMuPDF (única dependência externa)
│   ├── renamer.py       # Caso de uso: renomear o lote e reportar o resultado
│   └── errors.py        # Erros do domínio
├── views/
│   └── main_window.py   # Janela Tkinter, apenas apresentação
├── controllers/
│   └── renamer_controller.py  # Valida a entrada, aciona o modelo, devolve o resumo
└── app.py               # Composição: instancia e conecta as três camadas
```

A leitura do PDF entra no caso de uso por injeção de dependência
(`TextExtractor`), o que mantém o domínio testável sem PyMuPDF instalado.

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

## Build do executável

```bash
pip install pyinstaller
pyinstaller darf.spec
```

O binário é gerado em `dist/`.
