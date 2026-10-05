# Dashboard TAF FAB

Dashboard interativo **Streamlit** para calculo de pontuacao do Teste de Aptidao Fisica (TAF) da FAB 
(EEAR, EPCAR, QOCON, CFS), com graficos, simulacao de metas e exportacao **PDF/CSV**.

## Funcionalidades
- Calculo **oficial** baseado na IN 002/2023-DGP/FAB (todas as 5 provas, homem/mulher)
- **Radar chart** + barras horizontais + tabela detalhada
- **Simulador**: "e se eu melhorar X metros/reps/segundos?"
- **Metas automaticas**: mostra quanto precisa para media 60, 70, 80, 90
- **Exporta PDF profissional** (cabecalho FAB, tabela colorida, status APTO/INAPTO)
- **Exporta CSV** para planilha
- **Historico de sessao** com grafico de evolucao
- **Deploy gratis** no Streamlit Cloud / Railway / Render

## Stack
- Streamlit 1.37
- Plotly 5.22 (graficos interativos)
- Pandas 2.2
- fpdf2 (PDF leve, sem LaTeX)

## Configuracao Local

### 1. Clone e instale
```bash
git clone https://github.com/jvng16688/dashboard-taf-fab.git
cd dashboard-taf-fab
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Rode
```bash
streamlit run app.py
```
Abre em `http://localhost:8501`

## Deploy Gratis

### Streamlit Cloud (Mais facil)
1. Push para GitHub
2. Acesse share.streamlit.io -> login GitHub
3. "New app" -> repo `jvng16688/dashboard-taf-fab` -> branch `main` -> file `app.py`
4. Deploy URL publica: `https://dashboard-taf-fab-xxx.streamlit.app`

### Railway
1. New Project -> GitHub repo
2. Settings -> Variables: (nenhuma obrigatoria)
3. Deploy

### Render
1. New Web Service -> GitHub repo
2. Build: `pip install -r requirements.txt`
3. Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Deploy

## Estrutura dos Modulos

| Arquivo | Responsabilidade |
|---------|------------------|
| `taf_calculator.py` | **Core** — tabelas oficiais, lookup, calculo, metas |
| `pdf_export.py` | Gera PDF profissional com fpdf2 |
| `app.py` | Interface Streamlit + graficos Plotly |

## Licenca
MIT — Portfolio project para demonstrar habilidades Python/Streamlit/Plotly.