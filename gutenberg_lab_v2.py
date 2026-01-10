import os
import shutil
import markdown
import re
import glob
from datetime import datetime

# --- CONFIG LAB V2 ---
SOURCE_DIR = "curriculo/01_SEMENTES_TESTE"
TEMPLATE_DIR = "curriculo/_SISTEMA/TEMPLATES"
DIST_DIR = "dist"
DIST_LAB_V2 = os.path.join(DIST_DIR, "lab_v2")
DIST_LAB_V2_SEMENTES = os.path.join(DIST_LAB_V2, "sementes")

def clean_lab_v2():
    """Limpa apenas a pasta lab_v2."""
    if os.path.exists(DIST_LAB_V2):
        shutil.rmtree(DIST_LAB_V2, ignore_errors=True)
    os.makedirs(DIST_LAB_V2_SEMENTES, exist_ok=True)
    print(f"✨ [LAB-V2] Pasta {DIST_LAB_V2} limpa.")

def copy_lab_v2_assets():
    """Copia o CSS do Lab V2."""
    shutil.copy(os.path.join(TEMPLATE_DIR, "style_lab_v2.css"), os.path.join(DIST_LAB_V2, "style_lab_v2.css"))
    print(f"🎨 [LAB-V2] style_lab_v2.css copiado.")

def parse_markdown(filepath):
    """Lê um arquivo MD e extrai Frontmatter e Conteúdo."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        body_md = match.group(2)
    else:
        clean_content = re.sub(r"^```markdown\n", "", content)
        meta_lines = []
        body_lines = []
        in_meta = True
        for line in clean_content.split("\n"):
            if in_meta and (":" in line and not line.startswith("#")):
                meta_lines.append(line)
            else:
                in_meta = False
                body_lines.append(line)
        yaml_text = "\n".join(meta_lines)
        body_md = "\n".join(body_lines)
        body_md = re.sub(r"```$", "", body_md).strip()
    
    metadata = {}
    if yaml_text:
        for line in yaml_text.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().replace('"', '')

    # Admonition processing
    replacements = {
        "[!RITUAL]": ("ritual", "🕯️ Ritual"),
        "[!MESTRA]": ("mestra", "👩‍🏫 Mestra"),
        "[!NARRATIVA]": ("narrativa", "📖 Narrativa"),
        "[!ATIVIDADE]": ("atividade", "🛠️ Atividade"),
        "[!CONCEITO]": ("conceito", "💡 Conceito"),
        "[!TIP]": ("tip", "🦋 Se Quiser Voar"),
        "[!NOTE]": ("note", "📝 Nota"),
        "[!IMPORTANT]": ("important", "⚠️ Importante"),
        "[!MATERIAL]": ("material-card", "🎒 Material Necessário"),
        "[!FECHAMENTO]": ("fechamento", "🏁 Fechamento"),
        "[!PAI]": ("pai-action", "👨‍👧 Ação do Pai")
    }

    html_content = markdown.markdown(body_md, extensions=['fenced_code', 'tables', 'admonition'])
    
    for tag, (cls, title) in replacements.items():
        pattern = r"(<blockquote>\s*<p>)" + re.escape(tag)
        replacement = f"<blockquote class='{cls}'>\n<p><strong>{title}</strong>"
        html_content = re.sub(pattern, replacement, html_content)
    
    # === POST-PROCESSING (Schoger + CM Audit Fixes) ===
    
    # 1. Remove first H1 from content (duplicate of title)
    html_content = re.sub(r'^<h1[^>]*>.*?</h1>\s*', '', html_content, count=1)
    
    # 2. Process remaining inline admonitions that weren't caught
    inline_admonitions = [
        (r'\[!NOTE\]', '<strong>📝 Nota:</strong>'),
        (r'\[!PAI\]', '<strong>👨‍👧 Ação do Pai:</strong>'),
        (r'\[!NARRAÇÃO\]', '<strong>🗣️ Narração:</strong>'),
        (r'\[!TIP\]', '<strong>🦋 Dica:</strong>'),
        (r'\[!IMPORTANT\]', '<strong>⚠️ Importante:</strong>'),
        (r'\[!WARNING\]', '<strong>⚠️ Atenção:</strong>'),
    ]
    for pattern, replacement in inline_admonitions:
        html_content = re.sub(pattern, replacement, html_content)
    
    # 3. Convert absolute file:/// paths to relative paths
    html_content = re.sub(
        r'src="file:///[^"]*[/\\]imagens[/\\]([^"]+)"',
        r'src="../../assets/img/\1"',
        html_content
    )
    
    # 4. Remove governance links (file:/// links)
    html_content = re.sub(
        r'<a href="file:///[^"]*">([^<]+)</a>',
        r'\1',
        html_content
    )
    
    # 5. Remove leftover markdown image syntax with file:/// paths
    html_content = re.sub(
        r'<img[^>]*src="file:///[^"]*"[^>]*>',
        '',
        html_content
    )
    
    return metadata, html_content

def render_lab_v2_lesson(meta, body_html, prev_url, next_url):
    """Renderiza a lição usando o template do Lab V2."""
    template_path = os.path.join(TEMPLATE_DIR, "layout_lab_v2.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    guardian_name = meta.get("guardia", "Melquior").split(' ')[0]
    image_map = {
        "Melquior": "melquior-leao.webp",
        "Celeste": "celeste-raposa.webp",
        "Bernardo": "bernardo-urso.webp",
        "Íris": "iris-passarinho-colar.webp",
        "Noé": "noe-coruja.webp"
    }

    html = template
    html = html.replace("{{ titulo }}", meta.get("titulo", "Sem Título"))
    html = html.replace("{{ meta }}", meta.get("meta", ""))
    html = html.replace("{{ conteudo }}", body_html)
    html = html.replace("{{ fase }}", meta.get("fase", "Sementes"))
    html = html.replace("{{ guardia }}", meta.get("guardia", "Misterioso"))
    html = html.replace("{{ tempo }}", meta.get("tempo", "15 min"))
    html = html.replace("{{ tgtb }}", meta.get("tgtb", "N/A"))
    html = html.replace("{{ guardia_img }}", f"../../assets/img/{image_map.get(guardian_name, 'melquior-leao.webp')}")
    html = html.replace("{{ prev_url }}", prev_url)
    html = html.replace("{{ next_url }}", next_url)
    
    return html

def build_lab_v2_index(lessons):
    """Gera um index minimalista para o Lab V2."""
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lab v2: Imersão Naturalista | MatViva</title>
        <link rel="stylesheet" href="style_lab_v2.css">
        <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@700;900&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            .index-grid { 
                display: grid; 
                grid-template-columns: 1fr; 
                gap: 1.5rem; 
                margin-top: 3rem; 
            }
            .index-card { 
                background: var(--color-paper);
                padding: 2rem;
                border-radius: 8px;
                border-left: 4px solid var(--color-gold);
                text-decoration: none;
                color: var(--color-ink);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .index-card:hover {
                transform: translateX(8px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            }
            .index-card h3 {
                margin: 0 0 0.5rem;
                font-family: var(--font-ui);
                font-size: 1.2rem;
                color: var(--color-green);
            }
            .index-card p {
                margin: 0;
                font-size: 1rem;
                color: var(--color-ink-soft);
            }
        </style>
    </head>
    <body>
        <header class="lab2-header">
            <a href="../index.html">🏰 Reino</a>
            <span class="lab2-meta">LAB V2 • IMERSÃO</span>
        </header>

        <main class="lab2-content" style="max-width: 700px;">
            <div class="lab2-title-block" style="border-bottom: none; padding-bottom: 0;">
                <h1>Lab v2: Imersão Naturalista</h1>
                <p class="subtitle">Experiência de leitura fluida, como um livro.</p>
            </div>

            <div class="index-grid">
    """
    
    for l in lessons:
        html += f"""
            <a href="sementes/{l['html_filename']}" class="index-card">
                <h3>{l['meta'].get('titulo', 'Lição')}</h3>
                <p>{l['meta'].get('meta', 'Explore esta lição.')}</p>
            </a>
        """
        
    html += """
            </div>
        </main>
    </body>
    </html>
    """
    
    out_path = os.path.join(DIST_LAB_V2, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("🏠 [LAB-V2-INDEX] Index gerado.")

def main():
    print("📖 Gutenberg LAB V2 Engine (Imersão Naturalista)...")
    clean_lab_v2()
    copy_lab_v2_assets()
    
    files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.md")))
    lessons_data = []
    
    for f in files:
        meta, body = parse_markdown(f)
        filename = os.path.basename(f)
        html_filename = filename.replace('.md', '.html')
        lessons_data.append({
            "meta": meta,
            "body": body,
            "filename": filename,
            "html_filename": html_filename
        })
    
    for i, lesson in enumerate(lessons_data):
        prev_url = lessons_data[i-1]['html_filename'] if i > 0 else "../index.html"
        next_url = lessons_data[i+1]['html_filename'] if i < len(lessons_data)-1 else "#"
        
        final_html = render_lab_v2_lesson(lesson['meta'], lesson['body'], prev_url, next_url)
        
        out_path = os.path.join(DIST_LAB_V2_SEMENTES, lesson['html_filename'])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        
        print(f"✅ [LAB-V2] {lesson['html_filename']}")

    build_lab_v2_index(lessons_data)
    
    print("🚀 Lab V2 (Imersão Naturalista) Concluído!")

if __name__ == "__main__":
    main()
