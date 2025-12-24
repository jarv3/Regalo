
# app.py
# --------------------------------------------------
# 🎁 GiftBox – App navideña en Streamlit
# Pestañas: Personal y Resumen anual (sin guardar datos)
# Incluye: Regalo “Feliz Navidad 2025” con globos al abrir
# + Botón para guardar imagen (PNG) del resumen anual
# --------------------------------------------------
import streamlit as st
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

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
    st.session_state.regalo_abierto = False

# ---------- Encabezado con regalo ----------
st.title("🎁 Tu app personal navideña")
st.caption("Organiza hábitos, gratitud y metas; visualiza tu resumen anual.")

c1, c2, c3 = st.columns([1,1,1])
with c2:
    st.markdown("""
<div class="gift-box">
  <div class="ribbon-vert"></div>
  <div class="ribbon-hori"></div>
  <div class="tag">🎄 Feliz Navidad</div>
</div>
""", unsafe_allow_html=True)
    if st.button("🎁 Abrir regalo de Feliz Navidad"):
        st.session_state.regalo_abierto = True
        st.balloons()

if st.session_state.regalo_abierto:
    st.markdown(
        "<div class='gift-message'>✨ ¡Feliz Navidad! Que sea un año de salud, proyectos con propósito y metas cumplidas. ✨</div>",
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
    st.caption("Se muestra en pantalla y puedes guardar una imagen (PNG) del resumen en tu equipo.")

    # Datos en memoria
    habitos = pd.DataFrame(st.session_state.habitos)
    journal = pd.DataFrame(st.session_state.journal)
    metas = pd.DataFrame(st.session_state.metas)

    # Métricas
    completados = habitos["Completado"].eq("Sí").sum() if not habitos.empty else 0
    total_habitos = len(habitos)
    ratio = (completados / total_habitos * 100) if total_habitos else 0.0
    categoria_top = metas["Categoría"].mode()[0] if not metas.empty else "N/A"
    avance_promedio = metas["Progreso (%)"].mean() if not metas.empty else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Hábitos completados (%)", f"{ratio:.1f}%")
    c2.metric("Avance promedio en metas", f"{avance_promedio:.1f}%")
    c3.metric("Categoría más trabajada", categoria_top)

    # Markdown del resumen (solo visual)
    notas = "\n".join([f"- {n}" for n in journal["Nota"].tail(10)]) if not journal.empty else "- Sin registros"
    anio = datetime.now().year
    md = f"""# 🎉 Resumen anual
**Escrito en el:** {anio}

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

    # ---------- Generar imagen PNG del resumen (descarga local) ----------
    def generar_imagen_resumen(md_text: str) -> io.BytesIO:
        """Convierte el texto del resumen a una imagen PNG con estilo claro.
        No guarda en disco; devuelve un buffer en memoria."""
        # Intentar cargar una fuente legible; fallback si no está disponible
        try:
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
            font_body  = ImageFont.truetype("DejaVuSans.ttf", 26)
            font_footer = ImageFont.truetype("DejaVuSans.ttf", 22)
        except Exception:
            font_title = ImageFont.load_default()
            font_body  = ImageFont.load_default()
            font_footer = ImageFont.load_default()

        # Preparar el texto (envolver líneas)
        # Reemplazar cabeceras Markdown simples
        limpio = md_text.replace("# 🎉", "🎉").replace("## ", "").replace("**", "")
        wrapped = []
        for line in limpio.splitlines():
            if not line.strip():
                wrapped.append("")  # línea en blanco
            else:
                # ancho de envoltura (caracteres) aproximado
                wrapped.extend(textwrap.wrap(line, width=68))

        # Calcular alto de imagen según líneas
        padding = 40
        line_spacing = 10
        # Altura por línea estimada con la fuente body
        sample_h = font_body.getbbox("Ag")[3] if hasattr(font_body, "getbbox") else 24
        content_height = len(wrapped) * (sample_h + line_spacing)
        title_height = font_title.getbbox("Resumen anual")[3] if hasattr(font_title, "getbbox") else 40
        footer_height = font_footer.getbbox("Footer")[3] if hasattr(font_footer, "getbbox") else 20

        W = 1200  # ancho imagen
        H = padding*2 + title_height + 20 + content_height + 20 + footer_height + 20

        # Crear imagen
        img = Image.new("RGB", (W, H), color=(253, 246, 227))  # #fdf6e3
        draw = ImageDraw.Draw(img)

        # Título
        x = padding
        y = padding
        draw.text((x, y), f"🎉 Resumen anual {anio}", fill=(109, 76, 65), font=font_title)
        y += title_height + 20

        # Cuerpo
        for line in wrapped:
            draw.text((x, y), line, fill=(70, 60, 50), font=font_body)
            y += sample_h + line_spacing

        # Exportar a buffer
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf

    # Botón de descarga solo de imagen (no guarda en servidor)
    png_buffer = generar_imagen_resumen(md)
    st.download_button(
        label="🖼️ Guardar imagen del resumen (PNG)",
        data=png_buffer,
        file_name="resumen_anual.png",
        mime="image/png"
    )


