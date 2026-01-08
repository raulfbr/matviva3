import os
import shutil
import markdown
import re
from datetime import datetime

# --- CONFIG ---
SOURCE_DIR = "curriculo/01_SEMENTES"
TEMPLATE_DIR = "curriculo/_SISTEMA/TEMPLATES"
DIST_DIR = "dist"
DIST_SEMENTES = os.path.join(DIST_DIR, "sementes")

def clean_dist():
    """Limpa a pasta dist para um build fresco."""
    if os.path.exists(DIST_DIR):
        try:
            shutil.rmtree(DIST_DIR)
            print(f"🧹 [CLEAN] Pasta {DIST_DIR} removida.")
        except Exception as e:
            print(f"⚠️ [WARN] Não foi possível remover completamente {DIST_DIR}: {e}")
    
    os.makedirs(DIST_SEMENTES, exist_ok=True)
    print(f"✨ [INIT] Pasta {DIST_DIR} pronta.")

def copy_assets():
    """Copia o CSS."""
    shutil.copy(os.path.join(TEMPLATE_DIR, "style.css"), os.path.join(DIST_DIR, "style.css"))
    # shutil.copytree("assets", os.path.join(DIST_DIR, "assets")) # Assets placeholder
    print(f"🎨 [ASSETS] style.css copiado.")

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
    
    return metadata, html_content

def build_lesson(filename):
    """Constrói uma única lição."""
    filepath = os.path.join(SOURCE_DIR, filename)
    metadata, body_html = parse_markdown(filepath)
    
    # Filter: Process only valid lessons (skip templates/drafts if needed)
    
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
    
    output_filename = filename.replace(".md", ".html")
    with open(os.path.join(DIST_SEMENTES, output_filename), "w", encoding="utf-8") as f:
        f.write(output_html)
        
    print(f"✅ [BUILD] {output_filename}")
    
    metadata['filename'] = output_filename
    metadata['original_filename'] = filename
    return metadata

def render_card_grid(lessons_subset):
    """Gera o HTML do Grid de Cards para um subconjunto de lições."""
    html = ""
    for licao in lessons_subset:
        card = f"""
        <a href="sementes/{licao['filename']}" class="card">
            <span class="card-id">{licao.get('id', 'MV-S-???')}</span>
            <h3 class="card-title">{licao.get('titulo')}</h3>
            <p class="card-desc">{licao.get('meta')}</p>
            <div class="card-footer">
                <span>🛡️ {licao.get('guardia')}</span>
                <span>⏱️ {licao.get('tempo')}</span>
            </div>
        </a>
        """
        html += card
    return html

def build_index(lessons):
    """Constrói a Landing Page com Arcos."""
    with open(os.path.join(TEMPLATE_DIR, "layout_index.html"), "r", encoding="utf-8") as f:
        template = f.read()

    # Buckets (Arcos)
    arco_despertar = []  # 000 - 003
    arco_ritmo = []      # 004 - 010
    arco_plenitude = []  # 011 +
    
    # Simple sorting logic based on filename prefix (000, 001...)
    for licao in lessons:
        fname = licao['original_filename']
        try:
            num = int(fname.split('_')[0])
            if num <= 3:
                arco_despertar.append(licao)
            elif num <= 10:
                arco_ritmo.append(licao)
            else:
                arco_plenitude.append(licao)
        except ValueError:
            # Fallback for non-numbered files
            arco_plenitude.append(licao)

    # Render Grids
    html_despertar = render_card_grid(arco_despertar)
    html_ritmo = render_card_grid(arco_ritmo)
    html_plenitude = render_card_grid(arco_plenitude)

    # Inject
    final_index = template
    final_index = final_index.replace("{{ arco_despertar }}", html_despertar)
    final_index = final_index.replace("{{ arco_ritmo }}", html_ritmo)
    final_index = final_index.replace("{{ arco_plenitude }}", html_plenitude)
    
    final_index = final_index.replace("{{ data_build }}", datetime.now().strftime("%d/%m/%Y %H:%M"))

    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_index)
    
    print(f"🏠 [INDEX] Landing Page gerada. (Despertar: {len(arco_despertar)}, Ritmo: {len(arco_ritmo)}, Plenitude: {len(arco_plenitude)})")

def main():
    print("🦁 Gutenberg Engine v2.0 (Exponential)...")
    clean_dist()
    copy_assets()
    
    lessons = []
    
    # Ler pasta Sementes
    files = sorted(os.listdir(SOURCE_DIR))
    for filename in files:
        if filename.endswith(".md"):
             # Simple skip for templates inside the lesson folder if any
            if "TEMPLATE" in filename: continue
            
            meta = build_lesson(filename)
            if meta:
                lessons.append(meta)
    
    build_index(lessons)
    print("🚀 Build Exponencial Concluído!")

if __name__ == "__main__":
    main()
