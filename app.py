import streamlit as st
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Calculadora de Explosivos - Subterránea",
    page_icon="⛏️",
    layout="centered"
)

# --- FUNCIÓN DE CÁLCULO VOLUMÉTRICO ---
def calcular_kg_anfo_tiro(diametro_pulg, largo_m, taco_m, densidad_kg_m3=850):
    diametro_m = diametro_pulg * 0.0254
    largo_carga = largo_m - taco_m
    if largo_carga <= 0:
        return 0.0
    radio_m = diametro_m / 2
    volumen_m3 = math.pi * (radio_m ** 2) * largo_carga
    return volumen_m3 * densidad_kg_m3

# --- INTERFAZ VISUAL ---
st.title("⛏️ Calculadora de Carga de Explosivos")
st.caption("ANFO a granel y Emulsión FAMESA para Galerías de Transporte y Zanjas")

st.markdown("---")

# 1. Selección de Labor
col_labor, col_diam, col_largo = st.columns(3)

with col_labor:
    labor = st.selectbox(
        "Tipo de Labor",
        ["Galería de Transporte (GT)", "Zanja / Drawpoint", "Personalizado"]
    )

if labor == "Galería de Transporte (GT)":
    zapateras_default = 9
elif labor == "Zanja / Drawpoint":
    zapateras_default = 8
else:
    zapateras_default = 6

with col_diam:
    diametro_pulg = st.number_input("Diámetro (pulgadas)", value=1.75, step=0.25)

with col_largo:
    largo_tiro = st.number_input("Largo Tiro / Barra (m)", value=3.8, step=0.2)

st.markdown("### 💥 Distribución de la Malla de Perforación")

# 2. Carga de Zapateras (Emulsión FAMESA)
st.subheader("1. Zapateras (Agua / Humedad - Emulsión FAMESA)")
col_zap1, col_zap2 = st.columns(2)

with col_zap1:
    tiros_zapateras = st.number_input("Número de Zapateras", value=zapateras_default, step=1)

with col_zap2:
    pates_por_tiro_zap = st.number_input("Patés / Cartuchos por Zapatera", value=10, step=1)

# 3. Carga de Tiros Secos (ANFO)
st.subheader("2. Resto de la Malla (ANFO)")

col1, col2 = st.columns(2)
with col1:
    tiros_auxiliares = st.number_input("Tiros Auxiliares / Zapatilleros", value=22, step=1)
    tiros_cajas = st.number_input("Tiros de Cajas (Paredes)", value=10, step=1)

with col2:
    tiros_corona = st.number_input("Tiros de Corona (Techo)", value=8, step=1)
    tiros_ranura = st.number_input("Tiros de Rainura / Corte", value=6, step=1)

st.markdown("---")

# --- BOTÓN DE CÁLCULO Y RESULTADOS ---
if st.button("🚀 Calcular Carga de Disparo", type="primary", use_container_width=True):
    
    # Cálculo Emulsión
    total_pates_emulsion = tiros_zapateras * pates_por_tiro_zap
    
    # Cálculo ANFO (Densidad neumática promedio: 850 kg/m3)
    densidad_anfo = 850
    kg_aux = tiros_auxiliares * calcular_kg_anfo_tiro(diametro_pulg, largo_tiro, 0.7, densidad_anfo)
    kg_caj = tiros_cajas * calcular_kg_anfo_tiro(diametro_pulg, largo_tiro, 0.9, densidad_anfo)
    kg_cor = tiros_corona * calcular_kg_anfo_tiro(diametro_pulg, largo_tiro, 1.1, densidad_anfo)
    kg_ran = tiros_ranura * calcular_kg_anfo_tiro(diametro_pulg, largo_tiro, 0.6, densidad_anfo)

    anfo_teorico = kg_aux + kg_caj + kg_cor + kg_ran
    anfo_real = anfo_teorico * 1.12  # +12% de factor por compactación y margen operativo
    sacos_25kg = math.ceil(anfo_real / 25)
    
    tiros_totales = tiros_zapateras + tiros_auxiliares + tiros_cajas + tiros_corona + tiros_ranura

    # Presentación de Resultados
    st.header("📊 Resumen del Disparo")
    st.info(f"**Total de Tiros en la Malla:** {tiros_totales} tiros")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.metric(
            label="📦 Emulsión FAMESA (Zapateras)",
            value=f"{total_pates_emulsion} Patés",
            delta=f"{tiros_zapateras} tiros con emulsión"
        )
        
    with res_col2:
        st.metric(
            label="🌾 ANFO a Granel (Sacos 25 kg)",
            value=f"{sacos_25kg} Sacos",
            delta=f"{anfo_real:.1f} kg estimados"
        )
        