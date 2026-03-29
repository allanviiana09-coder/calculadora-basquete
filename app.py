import streamlit as st

st.set_page_config(page_title="Calculadora Basquete Pro", page_icon="🏀")

st.title("🏀 Analisador Estratégico de Basquete")
st.markdown("---")

# Painel de Guia
with st.expander("📖 Guia de Estratégia e Confirmação"):
    st.write("1️⃣ **PRÉ-ANÁLISE (7-6 min):** Insira os dados e observe o ritmo.")
    st.write("2️⃣ **CONFIRMAÇÃO (5 min):** Valide a entrada neste exato momento.")
    st.write("3️⃣ **GATILHO:** Entre se Confiança > 90% e Margem > 3.0 pts.")

# Sidebar para dados fixos (Quartos)
st.sidebar.header("📊 Dados dos Quartos")
liga = st.sidebar.selectbox("Liga", ["NBA (48m)", "FIBA/NBB (40m)"])
t_total = 48 if "NBA" in liga else 40

p1 = st.sidebar.number_input("Pts Q1", value=0)
p2 = st.sidebar.number_input("Pts Q2", value=0)
p3 = st.sidebar.number_input("Pts Q3", value=0)

# Corpo Principal (Live)
col1, col2 = st.columns(2)
with col1:
    m_rest = st.number_input("Minutos que FALTAM", min_value=0, max_value=12, value=5)
with col2:
    s_rest = st.number_input("Segundos que FALTAM", min_value=0, max_value=59, value=0)

p4_atual = st.number_input("Pts no 4º Quarto (até agora)", value=0)
linha_base = st.number_input("Linha atual da Casa", value=200.0, step=0.5)

ctx = st.selectbox("Contexto do Jogo", ["Normal", "Acirrado (Clutch)", "Jogo Ganho (Lento)"])
bonus = st.radio("Times no Bônus?", ["Não", "Apenas Um", "Ambos"], horizontal=True)

# Cálculos
t_restante_q4 = m_rest + (s_rest / 60)
t_passado_q4 = (t_total / 4) - t_restante_q4
t_passado_total = (t_total * 0.75) + t_passado_q4
pts_atuais = p1 + p2 + p3 + p4_atual

# Lógica de Pesos
peso_ctx = {"Normal": 1.0, "Acirrado (Clutch)": 1.18, "Jogo Ganho (Lento)": 0.82}[ctx]
peso_bonus = {"Não": 1.0, "Apenas Um": 1.05, "Ambos": 1.10}[bonus]

ppm_123 = (p1 + p2 + p3) / (t_total * 0.75) if (p1+p2+p3) > 0 else 0
ppm_q4 = p4_atual / t_passado_q4 if t_passado_q4 > 0 else ppm_123
ppm_proj = ((ppm_q4 * 0.65) + (ppm_123 * 0.35)) * peso_ctx * peso_bonus
proj_final = pts_atuais + (ppm_proj * t_restante_q4)

# Resultados Visuais
st.markdown("---")
if 4.0 <= t_restante_q4 <= 6.0:
    st.success("🎯 MOMENTO DO GATILHO (CONFIRMAÇÃO)")
elif 6.0 < t_restante_q4 <= 8.5:
    st.info("✅ JANELA DE PRÉ-ANÁLISE")

st.subheader(f"Projeção Final Estimada: {proj_final:.1f} pts")

# Grade de Linhas
st.write("### 📈 Grade de 1 em 1 Ponto")
for l in [linha_base - 2, linha_base - 1, linha_base, linha_base + 1, linha_base + 2]:
    diff = proj_final - l
    conf = min(abs(diff) * 14 + 42, 99.9)
    cor = "green" if proj_final > l else "red"
    seta = "▲ OVER" if proj_final > l else "▼ UNDER"
    alerta = "🔥 OPORTUNIDADE ALTA" if conf >= 90 else ""
    
    st.markdown(f":{cor}[**{l:.1f}** | {seta} | Margem: {diff:>+4.1f} | Confiança: {conf:.1f}%] {alerta}")
