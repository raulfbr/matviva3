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

def build_lesson(filename):
    """Constrói uma única lição."""
    filepath = os.path.join(SOURCE_DIR, filename)
    metadata, body_html = parse_markdown(filepath)
    
    # Filter: Skip templates
    if "TEMPLATE" in filename: return None

    with open(os.path.join(TEMPLATE_DIR, "layout_base.html"), "r", encoding="utf-8") as f:
        template = f.read()
    
    # Injetar Dados
    output_html = template
    output_html = output_html.replace("{{ titulo }}", metadata.get("titulo", "Sem Título"))
    output_html = output_html.replace("{{ fase }}", metadata.get("fase", "Sementes"))
    output_html = output_html.replace("{{ meta }}", metadata.get("meta", ""))
    output_html = output_html.replace("{{ guardia }}", metadata.get("guardia", "Misterioso"))
    output_html = output_html.replace("{{ tempo }}", metadata.get("tempo", "15 min"))
    output_html = output_html.replace("{{ local }}", metadata.get("local", "O Reino"))
    output_html = output_html.replace("{{ versao }}", metadata.get("versao", "3.6"))
    output_html = output_html.replace("{{ conteudo }}", body_html)
    
    # TGTB Logic (If empty, remove line or hide)
    tgtb_ref = metadata.get("tgtb", "")
    output_html = output_html.replace("{{ tgtb }}", tgtb_ref)
    
    # --- IMAGE MAPPING LOGIC ---
    guardian_name = metadata.get("guardia", "Misterioso").split(" ")[0] # Pegar primeiro nome
    
    # Map Names to Files (Naive approach, can be improved with regex or refined dict)
    image_map = {
        "Melquior": "melquior-leao.webp",
        "Celeste": "celeste-raposa.webp",
        "Bernardo": "bernardo-urso.webp",
        "Íris": "iris-passarinho-colar.webp",
        "Noé": "noe-coruja.webp"
    }

    # Location Fuzzy Match (Simple inclusion check)
    loc_name = metadata.get("local", "O Reino").lower()
    loc_img = "local-jardim-central.webp" # Default
    
    if "árvore" in loc_name or "arvore" in loc_name: loc_img = "local-arvore-silencio.webp"
    elif "caverna" in loc_name: loc_img = "local-caverna-recomeco.webp"
    elif "clareira" in loc_name: loc_img = "local-clareira-perguntas.webp"
    elif "ninho" in loc_name: loc_img = "local-ninho-mirante.webp"
    elif "floresta" in loc_name: loc_img = "local-arvore-silencio.webp"

    # Inject Image Paths
    output_html = output_html.replace("{{ guardia_img }}", f"../assets/img/{image_map.get(guardian_name, 'melquior-leao.webp')}")
    output_html = output_html.replace("{{ local_img }}", f"../assets/img/{loc_img}")

    
    output_filename = filename.replace(".md", ".html")
    with open(os.path.join(DIST_SEMENTES, output_filename), "w", encoding="utf-8") as f:
        f.write(output_html)
        
    print(f"✅ [LESSON] {output_filename}")
    
    metadata['filename'] = output_filename
    metadata['original_filename'] = filename
    # Remove ugly MV-S prefix for display logic if needed
    metadata['clean_id'] = metadata.get('id', '').replace('MV-S-', 'Lição ')
    return metadata

def build_static_pages():
    """Constrói páginas estáticas (Quem Somos, Metodo, etc)."""
    if not os.path.exists(PAGES_DIR):
        return

    with open(os.path.join(TEMPLATE_DIR, "layout_page.html"), "r", encoding="utf-8") as f:
        template = f.read()

    for filename in os.listdir(PAGES_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(PAGES_DIR, filename)
            metadata, body_html = parse_markdown(filepath)
            
            output_html = template
            output_html = output_html.replace("{{ titulo }}", metadata.get("titulo", "Página"))
            output_html = output_html.replace("{{ conteudo }}", body_html)
            
            output_filename = filename.replace(".md", ".html")
            with open(os.path.join(DIST_PAGES, output_filename), "w", encoding="utf-8") as f:
                f.write(output_html)
            print(f"📄 [PAGE] {output_filename}")

def render_card_grid(lessons_subset):
    """Gera o HTML do Grid de Cards."""
    html = ""
    
    # Emojis para Guardiões
    guardian_emojis = {
        "Melquior": "🦁",
        "Celeste": "🦊",
        "Bernardo": "🐻",
        "Íris": "🐦",
        "Noé": "🦉"
    }

    for licao in lessons_subset:
        # TGTB Badge Logic
        tgtb_val = licao.get('tgtb', '')
        tgtb_html = ""
        if tgtb_val and "{{" not in tgtb_val: 
             # Limpar string para ficar curto (Ex: "Math K, Lesson 10" -> "MK L10" se quiser, mas vamos manter limpo)
             tgtb_html = f'<span class="badge-tgtb" title="Baseado em {tgtb_val}">📘 {tgtb_val}</span>'

        # Guardian Logic
        g_name = licao.get('guardia', '').split(' ')[0] # Pega só o primeiro nome
        g_emoji = guardian_emojis.get(g_name, "🛡️")

        card = f"""
        <a href="sementes/{licao['filename']}" class="card">
            <div class="card-header-row">
                <span class="card-id">{licao.get('clean_id', '???')}</span>
                {tgtb_html}
            </div>
            <h3 class="card-title">{licao.get('titulo')}</h3>
            
            <!-- Meta/Goal limpo (Essencialismo: apenas o texto, sem labels extras) -->
            <p class="card-desc">{licao.get('meta', '').replace('🍇 ', '').replace('🦁 ', '').replace('🐻 ', '').replace('🦊 ', '')}</p>
            
            <div class="card-footer">
                <span class="guardian-tag">{g_emoji} {g_name}</span>
                <span class="time-tag">⏱️ {licao.get('tempo')}</span>
            </div>
        </a>
        """
        html += card
    return html

def build_index(lessons):
    """Constrói a Landing Page."""
    with open(os.path.join(TEMPLATE_DIR, "layout_index.html"), "r", encoding="utf-8") as f:
        template = f.read()

    arco_despertar = []
    arco_ritmo = [] 
    arco_plenitude = []
    
    for licao in lessons:
        fname = licao['original_filename']
        try:
            num = int(fname.split('_')[0])
            if num <= 3: arco_despertar.append(licao)
            elif num <= 10: arco_ritmo.append(licao)
            else: arco_plenitude.append(licao) # 11+ e Assessments caem aqui
        except ValueError:
            arco_plenitude.append(licao)

    final_index = template
    
    # Navigation Bar Injection
    nav_bar = """
    <nav class="portal-nav">
        <a href="pages/convite_real.html" class="nav-link">🏰 O Convite Real</a>
        <a href="pages/manifesto.html" class="nav-link">📜 Manifesto</a>
        <a href="pages/quem_somos.html" class="nav-link">🦁 Quem Somos</a>
    </nav>
    """
    # Replace a placeholder if exists, otherwise prepend to body (risky). 
    # Let's assume there is a place or I insert after <body>
    if "<body>" in final_index:
        final_index = final_index.replace("<body>", "<body>" + nav_bar)
    else:
        # Fallback if no body tag found (unlikely)
        final_index = nav_bar + final_index

    final_index = final_index.replace("{{ arco_despertar }}", render_card_grid(arco_despertar))
    final_index = final_index.replace("{{ arco_ritmo }}", render_card_grid(arco_ritmo))
    final_index = final_index.replace("{{ arco_plenitude }}", render_card_grid(arco_plenitude))
    final_index = final_index.replace("{{ data_build }}", datetime.now().strftime("%d/%m/%Y %H:%M"))

    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_index)
    
    print(f"🏠 [INDEX] Home Page Gerada.")

def collect_metadata():
    """Passo 1: Coletar metadados de todas as lições."""
    lessons_data = []
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ [ERR] Pasta fonte não encontrada: {SOURCE_DIR}")
        return []

    files = sorted(os.listdir(SOURCE_DIR))
    for filename in files:
        if filename.endswith(".md") and "TEMPLATE" not in filename:
            filepath = os.path.join(SOURCE_DIR, filename)
            meta, _ = parse_markdown(filepath) # Só precisamos do meta agora
            
            # Adicionar campos extras derivados
            meta['filename'] = filename.replace(".md", ".html")
            meta['original_filename'] = filename
            meta['clean_id'] = meta.get('id', '').replace('MV-S-', 'Lição ')
            
            lessons_data.append(meta)
    
    # Ordenar por ID ou Filename para garantir sequencia
    # Assumindo filename "001_..." funciona bem
    return lessons_data

def render_lesson(meta, prev_meta, next_meta):
    """Passo 2: Renderizar HTML com links de navegação."""
    filepath = os.path.join(SOURCE_DIR, meta['original_filename'])
    _, body_html = parse_markdown(filepath) # Ler corpo novamente (poderia otimizar, mas ok para SSG)
    
    with open(os.path.join(TEMPLATE_DIR, "layout_base.html"), "r", encoding="utf-8") as f:
        template = f.read()
    
    # Injetar Dados Básicos
    output_html = template
    output_html = output_html.replace("{{ titulo }}", meta.get("titulo", "Sem Título"))
    output_html = output_html.replace("{{ fase }}", meta.get("fase", "Sementes"))
    output_html = output_html.replace("{{ meta }}", meta.get("meta", ""))
    output_html = output_html.replace("{{ guardia }}", meta.get("guardia", "Misterioso"))
    output_html = output_html.replace("{{ tempo }}", meta.get("tempo", "15 min"))
    output_html = output_html.replace("{{ local }}", meta.get("local", "O Reino"))
    output_html = output_html.replace("{{ versao }}", meta.get("versao", "3.6"))
    output_html = output_html.replace("{{ conteudo }}", body_html)
    
    # TGTB Logic
    tgtb_ref = meta.get("tgtb", "")
    output_html = output_html.replace("{{ tgtb }}", tgtb_ref)

    # --- CARD SYSTEM (Inline Image Processor) ---
    # Encontra todas as tags <img src="..."> e reescreve para Assets Dist
    # Regex para capturar src="algo"
    import re
    def replace_img_src(match):
        src = match.group(1)
        alt = match.group(2) if match.group(2) else ""
        
        # Se for link externo (http), ignora
        if src.startswith("http") and "placeholder" not in src:
            return f'<img src="{src}" alt="{alt}" class="lesson-card">'
            
        # Tenta extrair apenas o nome do arquivo
        filename = os.path.basename(src)
        
        # Remove extensão antiga e põe .webp
        base_name = os.path.splitext(filename)[0]
        webp_name = f"{base_name}.webp"
        
        # Caminho final no Dist
        dist_path = f"../assets/img/{webp_name}"
        
        # Verifica se existe no source (para saber se o optimizer gerou)
        # O optimizer roda antes, então checamos se o arquivo existe em dist/assets/img
        # (Mas aqui estamos rodando o script, então podemos checar dist/assets/img diretamente)
        real_dist_path_abs = os.path.join(DIST_IMG, webp_name)
        
        img_html = ""
        if os.path.exists(real_dist_path_abs):
            img_html = f'<div class="card-image-container"><img src="{dist_path}" alt="{alt}" class="lesson-card"></div>'
        else:
            # Fallback Card
            img_html = f'''
            <div class="card-missing">
                <span class="missing-icon">🖼️</span>
                <p><strong>Arte Faltante:</strong> {base_name}</p>
                <small>Adicione "{base_name}.png" em <code>curriculo/_SISTEMA/imagens</code></small>
            </div>
            '''
        return img_html

    # Regex para substituir <img src="X" alt="Y" /> gerado pelo Markdown
    # Padrão do python-markdown é <img alt="alt" src="src" /> ou <img src="src" alt="alt" />
    # Vamos usar uma abordagem mais robusta: processar o markdown raw antes? ou o html depois?
    # O HTML é mais fácil se o regex for bom.
    
    # Regex simplificado para capturar imagens
    # Padrão 1: src="..." alt="..."
    body_html = re.sub(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>', replace_img_src, body_html)
    
    # Padrão 2: alt="..." src="..." (Markdown as vezes gera assim)
    def replace_img_alt_first(match):
        # Neste caso group(1) é alt, group(2) é src
        # Criamos um objeto fake compatível com replace_img_src que espera (src, alt)
        alt = match.group(1)
        src = match.group(2)
        
        # Chamamos a função original mas simulando o match group
        class MatchMock:
            def group(self, n):
                return src if n == 1 else alt
        
        return replace_img_src(MatchMock())

    body_html = re.sub(r'<img[^>]+alt="([^"]*)"[^>]*src="([^"]+)"[^>]*>', replace_img_alt_first, body_html)

    output_html = output_html.replace("{{ conteudo }}", body_html)
    guardian_name = meta.get("guardia", "Misterioso").split(" ")[0]
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
    elif "floresta" in loc_name: loc_img = "local-arvore-silencio.webp"

    output_html = output_html.replace("{{ guardia_img }}", f"../assets/img/{image_map.get(guardian_name, 'melquior-leao.webp')}")
    output_html = output_html.replace("{{ local_img }}", f"../assets/img/{loc_img}")

    # --- NAVIGATION LOGIC ---
    # Prev Link
    if prev_meta:
        prev_html = f'<a href="{prev_meta["filename"]}" class="nav-btn prev">← Anterior: {prev_meta["clean_id"]}</a>'
    else:
        prev_html = '<span class="nav-btn disabled">← Início</span>'
    
    # Next Link
    if next_meta:
        next_html = f'<a href="{next_meta["filename"]}" class="nav-btn next">Próxima: {next_meta["clean_id"]} →</a>'
    else:
        next_html = '<a href="../index.html" class="nav-btn next">Concluir Jornada 🏁</a>'

    output_html = output_html.replace("{{ nav_prev }}", prev_html)
    output_html = output_html.replace("{{ nav_next }}", next_html)


    output_path = os.path.join(DIST_SEMENTES, meta['filename'])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_html)
        
    print(f"✅ [LESSON] {meta['filename']}")


def main():
    print("🦁 Gutenberg Engine v3.6 (Portal + Visuals + Nav)...")
    clean_dist()
    copy_assets()
    
    # Build Lessons (Two Pass)
    print("🔄 [PASS 1] Coletando Metadados...")
    all_lessons = collect_metadata()
    
    print(f"🔄 [PASS 2] Renderizando {len(all_lessons)} lições com navegação...")
    for i, meta in enumerate(all_lessons):
        prev_meta = all_lessons[i-1] if i > 0 else None
        next_meta = all_lessons[i+1] if i < len(all_lessons) - 1 else None
        
        render_lesson(meta, prev_meta, next_meta)

    
    # Build Static Pages
    build_static_pages()

    # Build Index
    build_index(all_lessons)
    print("🚀 Portal v3.6 Concluído!")

if __name__ == "__main__":
    main()
