import os
import shutil
import markdown
import re
from datetime import datetime

import optimizer  # Importante: certifique-se que optimizer.py está na mesma pasta

# --- CONFIG ---
SOURCE_DIR = "curriculo/01_SEMENTES"
PAGES_DIR = "curriculo/PAGES"
TEMPLATE_DIR = "curriculo/_SISTEMA/TEMPLATES"
IMAGES_DIR = "curriculo/_SISTEMA/imagens"  # New Source
DIST_DIR = "dist"
DIST_SEMENTES = os.path.join(DIST_DIR, "sementes")
DIST_PAGES = os.path.join(DIST_DIR, "pages")
DIST_IMG = os.path.join(DIST_DIR, "assets", "img") # Target for images

def clean_dist():
    """Limpa a pasta dist para um build fresco, preservando IMAGENS otimizadas."""
    
    # 1. Clean HTML folders (Sementes, Pages) - We want to regenerate these always
    if os.path.exists(DIST_SEMENTES):
        shutil.rmtree(DIST_SEMENTES, ignore_errors=True)
    if os.path.exists(DIST_PAGES):
        shutil.rmtree(DIST_PAGES, ignore_errors=True)
    
    # 2. Clean Index
    if os.path.exists(os.path.join(DIST_DIR, "index.html")):
        os.remove(os.path.join(DIST_DIR, "index.html"))

    # 3. Clean CSS (Always copy fresh)
    if os.path.exists(os.path.join(DIST_DIR, "style.css")):
        os.remove(os.path.join(DIST_DIR, "style.css"))

    # 4. Create folders if they don't exist
    os.makedirs(DIST_SEMENTES, exist_ok=True)
    os.makedirs(DIST_PAGES, exist_ok=True)
    os.makedirs(DIST_IMG, exist_ok=True)

    print(f"✨ [INIT] Pastas limpas (Imagens preservadas).")

def copy_assets():
    """Copia CSS e Otimiza Imagens."""
    shutil.copy(os.path.join(TEMPLATE_DIR, "style.css"), os.path.join(DIST_DIR, "style.css"))
    print(f"🎨 [ASSETS] style.css copiado.")
    
    # Run Optimizer
    optimizer.optimize_images(IMAGES_DIR, DIST_IMG)

def parse_markdown(filepath):
    """Lê um arquivo MD e extrai Frontmatter (YAML) e Conteúdo."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex simples para extrair YAML header
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    
    metadata = {}
    body_md = content
    
    if frontmatter_match:
        yaml_text = frontmatter_match.group(1)
        body_md = frontmatter_match.group(2)
        
        for line in yaml_text.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().replace('"', '')

    # Converter Markdown para HTML
    html_content = markdown.markdown(body_md, extensions=['fenced_code', 'tables', 'admonition'])
    
    # Processar Admonitions Customizados (Classes CSS)
    html_content = html_content.replace("<blockquote>\n<p>[!RITUAL]", "<blockquote class='ritual'>\n<p><strong>🕯️ RITUAL</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!MESTRA]", "<blockquote class='mestra'>\n<p><strong>👩‍🏫 MESTRA</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!NARRATIVA]", "<blockquote class='narrativa'>\n<p><strong>📖 NARRATIVA</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!ATIVIDADE]", "<blockquote class='atividade'>\n<p><strong>🛠️ ATIVIDADE</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!CONCEITO]", "<blockquote class='conceito'>\n<p><strong>💡 CONCEITO</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!TIP]", "<blockquote class='tip'>\n<p><strong>🦋 SE QUISER VOAR</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!NOTE]", "<blockquote class='note'>\n<p><strong>📝 NOTA</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!IMPORTANT]", "<blockquote class='important'>\n<p><strong>⚠️ IMPORTANTE</strong>")
    
    return metadata, html_content

import glob

# --- CONFIGURAÇÃO K-12 ---
# Define a ordem e os metadados das fases
K12_PHASES = [
    {"id": "vivencia", "folder": "00_VIVENCIA", "title": "Vivência (0-4 Anos)", "desc": "O Despertar do Logos. A ordem no ordinário.", "color": "#7B68B8", "icon": "🍼"},
    {"id": "sementes", "folder": "01_SEMENTES", "title": "Sementes (5-6 Anos)", "desc": "O Jardim do Maravilhamento. Onde tudo começa.", "color": "#2E8B57", "icon": "🌿"},
    {"id": "raizes", "folder": "02_RAIZES", "title": "Raízes (7-10 Anos)", "desc": "A Oficina da Ordem. A construção do hábito.", "color": "#8B4513", "icon": "🌳"},
    {"id": "logica", "folder": "03_LOGICA", "title": "Lógica (11-14 Anos)", "desc": "A Fortaleza da Verdade. O rigor da razão.", "color": "#4682B4", "icon": "⚔️"},
    {"id": "legado", "folder": "04_LEGADO", "title": "Legado (15-18 Anos)", "desc": "O Governo do Logos. Servir para liderar.", "color": "#D4A84B", "icon": "👑"}
]

CONTENT_DIR = "curriculo" # Base para scan

def scan_markdown_files():
    """Varre todas as pastas de fase definidas em K12_PHASES."""
    all_lessons = []
    
    for phase in K12_PHASES:
        phase_dir = os.path.join(CONTENT_DIR, phase["folder"])
        # Fallback para Sementes se estiver em outro lugar ou se for a estrutura antiga
        
        if not os.path.exists(phase_dir):
            print(f"⚠️ [WARN] Fase não encontrada: {phase['folder']}")
            continue
            
        print(f"🔍 [SCAN] Lendo fase: {phase['title']}...")
        files = glob.glob(os.path.join(phase_dir, "*.md"))
        
        for f in files:
            meta, body = parse_markdown(f)
            
            # Skip se for dummy (mas queremos renderizar dummy para debug? Na verdade, dummy é placeholder)
            # Vamos renderizar dummy SE não houver ID.
            if not meta.get('id'): 
                 if "DUMMY" not in f: continue
            
            # Injeta metadata da fase se não existir
            if not meta.get('fase'): meta['fase'] = phase['title']
            
            # Adiciona caminho relativo para link
            filename = os.path.basename(f)
            html_filename = filename.replace('.md', '.html')
            
            dest_folder = phase["folder"].lower().split('_', 1)[1] # Ex: 01_SEMENTES -> sementes
            
            lesson_data = {
                "meta": meta,
                "body": body,
                "filename": filename,
                "html_filename": html_filename,
                "dest_folder": dest_folder, # sementes, raizes, etc
                "phase_id": phase["id"]
            }
            all_lessons.append(lesson_data)
            
    return all_lessons

def render_lesson_template(meta, body_content, prev_link=None, next_link=None):
    """Renderiza o template HTML final para uma lição."""
    
    # 1. Carregar Template Base
    template_path = os.path.join(TEMPLATE_DIR, "layout_base.html") # Usando layout_base existente
    # Se layout_lesson.html existir, use. Mas vamos manter layout_base para compatibilidade imediata.
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
        
    # 2. Dados do Guardião (Imagem e Cor)
    guardian_name = meta.get("guardia", "Melquior").split(' ')[0]
    image_map = {
        "Melquior": "melquior-leao.webp",
        "Celeste": "celeste-raposa.webp",
        "Bernardo": "bernardo-urso.webp",
        "Íris": "iris-passarinho-colar.webp",
        "Noé": "noe-coruja.webp"
    }
    
    loc_name = meta.get("local", "O Reino").lower()
    loc_img = "local-jardim-central.webp" # Default
    if "árvore" in loc_name or "arvore" in loc_name: loc_img = "local-arvore-silencio.webp"
    elif "caverna" in loc_name: loc_img = "local-caverna-recomeco.webp"
    elif "clareira" in loc_name: loc_img = "local-clareira-perguntas.webp"
    elif "ninho" in loc_name: loc_img = "local-ninho-mirante.webp"
    
    # --- NAVIGATION LOGIC ---
    # Prev Link
    if prev_link:
        nav_prev = f'<a href="{prev_link}" class="nav-btn prev">← Anterior</a>'
    else:
        nav_prev = '<a href="../index.html" class="nav-btn prev">🏠 Início</a>'
        
    # Next Link
    if next_link:
        nav_next = f'<a href="{next_link}" class="nav-btn next">Próxima →</a>'
    else:
        nav_next = '<span class="nav-btn disabled">Fim 🏁</span>'

    # 3. Substituições
    html = template
    html = html.replace("{{ titulo }}", meta.get("titulo", "Sem Título"))
    html = html.replace("{{ meta }}", meta.get("meta", ""))
    html = html.replace("{{ conteudo }}", body_content)
    
    # Inject Nav (Manually if template doesn't support placeholders yet, but let's try injecting into wrapper)
    # Hack: Inject nav buttons at end of content if placeholders missing
    if "{{ nav_prev }}" in html:
        html = html.replace("{{ nav_prev }}", nav_prev)
        html = html.replace("{{ nav_next }}", nav_next)
    else:
        # Append to body content
        html = html.replace("{{ conteudo }}", body_content + f'<div class="lesson-nav">{nav_prev} {nav_next}</div>')

    # Metadata Injections
    html = html.replace("{{ fase }}", meta.get("fase", "Geral"))
    html = html.replace("{{ guardia }}", meta.get("guardia", "Misterioso"))
    html = html.replace("{{ tempo }}", meta.get("tempo", "15 min"))
    html = html.replace("{{ local }}", meta.get("local", "O Reino"))
    html = html.replace("{{ versao }}", meta.get("versao", "3.6"))
    html = html.replace("{{ tgtb }}", meta.get("tgtb", ""))
    
    # Images
    html = html.replace("{{ guardia_img }}", f"../assets/img/{image_map.get(guardian_name, 'melquior-leao.webp')}")
    html = html.replace("{{ local_img }}", f"../assets/img/{loc_img}")
    
    # Clean up empty tags
    html = re.sub(r'\{\{.*?\}\}', '', html)
    
    return html

def build_navigation_map(lessons):
    """Cria mapa de navegação (prev/next) ordenado por ID dentro de cada fase."""
    nav_map = {}
    
    # Agrupar por fase
    lessons_by_phase = {}
    for l in lessons:
        pid = l['phase_id']
        if pid not in lessons_by_phase: lessons_by_phase[pid] = []
        lessons_by_phase[pid].append(l)
        
    for pid, phase_lessons in lessons_by_phase.items():
        # Ordenar por filename (assumindo 001, 002...)
        phase_lessons.sort(key=lambda x: x['filename'])
        
        for i, l in enumerate(phase_lessons):
            curr = l['filename']
            prev = phase_lessons[i-1]['html_filename'] if i > 0 else "../index.html"
            nxt = phase_lessons[i+1]['html_filename'] if i < len(phase_lessons)-1 else None
            
            nav_map[curr] = {"prev": prev, "next": nxt}
            
    return nav_map

def build_lessons(lessons):
    """Renderiza cada lição em sua subpasta correta."""
    nav_map = build_navigation_map(lessons)
    
    for lesson in lessons:
        meta = lesson['meta']
        body_html = lesson['body']
        dest_folder = lesson['dest_folder']
        filename = lesson['filename']
        
        # Cria pasta de destino se não existir
        out_dir = os.path.join(DIST_DIR, dest_folder)
        os.makedirs(out_dir, exist_ok=True)
        
        # Navigation Links
        nav_data = nav_map.get(filename, {})
        prev_link = nav_data.get('prev')
        next_link = nav_data.get('next')

        final_html = render_lesson_template(meta, body_html, prev_link, next_link)
        
        out_path = os.path.join(out_dir, lesson['html_filename'])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        print(f"✅ [LESSON] {dest_folder}/{lesson['html_filename']}")

def render_static_page(meta, body, filename):
     # Simple static page renderer
    template_path = os.path.join(TEMPLATE_DIR, "layout_page.html")
    if not os.path.exists(template_path): return
    
    with open(template_path, "r", encoding="utf-8") as f: template = f.read()
    
    html = template.replace("{{ titulo }}", meta.get("titulo", "Page")).replace("{{ conteudo }}", body)
    with open(os.path.join(DIST_PAGES, filename), "w", encoding="utf-8") as f: f.write(html)
    print(f"📄 [PAGE] {filename}")

def render_card_grid(lessons_list, is_coming_soon=False):
    """Renderiza grid de cards HTML."""
    if is_coming_soon or not lessons_list:
        return """
        <div class="coming-soon-card">
            <span class="coming-soon-icon">🚧</span>
            <h3 class="coming-soon-title">Em Breve: Área do Construtor</h3>
            <p class="coming-soon-desc">Os Guardiões estão preparando este terreno.</p>
        </div>
        """
        
    html = '<div class="card-grid">\n'
    
    # Order lessons by filename
    lessons_list.sort(key=lambda x: x['filename'])
    
    for l in lessons_list:
        meta = l['meta']
        link = f"{l['dest_folder']}/{l['html_filename']}"
        
        title = meta.get('titulo', 'Sem Título')
        desc = meta.get('meta', 'Descrição não disponível.')
        guardian = meta.get('guardia', 'Reino')
        time = meta.get('tempo', 'N/A')
        tgtb_ref = meta.get('tgtb', '')
        lid = meta.get('id', '')
        
        # Badge Logic
        badge_html = ""
        if tgtb_ref and tgtb_ref.upper() != "N/A":
            badge_html = f'<span class="badge-tgtb" title="Baseado em {tgtb_ref}">📘 {tgtb_ref}</span>'
        
        # Guardian Emoji logic
        g_emoji = "🦁"
        if "Celeste" in guardian: g_emoji = "🦊"
        if "Bernardo" in guardian: g_emoji = "🐻"
        if "Íris" in guardian: g_emoji = "🐦"
        if "Noé" in guardian: g_emoji = "🦉"
        
        html += f"""
        <a href="{link}" class="card">
            <div class="card-header-row">
                <span class="card-id">{lid}</span>
                {badge_html}
            </div>
            <h3 class="card-title">{title}</h3>
            <p class="card-desc">{desc}</p>
            <div class="card-footer">
                <span class="guardian-tag">{g_emoji} {guardian}</span>
                <span class="time-tag">⏱️ {time}</span>
            </div>
        </a>
        """
    html += '</div>'
    return html

def build_index(lessons):
    """Constrói a Home Page K-12."""
    template_path = os.path.join(TEMPLATE_DIR, "layout_index.html")
    
    # Fallback template se não existir
    if not os.path.exists(template_path): return
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
        
    # Limpar placeholders antigos se existirem
    final_index = template
    
    nav_bar = """
    <nav class="portal-nav">
        <a href="pages/convite_real.html" class="nav-link">🏰 O Convite</a>
        <a href="pages/manifesto.html" class="nav-link">📜 Manifesto</a>
        <a href="pages/quem_somos.html" class="nav-link">🦁 Quem Somos</a>
    </nav>
    """
    
    sections_html = ""
    for phase in K12_PHASES:
        # Filtrar lições desta fase
        # phase['id'] was inserted into lesson meta
        p_lessons = [l for l in lessons if l['phase_id'] == phase['id']]
        
        # Se for dummy, tratar como empty para mostrar Coming Soon
        real_lessons = [l for l in p_lessons if "DUMMY" not in l['filename']]
        
        is_coming_soon = len(real_lessons) == 0
        
        sections_html += f"""
        <section class="section" id="{phase['id']}">
            <div class="container">
                <div class="arc-header" style="border-left: 4px solid {phase['color']}; padding-left: 1rem; margin-bottom:1.5rem;">
                    <span style="color: {phase['color']}; font-weight: bold; text-transform: uppercase; font-size: 0.9rem;">{phase['icon']} FASE {phase['id'].upper()}</span>
                    <h2>{phase['title']}</h2>
                    <p>{phase['desc']}</p>
                </div>
                {render_card_grid(real_lessons, is_coming_soon)}
            </div>
        </section>
        """
    
    # Hero Logic: We need to replace the content of layout_index.html dynamically
    # But layout_index might expect {{ arco_despertar }} etc.
    # We will replace the whole content area or try to be smart.
    # Check if {{ sections_k12 }} exists? Probably not.
    # Let's replace {{ arco_despertar }} with sections_html and remove others.
    
    final_index = final_index.replace("<body>", "<body>" + nav_bar)
    final_index = final_index.replace("{{ arco_despertar }}", sections_html)
    final_index = final_index.replace("{{ arco_ritmo }}", "")
    final_index = final_index.replace("{{ arco_plenitude }}", "")
    
    final_index = final_index.replace("{{ data_build }}", datetime.now().strftime("%d/%m/%Y %H:%M"))
    
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_index)
    print("🏠 [INDEX] Home Page K-12 Gerada.")


def main():
    print("🦁 Gutenberg Engine v3.6 (Portal + Visuals + Nav)...")
    clean_dist()
    copy_assets()
    
    # Build Lessons    # 3. Scan & Build
    print("🔄 [PASS 1] Coletando Metadados K-12...")
    all_lessons = scan_markdown_files()
    
    print(f"🔄 [PASS 2] Renderizando {len(all_lessons)} lições com navegação...")
    build_lessons(all_lessons)
    
    # 4. Build Pages (Static)
    # Scan pages dir
    pages_files = glob.glob(os.path.join(PAGES_DIR, "*.md"))
    for p in pages_files:
        meta, body = parse_markdown(p)
        filename = os.path.basename(p).replace('.md', '.html')
        
        # Render Page
        # Uses simpler template or same? Let's use generic layout
        # ... (reuse logic or simplify)
        # For now, simplistic render:
        render_static_page(meta, body, filename)

    # 5. Build Index (K-12 Family Home)
    build_index(all_lessons)
    print("🚀 Portal v3.6 Concluído!")

if __name__ == "__main__":
    main()
