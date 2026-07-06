import streamlit as st
import pandas as pd
import plotly.express as px
import time
from google import genai
from google.genai import types
st.set_page_config(page_title="Rendimiento Académico", layout="wide")

# --- DICCIONARIO DE TRADUCCIONES COMPLETAS (Sistema Multiidioma con todos tus idiomas) ---
TRADUCCIONES = {
    "Inglés": {
        "titulo_app": "📊 Academic Performance",
        "panel_control": "⚙️ Control Panel",
        "color_graficos": "Chart Color:",
        "color_neon": "Letter Neon Color:",
        "idioma": "🌐 Language",
        "materias_lbl": "📚 Subjects",
        "nueva_materia_placeholder": "New subject name:",
        "btn_add_materia": "➕ Add Subject",
        "btn_volver_general": "🏠 Back to General Panel",
        "ia_estudiantes": "🤖 AI Students (Gemini)",
        "perfil_lbl": "Educational Level:",
        "pregunta_ia_lbl": "Academic question:",
        "btn_preguntar_ia": "Ask AI",
        "warning_api_key": "⚠️ Please enter a valid API Key in the code.",
        "confirm_eliminar": "⚠️ Permanently delete {}?",
        "btn_cancelar": "❌ Cancel",
        "btn_eliminar": "🗑️ Delete",
        "rango_general_exp": "🎯 COMBINED SUBJECT RANGE",
        "nota_media_general": "📈 General Average Score",
        "sin_tareas_expediente": "Register tasks in your subjects to calculate the file.",
        "lista_asignaturas": "📋 List of Subjects",
        "sin_tareas_grid": "*No tasks*",
        "no_graficos": "No charts available yet.",
        "seccion_gestion_tareas": "📝 Task Management",
        "sin_tareas_materia": "This subject does not contain tasks yet.",
        "add_nueva_entrega": "Add new task or exam:",
        "tipo_entrega_lbl": "Select delivery type:",
        "tema_examen_lbl": "Exam topic or name:",
        "desc_tarea_lbl": "Task name or description:",
        "modalidad_trabajo": "Project Modality:",
        "nombre_trabajo_lbl": "Project Name:",
        "nota_obtenida_lbl": "Score obtained (0.0 - 10.0):",
        "btn_guardar": "Save Academic Record",
        "guardado_ok": "Saved successfully.",
        "grafico_caption": "Add marks to view the interactive chart.",
        "opc_examen": "Exam",
        "opc_tarea": "Task",
        "opc_trabajo": "Project",
        "individual": "Individual",
        "en_grupo": "Group",
        "valor_tareas": "Value of Tasks",
        "porcentaje_error": "⚠️ Attention! The sum of the percentages must be exactly 100%.",
        "aviso_ia": "⚠️ AI can make mistakes. Verify important information for your studies."
    },
    "Español (España)": {
        "titulo_app": "📊 Rendimiento Académico",
        "panel_control": "⚙️ Panel de Control",
        "color_graficos": "Color de los Gráficos:",
        "color_neon": "Color del Neón de la Letra:",
        "idioma": "🌐 Idioma",
        "materias_lbl": "📚 Materias",
        "nueva_materia_placeholder": "Nombre de la nueva materia:",
        "btn_add_materia": "➕ Añadir Materia",
        "btn_volver_general": "🏠 Volver al Panel General",
        "ia_estudiantes": "🤖 IA Estudiantes (Gemini)",
        "perfil_lbl": "Nivel Educativo:",
        "pregunta_ia_lbl": "Pregunta académica:",
        "btn_preguntar_ia": "Preguntar a IA",
        "warning_api_key": "⚠️ Introduce una API Key válida en el código.",
        "confirm_eliminar": "⚠️ ¿Eliminar permanentemente **{}**?",
        "btn_cancelar": "❌ Cancelar",
        "btn_eliminar": "🗑️ Eliminar",
        "rango_general_exp": "🎯 RANGO COMBINADO DE LA MATERIA",
        "nota_media_general": "📈 Nota Media General",
        "sin_tareas_expediente": "Registre tareas en sus asignaturas para calcular el expediente.",
        "lista_asignaturas": "📋 Lista de Asignaturas",
        "sin_tareas_grid": "*Sin tareas*",
        "no_graficos": "No hay gráficos disponibles todavía.",
        "seccion_gestion_tareas": "📝 Gestión de Tareas",
        "sin_tareas_materia": "Esta materia no contiene tareas todavía.",
        "add_nueva_entrega": "Agregar nueva tarea o examen:",
        "tipo_entrega_lbl": "Selecciona el tipo de entrega:",
        "tema_examen_lbl": "Tema o nombre del Examen:",
        "desc_tarea_lbl": "Nombre o descripción de la Tarea:",
        "modalidad_trabajo": "Modalidad del Trabajo:",
        "nombre_trabajo_lbl": "Nombre del Trabajo:",
        "nota_obtenida_lbl": "Nota obtenida (0.0 - 10.0):",
        "btn_guardar": "Guardar Registro Académico",
        "guardado_ok": "Guardado correctamente.",
        "grafico_caption": "Agrega notas para ver el gráfico interactivo.",
        "opc_examen": "Examen",
        "opc_tarea": "Tarea",
        "opc_trabajo": "Trabajo",
        "individual": "Individual",
        "en_grupo": "En Grupo",
        "valor_tareas": "Valor de las Tareas",
        "porcentaje_error": "⚠️ ¡Atención! La suma de los porcentajes debe ser exactamente 100%.",
        "aviso_ia": "⚠️ La IA puede cometer errores. Verifica la información importante para tus estudios."
    },
    "Catalán": {
        "titulo_app": "📊 Rendiment Acadèmic",
        "panel_control": "⚙️ Panell de Control",
        "color_graficos": "Color dels Gràfics:",
        "color_neon": "Color del Neó de la Lletra:",
        "idioma": "🌐 Idioma",
        "materias_lbl": "📚 Matèries",
        "nueva_materia_placeholder": "Nom de la nova matèria:",
        "btn_add_materia": "➕ Afegir Matèria",
        "btn_volver_general": "🏠 Tornar al Panell General",
        "ia_estudiantes": "🤖 IA Estudiants (Gemini)",
        "perfil_lbl": "Nivell Educatiu:",
        "pregunta_ia_lbl": "Pregunta acadèmica:",
        "btn_preguntar_ia": "Preguntar a la IA",
        "warning_api_key": "⚠️ Introdueix una API Key vàlida al codi.",
        "confirm_eliminar": "⚠️ Eliminar permanentment **{}**?",
        "btn_cancelar": "❌ Cancel·lar",
        "btn_eliminar": "🗑️ Eliminar",
        "rango_general_exp": "🎯 RANG COMBINAT DE LA MATÈRIA",
        "nota_media_general": "📈 Nota Mitjana General",
        "sin_tareas_expediente": "Registreu tasques a les vostres assignatures per calcular l'expedient.",
        "lista_asignaturas": "📋 Llista d'Assignatures",
        "sin_tareas_grid": "*Sense tasques*",
        "no_graficos": "No hi ha gràfics disponibles encara.",
        "seccion_gestion_tareas": "📝 Gestió de Tasques",
        "sin_tareas_materia": "Aquesta matèria no conté tasques encara.",
        "add_nueva_entrega": "Afegir nova tasca o examen:",
        "tipo_entrega_lbl": "Selecciona el tipus de lliurament:",
        "tema_examen_lbl": "Tema o nom de l'Examen:",
        "desc_tarea_lbl": "Nom o descripció de la Tasca:",
        "modalidad_trabajo": "Modalitat del Treball:",
        "nombre_trabajo_lbl": "Nom del Treball:",
        "nota_obtenida_lbl": "Nota obtinguda (0.0 - 10.0):",
        "btn_guardar": "Desar Registre Acadèmic",
        "guardado_ok": "Desat correctament.",
        "grafico_caption": "Afegiu notes per veure el gràfic interactiu.",
        "opc_examen": "Examen",
        "opc_tarea": "Tasca",
        "opc_trabajo": "Treball",
        "individual": "Individual",
        "en_grupo": "En Grup",
        "valor_tareas": "Valor de les Tasques",
        "porcentaje_error": "⚠️ Atenció! La suma dels percentatges ha de ser exactament 100%.",
        "aviso_ia": "⚠️ La IA pot cometre errors. Verifica la informació important per als teus estudis."
    },
    "Francés": {
        "titulo_app": "📊 Rendement Académique",
        "panel_control": "⚙️ Panneau de Contrôle",
        "color_graficos": "Couleur des Graphiques:",
        "color_neon": "Couleur du Néon de la Lettre:",
        "idioma": "🌐 Langue",
        "materias_lbl": "📚 Matières",
        "nueva_materia_placeholder": "Nom de la nouvelle matière:",
        "btn_add_materia": "➕ Ajouter une Matière",
        "btn_volver_general": "🏠 Retour au Panneau Général",
        "ia_estudiantes": "🤖 IA Étudiants (Gemini)",
        "perfil_lbl": "Niveau Éducatif:",
        "pregunta_ia_lbl": "Question académique:",
        "btn_preguntar_ia": "Demander à l'IA",
        "warning_api_key": "⚠️ Veuillez entrer une clé API valide.",
        "confirm_eliminar": "⚠️ Supprimer définitivement {}?",
        "btn_cancelar": "❌ Annuler",
        "btn_eliminar": "🗑️ Supprimer",
        "rango_general_exp": "🎯 GAMME COMBINÉE DE MATIÈRES",
        "nota_media_general": "📈 Note Moyenne Générale",
        "sin_tareas_expediente": "Enregistrez des devoirs dans vos matières.",
        "lista_asignaturas": "📋 Liste des Matières",
        "sin_tareas_grid": "*Aucun devoir*",
        "no_graficos": "Aucun graphique disponible.",
        "seccion_gestion_tareas": "📝 Gestion des Devoirs",
        "sin_tareas_materia": "Cette matière ne contient pas encore de devoirs.",
        "add_nueva_entrega": "Ajouter un nouveau devoir:",
        "tipo_entrega_lbl": "Type de rendu:",
        "tema_examen_lbl": "Sujet de l'Examen:",
        "desc_tarea_lbl": "Description du Devoir:",
        "modalidad_trabajo": "Modalité du Projet:",
        "nombre_trabajo_lbl": "Nom du Projet:",
        "nota_obtenida_lbl": "Note obtenue (0.0 - 10.0):",
        "btn_guardar": "Enregistrer le Dossier",
        "guardado_ok": "Enregistré avec succès.",
        "grafico_caption": "Ajoutez des notes pour voir le graphique.",
        "opc_examen": "Examen",
        "opc_tarea": "Devoir",
        "opc_trabajo": "Projet",
        "individual": "Individuel",
        "en_grupo": "En Groupe",
        "valor_tareas": "Valeur des Devoirs",
        "porcentaje_error": "⚠️ Attention! La somme des pourcentages doit être de 100%.",
        "aviso_ia": "⚠️ L'IA peut faire des erreurs. Vérifiez les informations importantes pour vos études."
    },
    "Alemán": {
        "titulo_app": "📊 Akademische Leistung",
        "panel_control": "⚙️ Bedienfeld",
        "color_graficos": "Diagrammfarbe:",
        "color_neon": "Buchstaben-Neonfarbe:",
        "idioma": "🌐 Sprache",
        "materias_lbl": "📚 Fächer",
        "nueva_materia_placeholder": "Name des neuen Fachs:",
        "btn_add_materia": "➕ Fach hinzufügen",
        "btn_volver_general": "🏠 Zurück zum Hauptpanel",
        "ia_estudiantes": "🤖 KI für Studenten (Gemini)",
        "perfil_lbl": "Bildungsstufe:",
        "pregunta_ia_lbl": "Akademische Frage:",
        "btn_preguntar_ia": "KI fragen",
        "warning_api_key": "⚠️ Bitte geben Sie einen gültigen API-Schlüssel ein.",
        "confirm_eliminar": "⚠️ Möchten Sie {} dauerhaft löschen?",
        "btn_cancelar": "❌ Abbrechen",
        "btn_eliminar": "🗑️ Löschen",
        "rango_general_exp": "🎯 KOMBINIERTER FACHBEREICH",
        "nota_media_general": "📈 Gesamtdurchschnittsnote",
        "sin_tareas_expediente": "Tragen Sie Aufgaben in Ihren Fächern ein.",
        "lista_asignaturas": "📋 Fächerliste",
        "sin_tareas_grid": "*Keine Aufgaben*",
        "no_graficos": "Noch keine Diagramme verfügbar.",
        "seccion_gestion_tareas": "📝 Aufgabenverwaltung",
        "sin_tareas_materia": "Dieses Fach enthält noch keine Aufgaben.",
        "add_nueva_entrega": "Neue Aufgabe hinzufügen:",
        "tipo_entrega_lbl": "Abgabetyp auswählen:",
        "tema_examen_lbl": "Thema der Prüfung:",
        "desc_tarea_lbl": "Beschreibung der Aufgabe:",
        "modalidad_trabajo": "Projektmodalität:",
        "nombre_trabajo_lbl": "Projektname:",
        "nota_obtenida_lbl": "Erzielte Note (0.0 - 10.0):",
        "btn_guardar": "Speichern",
        "guardado_ok": "Erfolgreich gespeichert.",
        "grafico_caption": "Fügen Sie Noten hinzu.",
        "opc_examen": "Prüfung",
        "opc_tarea": "Aufgabe",
        "opc_trabajo": "Projekt",
        "individual": "Einzeln",
        "en_grupo": "In der Gruppe",
        "valor_tareas": "Wert der Aufgaben",
        "porcentaje_error": "⚠️ Die Summe der Prozentwerte muss genau 100% sein.",
        "aviso_ia": "⚠️ KI kann Fehler machen. Überprüfen Sie wichtige Informationen für Ihr Studium."
    }
}

# Estilos CSS globales para animaciones holográficas y plataformas
st.markdown("""
<style>
    .grid-letter-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 10px;
        background: rgba(20, 20, 25, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        min-height: 140px;
    }
    
    @keyframes floatAndRotate {
        0% { transform: translateY(0px) rotateY(0deg); }
        50% { transform: translateY(-8px) rotateY(180deg); }
        100% { transform: translateY(0px) rotateY(360deg); }
    }

    .futuristic-letter {
        font-size: 55px;
        font-weight: bold;
        perspective: 1000px;
        animation: floatAndRotate 6s ease-in-out infinite;
        z-index: 2;
        text-shadow: 0 0 10px currentColor, 0 0 20px currentColor;
    }

    .platform-A {
        position: relative;
        width: 120px;
        height: 25px;
        background: #1e1e2f;
        border: 3px solid #ffd700;
        border-radius: 6px;
        box-shadow: 0 0 15px #00d2ff, inset 0 0 10px #ffd700;
        transform: rotateX(60deg);
        margin-top: 5px;
    }

    .platform-B {
        position: relative;
        width: 110px;
        height: 25px;
        background: #112233;
        border: 3px solid #00f0ff;
        border-radius: 50%;
        box-shadow: 0 0 20px #00f0ff, inset 0 0 8px #00f0ff;
        transform: rotateX(65deg);
        margin-top: 5px;
    }
    
    .platform-generic {
        position: relative;
        width: 100px;
        height: 20px;
        background: #222;
        border: 2px solid #9932cc;
        border-radius: 4px;
        box-shadow: 0 0 10px #9932cc;
        transform: rotateX(60deg);
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = "AQ.Ab8RN6K4_MTXKxpY9IgVltfYxzLZH9BEknvUK8-pNnSoK7SSbA" 

def calcular_letra_rango(nota):
    if 9 <= nota <= 10: return "A"
    elif 8 <= nota < 9: return "B"
    elif 7 <= nota < 8: return "C"
    elif 6 <= nota < 7: return "D"
    elif 5 <= nota < 6: return "E"
    elif 4 <= nota < 5: return "F"
    elif 3 <= nota < 4: return "G"
    elif 2 <= nota < 3: return "H"
    elif 1 <= nota < 2: return "I"
    else: return "J"

# --- Inicialización de los Estados de Sesión ---
if 'materias' not in st.session_state:
    st.session_state.materias = ["Matemáticas", "Historia", "Ciencias"]

if 'registro_actividades' not in st.session_state:
    st.session_state.registro_actividades = {
        "Matemáticas": [
            {"Tipo": "Examen", "Actividad": "Examen: Álgebra", "Nota": 9.5},
            {"Tipo": "Tarea", "Actividad": "Tarea: Matrices", "Nota": 8.0},
            {"Tipo": "Trabajo", "Actividad": "Trabajo (En Grupo): Hologramas", "Nota": 9.0}
        ],
        "Historia": [],
        "Ciencias": []
    }

if 'ponderaciones' not in st.session_state:
    st.session_state.ponderaciones = {
        "Matemáticas": {"Examen": 60, "Tarea": 20, "Trabajo": 20},
        "Historia": {"Examen": 40, "Tarea": 30, "Trabajo": 30},
        "Ciencias": {"Examen": 50, "Tarea": 25, "Trabajo": 25}
    }

if 'materia_a_eliminar' not in st.session_state:
    st.session_state.materia_a_eliminar = None

if 'materia_seleccionada' not in st.session_state:
    st.session_state.materia_seleccionada = None

# Idioma por defecto inicializado en Inglés (English)
if 'idioma_actual' not in st.session_state:
    st.session_state.idioma_actual = "Inglés"

if 'animar_graficos' not in st.session_state:
    st.session_state.animar_graficos = True

txt = TRADUCCIONES.get(st.session_state.idioma_actual, TRADUCCIONES["Inglés"])

# BARRA LATERAL (Sidebar)
with st.sidebar:
    st.header(txt["panel_control"])
    
    # Menú de Idiomas solicitado
    idioma_elegido = st.selectbox(
        txt["idioma"], 
        ["Español (España)", "Catalán", "Inglés", "Francés", "Alemán"],
        index=["Español (España)", "Catalán", "Inglés", "Francés", "Alemán"].index(st.session_state.idioma_actual)
    )
    if idioma_elegido != st.session_state.idioma_actual:
        st.session_state.idioma_actual = idioma_elegido
        st.rerun()

    color_graficos = st.color_picker(txt["color_graficos"], "#4169E1")
    color_letra = st.color_picker(txt["color_neon"], "#00F0FF")
    
    st.write("---")
    st.subheader(txt["materias_lbl"])
    nueva_materia = st.text_input(txt["nueva_materia_placeholder"])
    if st.button(txt["btn_add_materia"], use_container_width=True) and nueva_materia:
        if nueva_materia not in st.session_state.materias:
            st.session_state.materias.append(nueva_materia)
            st.session_state.registro_actividades[nueva_materia] = []
            st.session_state.ponderaciones[nueva_materia] = {"Examen": 40, "Tarea": 30, "Trabajo": 30}
            st.rerun()

    if st.session_state.materia_seleccionada is not None:
        st.write("---")
        if st.button(txt["btn_volver_general"], type="primary", use_container_width=True):
            st.session_state.materia_seleccionada = None
            st.session_state.animar_graficos = True
            st.rerun()

    # --- SECCIÓN IA CONFIGURADA CON FILTROS MÁXIMOS ---
    st.write("---")
    st.subheader(txt["ia_estudiantes"])
    
    # Nuevos perfiles educativos adaptados
    perfil_usuario = st.selectbox(
        txt["perfil_lbl"], 
        ["Secundaria", "Ciclos Formativos", "Bachillerato", "Formación Profesional", "Universitarios"]
    )
    
    prompt_ia = st.text_input(txt["pregunta_ia_lbl"])
    if st.button(txt["btn_preguntar_ia"], use_container_width=True) and prompt_ia:
        if API_KEY == "TU_API_KEY_AQUÍ":
            st.warning(txt["warning_api_key"])
        else:
            try:
                # Inicializar el cliente oficial SDK de GenAI v0.1+
                client = genai.Client(api_key=API_KEY)
                
                # Configuración estricta de seguridad al nivel más alto (Block Most / BLOCK_LOW_AND_ABOVE)
                seguridad = [
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    ),
                ]
                
                respuesta = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Nivel Académico: {perfil_usuario}. Pregunta: {prompt_ia}",
                    config=types.GenerateContentConfig(safety_settings=seguridad)
                )
                st.info(respuesta.text)
            except Exception as e:
                st.error(f"Error: {e}")
                
    # Texto de advertencia de IA obligatorio solicitado en el pie
    st.caption(f"_{txt['aviso_ia']}_")

# Diálogo de confirmación de borrado
if st.session_state.materia_a_eliminar:
    materia_target = st.session_state.materia_a_eliminar
    st.warning(txt["confirm_eliminar"].format(materia_target))
    col_conf1, col_conf2 = st.columns(2)
    with col_conf1:
        if st.button(txt["btn_cancelar"], use_container_width=True):
            st.session_state.materia_a_eliminar = None
            st.rerun()
    with col_conf2:
        if st.button(txt["btn_eliminar"], type="primary", use_container_width=True):
            if materia_target in st.session_state.materias:
                st.session_state.materias.remove(materia_target)
                if materia_target in st.session_state.registro_actividades:
                    del st.session_state.registro_actividades[materia_target]
                if materia_target in st.session_state.ponderaciones:
                    del st.session_state.ponderaciones[materia_target]
            if st.session_state.materia_seleccionada == materia_target:
                st.session_state.materia_seleccionada = None
            st.session_state.materia_a_eliminar = None
            st.rerun()

# Procesamiento de expedientes ponderados en el Dashboard General
datos_globales = []
lista_medias_validas = []

for m in st.session_state.materias:
    acts = st.session_state.registro_actividades.get(m, [])
    pesos = st.session_state.ponderaciones.get(m, {"Examen": 40, "Tarea": 30, "Trabajo": 30})
    if acts:
        ex_n = [a['Nota'] for a in acts if a.get('Tipo') == "Examen"]
        ta_n = [a['Nota'] for a in acts if a.get('Tipo') == "Tarea"]
        tr_n = [a['Nota'] for a in acts if a.get('Tipo') == "Trabajo"]
        
        media_ex = sum(ex_n) / len(ex_n) if ex_n else 0
        media_ta = sum(ta_n) / len(ta_n) if ta_n else 0
        media_tr = sum(tr_n) / len(tr_n) if tr_n else 0
        
        suma_pesos_activos = 0
        nota_ponderada = 0
        if ex_n:
            nota_ponderada += media_ex * (pesos["Examen"] / 100)
            suma_pesos_activos += (pesos["Examen"] / 100)
        if ta_n:
            nota_ponderada += media_ta * (pesos["Tarea"] / 100)
            suma_pesos_activos += (pesos["Tarea"] / 100)
        if tr_n:
            nota_ponderada += media_tr * (pesos["Trabajo"] / 100)
            suma_pesos_activos += (pesos["Trabajo"] / 100)
            
        final_score = (nota_ponderada / suma_pesos_activos) if suma_pesos_activos > 0 else 0.0
        lista_medias_validas.append(final_score)
        datos_globales.append({"Materia": m, "Calificación": round(final_score, 2), "Letra": calcular_letra_rango(final_score)})
    else:
        datos_globales.append({"Materia": m, "Calificación": None, "Letra": None})

# =========================================================================
# VISTA DE DETALLE DE UNA MATERIA SELECCIONADA
# =========================================================================
if st.session_state.materia_seleccionada is not None:
    materia_actual = st.session_state.materia_seleccionada
    
    # Nombre único de la materia como título principal de la vista
    st.title(f"📘 {materia_actual}")
    
    tareas = st.session_state.registro_actividades.get(materia_actual, [])
    pesos_actuales = st.session_state.ponderaciones.get(materia_actual, {"Examen": 40, "Tarea": 30, "Trabajo": 30})
    
    examenes_notas = [t['Nota'] for t in tareas if t.get('Tipo') == "Examen"]
    tareas_notas = [t['Nota'] for t in tareas if t.get('Tipo') == "Tarea"]
    trabajos_notas = [t['Nota'] for t in tareas if t.get('Tipo') == "Trabajo"]
    
    m_ex = sum(examenes_notas) / len(examenes_notas) if examenes_notas else 0
    m_ta = sum(tareas_notas) / len(tareas_notas) if tareas_notas else 0
    m_tr = sum(trabajos_notas) / len(trabajos_notas) if trabajos_notas else 0
    
    suma_div = 0
    num_pond = 0
    if examenes_notas:
        num_pond += m_ex * (pesos_actuales["Examen"] / 100)
        suma_div += (pesos_actuales["Examen"] / 100)
    if tareas_notas:
        num_pond += m_ta * (pesos_actuales["Tarea"] / 100)
        suma_div += (pesos_actuales["Tarea"] / 100)
    if trabajos_notas:
        num_pond += m_tr * (pesos_actuales["Trabajo"] / 100)
        suma_div += (pesos_actuales["Trabajo"] / 100)
        
    media_combinada = (num_pond / suma_div) if suma_div > 0 else 0.0
    
    # Rango general acumulado de la materia
    if tareas:
        letra_combinada = calcular_letra_rango(media_combinada)
        plat_comb = "platform-A" if letra_combinada == "A" else ("platform-B" if letra_combinada == "B" else "platform-generic")
        
        st.markdown(f"<div style='text-align:center; margin-bottom:2px; color:gray; font-weight:bold; letter-spacing:1px;'>{txt['rango_general_exp']} ({media_combinada:.2f})</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='display:flex; flex-direction:column; align-items:center; margin-bottom:35px;'>
            <div class='futuristic-letter' style='color:{color_letra}; font-size:48px;'>{letra_combinada}</div>
            <div class='{plat_comb}' style='width:90px; height:15px;'></div>
        </div>
        """, unsafe_allow_html=True)

    # Bloques independientes por categoría
    cat_c1, cat_c2, cat_c3 = st.columns(3)
    with cat_c1:
        st.markdown(f"<p style='text-align:center;margin-bottom:2px; font-weight:bold; font-size:18px;'>{txt['opc_examen']}</p>", unsafe_allow_html=True)
        if examenes_notas:
            l_ex = calcular_letra_rango(m_ex)
            plat = "platform-B" if l_ex == "B" else ("platform-A" if l_ex == "A" else "platform-generic")
            st.markdown(f"<div style='display:flex;flex-direction:column;align-items:center;'><div class='futuristic-letter' style='color:{color_letra};font-size:35px;'>{l_ex}</div><div class='{plat}' style='width:70px;height:12px;'></div></div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align:center;color:gray;'>-</p>", unsafe_allow_html=True)
            
    with cat_c2:
        st.markdown(f"<p style='text-align:center;margin-bottom:2px; font-weight:bold; font-size:18px;'>{txt['opc_tarea']}</p>", unsafe_allow_html=True)
        if tareas_notas:
            l_ta = calcular_letra_rango(m_ta)
            plat = "platform-B" if l_ta == "B" else ("platform-A" if l_ta == "A" else "platform-generic")
            st.markdown(f"<div style='display:flex;flex-direction:column;align-items:center;'><div class='futuristic-letter' style='color:{color_letra};font-size:35px;'>{l_ta}</div><div class='{plat}' style='width:70px;height:12px;'></div></div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align:center;color:gray;'>-</p>", unsafe_allow_html=True)
            
    with cat_c3:
        st.markdown(f"<p style='text-align:center;margin-bottom:2px; font-weight:bold; font-size:18px;'>{txt['opc_trabajo']}</p>", unsafe_allow_html=True)
        if trabajos_notas:
            l_tr = calcular_letra_rango(m_tr)
            plat = "platform-B" if l_tr == "B" else ("platform-A" if l_tr == "A" else "platform-generic")
            st.markdown(f"<div style='display:flex;flex-direction:column;align-items:center;'><div class='futuristic-letter' style='color:{color_letra};font-size:35px;'>{l_tr}</div><div class='{plat}' style='width:70px;height:12px;'></div></div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align:center;color:gray;'>-</p>", unsafe_allow_html=True)
            
    st.write("---")
    
    col_esp_1, col_esp_2, col_esp_3 = st.columns([1.2, 1.0, 1.2])
    
    with col_esp_1:
        st.subheader(txt["seccion_gestion_tareas"])
        if tareas:
            for index, t_info in enumerate(tareas):
                col_t_del, col_t_info = st.columns([0.15, 0.85])
                with col_t_del:
                    if st.button("🗑️", key=f"del_task_{materia_actual}_{index}"):
                        st.session_state.registro_actividades[materia_actual].pop(index)
                        st.rerun()
                with col_t_info:
                    tipo_trad = txt["opc_examen"] if t_info.get('Tipo') == "Examen" else (txt["opc_tarea"] if t_info.get('Tipo') == "Tarea" else txt["opc_trabajo"])
                    st.markdown(f"**[{tipo_trad}] {t_info['Actividad']}**: {t_info['Nota']:.1f} / 10.0")
        else:
            st.info(txt["sin_tareas_materia"])
            
        st.write("---")
        st.markdown(f"**{txt['add_nueva_entrega']}**")
        tipo_actividad = st.selectbox(txt["tipo_entrega_lbl"], [txt["opc_examen"], txt["opc_tarea"], txt["opc_trabajo"]])
        
        detalles_actividad = ""
        tipo_interno = "Tarea"
        if tipo_actividad == txt["opc_examen"]:
            nombre_especifico = st.text_input(txt["tema_examen_lbl"])
            detalles_actividad = nombre_especifico if nombre_especifico else txt["opc_examen"]
            tipo_interno = "Examen"
        elif tipo_actividad == txt["opc_tarea"]:
            nombre_especifico = st.text_input(txt["desc_tarea_lbl"])
            detalles_actividad = nombre_especifico if nombre_especifico else txt["opc_tarea"]
            tipo_interno = "Tarea"
        elif tipo_actividad == txt["opc_trabajo"]:
            sub_opcion = st.radio(txt["modalidad_trabajo"], [txt["individual"], txt["en_grupo"]], horizontal=True)
            nombre_especifico = st.text_input(txt["nombre_trabajo_lbl"])
            detalles_actividad = f"{nombre_especifico} ({sub_opcion})" if nombre_especifico else f"{txt['opc_trabajo']} ({sub_opcion})"
            tipo_interno = "Trabajo"

        nota_t = st.number_input(txt["nota_obtenida_lbl"], min_value=0.0, max_value=10.0, value=7.0, step=0.1)
        if st.button(txt["btn_guardar"], use_container_width=True):
            st.session_state.registro_actividades[materia_actual].append({
                "Tipo": tipo_interno,
                "Actividad": detalles_actividad, 
                "Nota": nota_t
            })
            st.success(txt["guardado_ok"])
            st.rerun()

    # Panel central: Ponderación de tareas
    with col_esp_2:
        st.subheader(txt["valor_tareas"])
        st.markdown("Modifica el valor porcentual que tiene cada opción sobre la asignatura:")
        
        p_examen = st.slider(f"📊 {txt['opc_examen']}", 0, 100, pesos_actuales["Examen"], step=5)
        p_tarea = st.slider(f"📝 {txt['opc_tarea']}", 0, 100, pesos_actuales["Tarea"], step=5)
        p_trabajo = st.slider(f"📁 {txt['opc_trabajo']} ({txt['individual']} / {txt['en_grupo']})", 0, 100, pesos_actuales["Trabajo"], step=5)
        
        total_p = p_examen + p_tarea + p_trabajo
        st.markdown(f"**Suma Total:** `{total_p}%` / `100%`")
        
        if total_p != 100:
            st.error(txt["porcentaje_error"])
        else:
            if (p_examen != pesos_actuales["Examen"] or p_tarea != pesos_actuales["Tarea"] or p_trabajo != pesos_actuales["Trabajo"]):
                st.session_state.ponderaciones[materia_actual] = {"Examen": p_examen, "Tarea": p_tarea, "Trabajo": p_trabajo}
                st.rerun()

    # Bloque 3: Animación de Gráficos Secuenciales
    with col_esp_3:
        if tareas:
            if st.session_state.animar_graficos:
                with st.spinner("Loading Holographic Systems..."):
                    time.sleep(0.5)
                st.session_state.animar_graficos = False
                
            df_tareas = pd.DataFrame(tareas)
            fig_ind = px.bar(df_tareas, x="Actividad", y="Nota", text="Nota", range_y=[0, 10])
            fig_ind.update_traces(texttemplate='%{text:.1f}', textposition='outside', marker_color=color_graficos)
            fig_ind.update_layout(
                width=380, height=380, margin=dict(l=20, r=20, t=20, b=20),
                transition={'duration': 600, 'easing': 'cubic-in-out'}
            )
            st.plotly_chart(fig_ind, use_container_width=True, config={'displayModeBar': False})
        else:
            st.caption(txt["grafico_caption"])

    if st.button(txt["btn_volver_general"]):
        st.session_state.materia_seleccionada = None
        st.session_state.animar_graficos = True
        st.rerun()

# =========================================================================
# VISTA GENERAL DEL EXPEDIENTE ACADÉMICO
# =========================================================================
else:
    st.title(txt["titulo_app"])
    
    if lista_medias_validas:
        media_general = sum(lista_medias_validas) / len(lista_medias_validas)
        letra_general = calcular_letra_rango(media_general)
        
        with st.container(border=True):
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.write(f"**{txt['rango_general_exp']} (PONDERADO)**")
                clase_plat_gen = "platform-A" if letra_general == "A" else ("platform-B" if letra_general == "B" else "platform-generic")
                html_gen = f"""
                <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 120px;'>
                    <div class='futuristic-letter' style='color: {color_letra};'>{letra_general}</div>
                    <div class='{clase_plat_gen}'></div>
                </div>
                """
                st.markdown(html_gen, unsafe_allow_html=True)
            with col_m2:
                st.metric(label=txt["nota_media_general"], value=f"{media_general:.2f} / 10.0")
    else:
        with st.container(border=True):
            st.info(txt["sin_tareas_expediente"])

    st.write("---")
    col1, col2 = st.columns([1.5, 1.5])

    with col1:
        st.subheader(txt["lista_asignaturas"])
        for fila in datos_globales:
            m_name = fila["Materia"]
            letra_m = fila["Letra"]
            
            c_del, c_nav, c_info = st.columns([0.15, 0.45, 0.4])
            with c_del:
                if st.button(f"🗑️", key=f"del_mat_{m_name}"):
                    st.session_state.materia_a_eliminar = m_name
                    st.rerun()
            with c_nav:
                if st.button(f"📘 {m_name}", key=f"open_mat_{m_name}", use_container_width=True):
                    st.session_state.materia_seleccionada = m_name
                    st.session_state.animar_graficos = True
                    st.rerun()
            with c_info:
                if letra_m is not None:
                    clase_plat_loop = "platform-A" if letra_m == "A" else ("platform-B" if letra_m == "B" else "platform-generic")
                    html_loop = f"""
                    <div class='grid-letter-container'>
                        <div class='futuristic-letter' style='color: {color_letra}; font-size: 38px;'>{letra_m}</div>
                        <div class='{clase_plat_loop}' style='width:70px; height:15px;'></div>
                    </div>
                    """
                    st.markdown(html_loop, unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='grid-letter-container'>{txt['sin_tareas_grid']}</div>", unsafe_allow_html=True)

    with col2:
        df_general_real = pd.DataFrame([f for f in datos_globales if f["Calificación"] is not None])
        if not df_general_real.empty:
            if st.session_state.animar_graficos:
                with st.spinner("Syncing Charts..."):
                    time.sleep(0.4)
                st.session_state.animar_graficos = False
                
            fig = px.bar(df_general_real, x="Materia", y="Calificación", text="Calificación", range_y=[0, 10])
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside', marker_color=color_graficos)
            fig.update_layout(
                width=420, height=400, margin=dict(l=30, r=30, t=20, b=30),
                transition={'duration': 800, 'easing': 'cubic-in-out'}
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.caption(txt["no_graficos"])
