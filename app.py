# --------------------------------------------------
# App metas en acción – Organización personal en Streamlit
# Pestañas: Personal y Resumen anual (sin guardar datos)
# Incluye: Botón para guardar imagen (PNG) del resumen anual
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
    page_title="App metas en acción",
    page_icon="✅",
    layout="wide"
)

# ---------- Estado inicial (solo memoria en sesión) ----------
if "habitos" not in st.session_state:
    st.session_state.habitos = []
if "journal" not in st.session_state:
    st.session_state.journal = []
if "metas" not in st.session_state:
    st.session_state.metas = []

# ---------- Encabezado ----------
st.title("Tu espacio para crecer y cumplir metas")
st.caption("¡Haz que cada día cuente! Registra tus hábitos, tu gratitud y alcanza tus metas con claridad.")

st.divider()

# ---------- Pestañas ----------
tab_personal, tab_resumen = st.tabs(["🧘 Registro", "📜 Resumen"])

# =========================================================
# 🧘 Registro
# =========================================================
with tab_personal:
    st.header("Construye la mejor versión de ti")

    # --- Hábitos diarios ---
    st.subheader("✅ Lista de hábitos para tu mejor versión")
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
    st.subheader("✍️ Escribe lo que te inspira hoy")
    with st.form("form_journal", clear_on_submit=True):
        fecha_j = st.date_input("Fecha", value=date.today(), key="fecha_journal")
        nota = st.text_area("¿Por qué te sientes agradecido/a hoy?")
        enviar_j = st.form_submit_button("Agregar entrada")
        if enviar_j:
            st.session_state.journal.append({"Fecha": fecha_j.isoformat(), "Nota": nota})
            st.success("Entrada agregada ✅")
    st.dataframe(pd.DataFrame(st.session_state.journal), use_container_width=True)

    # --- Metas ---
    st.subheader("🎯 Construye el camino hacia tus sueños")
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
    st.header("¡Descubre todo lo que puedes lograr!")
    st.caption("Se muestra en pantalla y puedes guardar una imagen (PNG) del resumen en tu equipo o dispositivo móvil.")

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
    md = f"""
**Escrito en el:** {anio}

## Hábitos
- Total: {total_habitos}
- Completados: {completados} ({ratio:.1f}%)

## Metas
- Avance promedio: {avance_promedio:.1f}%
- Categoría más trabajada: {categoria_top}

## Gratitud (últimas 10 entradas)
{notas}

"""
    st.markdown(md)

    # ---------- Generar imagen PNG del resumen (descarga local) ----------
    def generar_imagen_resumen(md_text: str) -> io.BytesIO:
        """Convierte el texto del resumen a una imagen PNG con estilo neutro.
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
        limpio = md_text.replace("# Resumen anual", "Resumen anual").replace("## ", "").replace("**", "")
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

        # Fondo y colores neutros
        bg_color = (255, 255, 255)   # blanco
        text_color = (0, 0, 0)       # negro
        line_color = (0, 0, 0)       # negro

        # Crear imagen
        img = Image.new("RGB", (W, H), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Título
        x = padding
        y = padding
        draw.text((x, y), f"¡Descubre todo lo que puedes lograr!", font=font_title, fill=text_color)
        y += title_height + 20

        # Cuerpo
        for line in wrapped:
            draw.text((x, y), line, font=font_body, fill=text_color)
            y += sample_h + line_spacing

        # Footer
        y += 20
        draw.line([(padding, y), (W - padding, y)], fill=line_color, width=2)
        y += 10
        footer = "Generado por Analytics Team"
        draw.text((x, y), footer, font=font_footer, fill=text_color)

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
        file_name="resumen_metas.png",
        mime="image/png"
    )


