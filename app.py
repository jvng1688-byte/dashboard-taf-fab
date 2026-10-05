"""
Dashboard TAF FAB - Streamlit
Interface web para calcular pontos TAF, visualizar evolucao e exportar PDF/CSV.
Deploy gratis no Streamlit Cloud / Railway / Render.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from taf_calculator import TAFResult, calculate_required_for_target, get_next_milestone
from pdf_export import generate_taf_pdf
import base64

st.set_page_config(page_title="Dashboard TAF FAB", page_icon="🇧🇷", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main-header { text-align: center; color: #003366; padding: 1rem 0; }
    .metric-card { background: #f0f4f8; padding: 1rem; border-radius: 8px; border-left: 4px solid #003366; }
    .status-apto { color: #009600; font-weight: bold; font-size: 1.5rem; }
    .status-inapto { color: #c80000; font-weight: bold; font-size: 1.5rem; }
</style>
""", unsafe_allow_html=True)

if "historico" not in st.session_state: st.session_state.historico = []

st.sidebar.markdown("# Dashboard TAF FAB")
st.sidebar.markdown("**Calculadora oficial baseada na IN 002/2023-DGP/FAB**"); st.sidebar.divider()
sexo = st.sidebar.radio("Sexo", ["M", "F"], format_func=lambda x: "Masculino" if x == "M" else "Feminino", horizontal=True)
idade = st.sidebar.number_input("Idade", min_value=17, max_value=45, value=18)
st.sidebar.markdown("### Performance Atual")
if sexo == "M":
    corrida = st.sidebar.slider("Corrida 12 min (metros)", 0, 3500, 2200, 50)
    flexao = st.sidebar.slider("Flexao de braco (reps)", 0, 55, 15)
    abdominal = st.sidebar.slider("Abdominal 1 min (reps)", 0, 60, 25)
    barra = st.sidebar.slider("Barra fixa (segundos)", 0, 65, 10)
else:
    corrida = st.sidebar.slider("Corrida 12 min (metros)", 0, 3000, 1800, 50)
    flexao = st.sidebar.slider("Flexao de braco (reps)", 0, 45, 8)
    abdominal = st.sidebar.slider("Abdominal 1 min (reps)", 0, 55, 20)
    barra = st.sidebar.slider("Barra fixa (repeticoes)", 0, 16, 0)
natacao = st.sidebar.slider("Natacao 50m livre (segundos)", 25.0, 100.0, 55.0, 0.5)
st.sidebar.divider()
btn_calcular = st.sidebar.button("CALCULAR TAF", type="primary", use_container_width=True)
btn_salvar = st.sidebar.button("Salvar no historico", use_container_width=True)
btn_limpar_hist = st.sidebar.button("Limpar historico", use_container_width=True)

result = TAFResult(sexo=sexo, idade=idade, corrida_metros=corrida, flexao_reps=flexao,
                   abdominal_reps=abdominal, barra_valor=barra, natacao_segundos=natacao)

st.markdown('<h1 class="main-header">Dashboard TAF FAB</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666;">EEAR | EPCAR | QOCON | CFS — Preparacao Fisica Baseada em Tabela Oficial</p>', unsafe_allow_html=True)
st.divider()

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1: st.metric("Corrida", f"{result.pts_corrida} pts", f"{result.corrida_metros:.0f} m")
with col2: st.metric("Flexao", f"{result.pts_flexao} pts", f"{result.flexao_reps} reps")
with col3: st.metric("Abdominal", f"{result.pts_abdominal} pts", f"{result.abdominal_reps} reps")
with col4:
    barra_label = f"{barra:.0f}s" if sexo == "M" else f"{int(barra)} reps"
    st.metric("Barra", f"{result.pts_barra} pts", barra_label)
with col5: st.metric("Natacao", f"{result.pts_natacao} pts", f"{result.natacao_segundos:.1f} s")
with col6:
    status_class = "status-apto" if result.status == "APTO" else "status-inapto"
    st.metric("MEDIA", f"{result.media}")
    st.markdown(f'<p class="{status_class}" style="text-align:center;">{result.status}</p>', unsafe_allow_html=True)
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Radar", "Barras", "Tabela", "Metas"])

with tab1:
    categorias = ["Corrida", "Flexao", "Abdominal", "Barra", "Natacao"]
    valores = [result.pts_corrida, result.pts_flexao, result.pts_abdominal, result.pts_barra, result.pts_natacao]
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=valores+[valores[0]], theta=categorias+[categorias[0]], fill='toself', name='Atual', line_color='#003366', fillcolor='rgba(0, 51, 102, 0.2)'))
    fig_radar.add_trace(go.Scatterpolar(r=[60]*6, theta=categorias+[categorias[0]], mode='lines', name='Minimo APTO (60)', line=dict(color='red', dash='dash')))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=450, title="Perfil de Pontuacao TAF")
    st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    df_barras = pd.DataFrame({"Prova": categorias, "Pontos": valores, "Minimo APTO": [40]*5, "Meta 60": [60]*5, "Meta 80": [80]*5})
    fig_bar = px.bar(df_barras, x="Pontos", y="Prova", orientation='h', color="Pontos", color_continuous_scale="Blues", text="Pontos", height=400)
    fig_bar.add_vline(x=40, line_dash="dash", line_color="red", annotation_text="Min/prova (40)")
    fig_bar.add_vline(x=60, line_dash="dash", line_color="green", annotation_text="Meta media (60)")
    fig_bar.update_layout(xaxis_range=[0, 105]); st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    df_table = pd.DataFrame({"Prova": categorias, "Performance": [f"{result.corrida_metros:.0f} m", f"{result.flexao_reps} reps", f"{result.abdominal_reps} reps", f"{barra:.0f} {'s' if sexo=='M' else 'reps'}", f"{result.natacao_segundos:.1f} s"], "Pontos": valores, "Status": ["OK" if v >= 60 else "ATENCAO" if v >= 40 else "BAIXO" for v in valores]})
    st.dataframe(df_table, use_container_width=True, hide_index=True)
    st.markdown(f"### **TOTAL: {result.total}/500  |  MEDIA: {result.media}/100**")
    if result.status == "APTO": st.success("APTO — Parabens! Voce atende aos criterios oficiais.")
    else: st.error("INAPTO — Continue treinando. Veja a aba 'Metas' para saber o que melhorar.")

with tab4:
    st.markdown("### Analise de Metas")
    milestone = get_next_milestone(result)
    if "target_media" in milestone:
        st.info(f"Proximo marco: Media {milestone['target_media']} — Faltam **{milestone['pontos_faltantes']:.0f} pontos** no total.")
        if "melhorias" in milestone and isinstance(milestone['melhorias'], dict):
            melhorias_df = []
            for prova, dados in milestone['melhorias'].items():
                if isinstance(dados, dict):
                    melhorias_df.append({"Prova": prova, "Pontos Atuais": dados['atual_pts'], "Pontos Necessarios": dados['necessario_pts'], "Ganho Necessario": dados['ganho_pts']})
            if melhorias_df: st.dataframe(pd.DataFrame(melhorias_df), use_container_width=True, hide_index=True)
    else: st.success(milestone.get("message", "Maximo atingido!"))
    st.divider(); st.markdown("### Simulador: O que acontece se eu melhorar...?")
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1: prova_sim = st.selectbox("Prova", categorias)
    with col_sim2:
        if prova_sim == "Corrida": novo_valor = st.slider("Nova performance (m)", 0, 3500, int(corrida), 50)
        elif prova_sim == "Flexao": novo_valor = st.slider("Novas reps", 0, 55, flexao)
        elif prova_sim == "Abdominal": novo_valor = st.slider("Novas reps", 0, 60, abdominal)
        elif prova_sim == "Barra":
            if sexo == "M": novo_valor = st.slider("Novos segundos", 0, 65, int(barra))
            else: novo_valor = st.slider("Novas reps", 0, 16, int(barra))
        else: novo_valor = st.slider("Novo tempo (s)", 25.0, 100.0, natacao, 0.5)
    kwargs = dict(corrida_metros=corrida, flexao_reps=flexao, abdominal_reps=abdominal, barra_valor=barra, natacao_segundos=natacao)
    idx = categorias.index(prova_sim)
    if idx == 0: kwargs["corrida_metros"] = novo_valor
    elif idx == 1: kwargs["flexao_reps"] = novo_valor
    elif idx == 2: kwargs["abdominal_reps"] = novo_valor
    elif idx == 3: kwargs["barra_valor"] = novo_valor
    else: kwargs["natacao_segundos"] = novo_valor
    sim_result = TAFResult(sexo=sexo, idade=idade, **kwargs)
    delta_media = sim_result.media - result.media; delta_total = sim_result.total - result.total
    if delta_media > 0: st.success(f"Media: {result.media} -> {sim_result.media} (+{delta_media:.1f}) | Total: {result.total} -> {sim_result.total} (+{delta_total})")
    elif delta_media < 0: st.error(f"Media: {result.media} -> {sim_result.media} ({delta_media:.1f}) | Total: {result.total} -> {sim_result.total} ({delta_total})")
    else: st.info("Sem mudanca na media.")

st.divider()
col_exp1, col_exp2, col_exp3 = st.columns(3)
with col_exp1:
    if st.button("Gerar PDF", use_container_width=True):
        pdf_file = generate_taf_pdf(result)
        with open(pdf_file, "rb") as f: b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="taf_resultado_{datetime.now().strftime("%Y%m%d")}.pdf">Baixar PDF</a>'
        st.markdown(href, unsafe_allow_html=True); st.success("PDF gerado! Clique no link acima.")
with col_exp2:
    if st.button("Exportar CSV", use_container_width=True):
        df_export = pd.DataFrame([result.to_dict()]); csv = df_export.to_csv(index=False, encoding="utf-8-sig")
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:text/csv;base64,{b64}" download="taf_{datetime.now().strftime("%Y%m%d")}.csv">Baixar CSV</a>'
        st.markdown(href, unsafe_allow_html=True); st.success("CSV pronto!")
with col_exp3:
    if btn_salvar:
        entry = result.to_dict(); entry["timestamp"] = datetime.now().isoformat()
        st.session_state.historico.append(entry); st.success("Salvo no historico da sessao!")

if st.session_state.historico:
    st.divider(); st.markdown("### Historico da Sessao")
    df_hist = pd.DataFrame(st.session_state.historico)
    cols_show = ["timestamp", "Sexo", "Idade", "MEDIA", "TOTAL", "STATUS"]
    st.dataframe(df_hist[cols_show], use_container_width=True, hide_index=True)
    if len(df_hist) > 1:
        fig_hist = px.line(df_hist, x="timestamp", y="MEDIA", markers=True, title="Evolucao da Media TAF", labels={"timestamp": "Data/Hora", "MEDIA": "Media"})
        fig_hist.add_hline(y=60, line_dash="dash", line_color="green", annotation_text="APTO (60)")
        st.plotly_chart(fig_hist, use_container_width=True)
if btn_limpar_hist: st.session_state.historico = []; st.rerun()

st.divider()
st.markdown("""
<div style="text-align:center; color:#888; font-size:0.85rem;">
    <p>Dashboard TAF FAB | Base: IN 002/2023-DGP/FAB | Portfolio: <a href="https://github.com/jvng16688" target="_blank">github.com/jvng16688</a></p>
    <p>Desenvolvido por Arthur Mota — Python, Streamlit, Plotly, fpdf2 | Deploy: Streamlit Cloud / Railway / Render</p>
</div>
""", unsafe_allow_html=True)