

# app.py
# --------------------------------------------------
# 🎁 GiftBox – App navideña en Streamlit
# Pestañas: Personal y Resumen anual (sin guardar ni descargar)
# Incluye: Regalo “Feliz Navidad 2025” con globos al abrir
# --------------------------------------------------
import streamlit as st
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# ---------- Configuración general ----------
st.set_page_config(
    page_title="🎁 GiftBox – Tu app navideña",
    page_icon="🎁",
    layout="wide"
)

# ---------- Estilos navideños (fondo claro + caja regalo) ----------
CSS_CLARO = """
<style>
body, .stApp {
  background: linear-gradient(180deg, #fdf6e3 0%, #fefefe 60%, #eaeaea 100%);
}
h1, h2, h3 {
  color: #6d4c41 !important;
}
.st-card {
  background: rgba(255,255,255,0.90);
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.10);
}

/* Caja de regalo */
.gift-box {
  position: relative;
  margin: 20px auto;
  width: 340px;
  height: 220px;
  background: #ff7043; /* naranja cálido */
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

/* Tapa */
.gift-box::before {
  content: "";
  position: absolute;
  top: -40px;
  left: 0;
  width: 340px;
  height: 60px;
  background: #f4511e;
  border-radius: 12px 12px 0 0;
}

/* Cinta vertical */
.ribbon-vert {
  position: absolute;
  top: -40px;
  left: 155px;
  width: 30px;
  height: 320px;
  background: #ffd54f;
  border-radius: 8px;
}

/* Cinta horizontal */
.ribbon-hori {
  position: absolute;
  top: 80px;
  left: 0;
  width: 340px;
  height: 30px;
  background: #ffd54f;
  border-radius: 8px;
}

/* Etiqueta colgante */
.tag {
  position: absolute;
  top: -20px;
  right: -10px;
  width: 140px;
  height: 60px;
  background: #fffde7;
  border: 2px dashed #ff7043;
  border-radius: 8px;
  transform: rotate(10deg);
  color: #ff7043;
  font-weight: 700;
  display:flex;
  align-items:center;
  justify-content:center;
}

.gift-message {
  text-align: center;
  font-weight: 700;
  color: #6d4c41;
  padding-top: 6px;
}
</style>
"""
st.markdown(CSS_CLARO, unsafe_allow_html=True)

# ---------- Estado inicial (solo memoria en sesión) ----------
if "habitos" not in st.session_state:
    st.session_state.habitos = []
if "journal" not in st.session_state:
    st.session_state.journal = []
if "metas" not in st.session_state:
    st.session_state.metas = []
if "regalo_abierto" not in st.session_state:
    st.session_state.regalo_abierto = False  # control para mostrar globos/mensaje

# ---------- Encabezado con regalo ----------
st.title("🎁 GiftBox – Tu app personal navideña")
st.caption("Organiza hábitos, gratitud y metas; visualiza tu resumen anual.")

c1, c2, c3 = st.columns([1,1,1])
with c2:
    st.markdown("""
<div class="gift-box">
  <div class="ribbon-vert"></div>
  <div class="ribbon-hori"></div>
  <div class="tag">🎄 Navidad 2025</div>
</div>
""", unsafe_allow_html=True)
    # Botón para abrir el regalo
    if st.button("🎁 Abrir regalo de Feliz Navidad 2025"):
        st.session_state.regalo_abierto = True
        # Efecto de globos
        st.balloons()

# Mensaje festivo al abrir el regalo
if st.session_state.regalo_abierto:
    st.markdown(
        "<div class='gift-message'>✨ ¡Feliz Navidad 2025! Que sea un año de salud, proyectos con propósito y metas cumplidas. ✨</div>",
        unsafe_allow_html=True
    )

st.divider()

# ---------- Pestañas ----------
tab_personal, tab_resumen = st.tabs(["🧘 Personal", "📜 Resumen anual"])

# =========================================================
# 🧘 PERSONAL
# =========================================================
with tab_personal:
    st.header("Bienestar y organización personal")

    # --- Hábitos diarios ---
    st.subheader("✅ Checklist de hábitos")
    with st.form("form_habitos", clear_on_submit=True):
        fecha_hab = st.date_input("Fecha", value=date.today())
        habito = st.text_input("Hábito (p. ej., caminar 20 min)")
        completado = st.checkbox("Completado")
        enviar_hab = st.form_submit_button("Agregar hábito")
        if enviar_hab:
            st.session_state.habitos.append({
                "Fecha": fecha_hab.isoformat(),
                "Hábito": habito,
                "Completado": "Sí" if completado else "No"
            })
            st.success("Hábito agregado ✅")
    st.dataframe(pd.DataFrame(st.session_state.habitos), use_container_width=True)

    # --- Gratitud / Diario ---
    st.subheader("✍️ Gratitud / Diario")
    with st.form("form_journal", clear_on_submit=True):
        fecha_j = st.date_input("Fecha", value=date.today(), key="fecha_journal")
        nota = st.text_area("¿Por qué te sientes agradecido/a hoy?")
        enviar_j = st.form_submit_button("Agregar entrada")
        if enviar_j:
            st.session_state.journal.append({"Fecha": fecha_j.isoformat(), "Nota": nota})
            st.success("Entrada agregada ✅")
    st.dataframe(pd.DataFrame(st.session_state.journal), use_container_width=True)

    # --- Metas ---
    st.subheader("🎯 Metas")
    with st.form("form_metas", clear_on_submit=True):
        meta = st.text_input("Meta (p. ej., leer 12 libros)")
        categoria = st.selectbox("Categoría", ["Salud", "Finanzas", "Habilidades", "Relaciones", "Trabajo", "Otro"])
        fecha_obj = st.date_input("Fecha objetivo", value=date.today() + relativedelta(months=3))
        progreso = st.slider("Progreso (%)", 0, 100, 0)
        enviar_m = st.form_submit_button("Agregar meta")
        if enviar_m:
            st.session_state.metas.append({
                "Meta": meta,
                "Categoría": categoria,
                "Fecha objetivo": fecha_obj.isoformat(),
                "Progreso (%)": progreso
            })
            st.success("Meta agregada ✅")
    st.dataframe(pd.DataFrame(st.session_state.metas), use_container_width=True)

# =========================================================
# 📜 RESUMEN ANUAL
# =========================================================
with tab_resumen:
    st.header("Resumen anual")
    st.caption("Visualiza tu resumen en pantalla.")

    # Construcción del resumen a partir del estado en memoria
    habitos = pd.DataFrame(st.session_state.habitos)
    journal = pd.DataFrame(st.session_state.journal)
    metas = pd.DataFrame(st.session_state.metas)

    completados = habitos["Completado"].eq("Sí").sum() if not habitos.empty else 0
    total_habitos = len(habitos)
    ratio = (completados / total_habitos * 100) if total_habitos else 0.0
    categoria_top = metas["Categoría"].mode()[0] if not metas.empty else "N/A"
    avance_promedio = metas["Progreso (%)"].mean() if not metas.empty else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Hábitos completados (%)", f"{ratio:.1f}%")
    c2.metric("Avance promedio en metas", f"{avance_promedio:.1f}%")
    c3.metric("Categoría más trabajada", categoria_top)

    # Mostrar resumen en Markdown (solo visual)
    notas = "\n".join([f"- {n}" for n in journal["Nota"].tail(10)]) if not journal.empty else "- Sin registros"
    anio = datetime.now().year
    md = f"""# 🎉 Resumen anual
**Año:** {anio}

## Hábitos
- Total: {total_habitos}
- Completados: {completados} ({ratio:.1f}%)

## Metas
- Avance promedio: {avance_promedio:.1f}%
- Categoría más trabajada: {categoria_top}

## Gratitud / Diario (últimas 10 entradas)
{notas}

---
> Generado por Analytics Team – ¡Feliz Navidad y un gran {anio + 1}! 🎄
"""
    st.markdown(md)
