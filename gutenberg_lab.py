import os
import shutil
import markdown
import re
import glob
from datetime import datetime

# --- CONFIG LAB ---
SOURCE_DIR = "curriculo/01_SEMENTES_TESTE"
TEMPLATE_DIR = "curriculo/_SISTEMA/TEMPLATES"
DIST_DIR = "dist"
DIST_LAB = os.path.join(DIST_DIR, "lab")
DIST_LAB_SEMENTES = os.path.join(DIST_LAB, "sementes")

def clean_lab():
    """Limpa apenas a pasta lab."""
    if os.path.exists(DIST_LAB):
        shutil.rmtree(DIST_LAB, ignore_errors=True)
    os.makedirs(DIST_LAB_SEMENTES, exist_ok=True)
    print(f"✨ [LAB] Pasta {DIST_LAB} limpa.")

def copy_lab_assets():
    """Copia o CSS do Laboratório."""
    shutil.copy(os.path.join(TEMPLATE_DIR, "style_lab.css"), os.path.join(DIST_LAB, "style_lab.css"))
    print(f"🎨 [LAB] style_lab.css copiado.")

def parse_markdown(filepath):
    """Lê um arquivo MD e extrai Frontmatter e Conteúdo (Reusado do Gutenberg)."""
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

    # Admonition processing logic
    replacements = {
        "[!RITUAL]": ("ritual", "🕯️ RITUAL"),
        "[!MESTRA]": ("mestra", "👩‍🏫 MESTRA"),
        "[!NARRATIVA]": ("narrativa", "📖 NARRATIVA"),
        "[!ATIVIDADE]": ("atividade", "🛠️ ATIVIDADE"),
        "[!CONCEITO]": ("conceito", "💡 CONCEITO"),
        "[!TIP]": ("tip", "🦋 SE QUISER VOAR"),
        "[!NOTE]": ("note", "📝 NOTA"),
        "[!IMPORTANT]": ("important", "⚠️ IMPORTANTE"),
        "[!MATERIAL]": ("material-card", "🎒 MATERIAL NECESSÁRIO"),
        "[!FECHAMENTO]": ("fechamento", "🏁 FECHAMENTO"),
        "[!PAI]": ("pai-action", "👨‍👧 AÇÃO DO PAI")
    }

    # Pre-process MD to handle custom admonitions before markdown conversion
    # or handle after HTML. Let's do after HTML for consistency with gutenberg.py
    html_content = markdown.markdown(body_md, extensions=['fenced_code', 'tables', 'admonition'])
    
    for tag, (cls, title) in replacements.items():
        pattern = r"(<blockquote>\s*<p>)" + re.escape(tag)
        replacement = f"<blockquote class='{cls}'>\n<p><strong>{title}</strong>"
        html_content = re.sub(pattern, replacement, html_content)
    
    return metadata, html_content

def render_lab_lesson(meta, body_html, prev_url, next_url):
    """Renderiza a lição usando o template do Laboratório."""
    template_path = os.path.join(TEMPLATE_DIR, "layout_lab.html")
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
    
    # Path to images: dist/lab/sementes/file.html -> ../../assets/img/
    html = html.replace("{{ guardia_img }}", f"../../assets/img/{image_map.get(guardian_name, 'melquior-leao.webp')}")
    
    html = html.replace("{{ prev_url }}", prev_url)
    html = html.replace("{{ next_url }}", next_url)
    
    return html

def build_lab_index(lessons):
    """Gera um index simplificado para o Laboratório."""
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Laboratório de Design | MatViva</title>
        <link rel="stylesheet" href="../style.css">
        <style>
            body { background: #fdfbf7; padding: 2rem; font-family: sans-serif; }
            .lab-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem; margin-top: 2rem; }
            .lab-card { background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #eee; text-decoration: none; color: #333; transition: all 0.2s; }
            .lab-card:hover { border-color: #C5A059; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
            .badge { background: #E6D2A8; color: #2A3B33; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; }
        </style>
    </head>
    <body>
        <a href="../index.html" style="color: #666; text-decoration: none;">← Voltar ao Reino</a>
        <h1 style="color: #2A3B33; margin-top: 1rem;">🧪 Laboratório de Design NEXT</h1>
        <p>Experimentando o novo layout Glassmorphism para a Fase Sementes.</p>
        
        <div class="lab-grid">
    """
    
    for l in lessons:
        html += f"""
        <a href="sementes/{l['html_filename']}" class="lab-card">
            <span class="badge">SEMENTES</span>
            <h3 style="margin: 0.5rem 0;">{l['meta'].get('titulo', 'Lição')}</h3>
            <p style="font-size: 0.85rem; color: #666; margin: 0;">{l['meta'].get('meta', '')}</p>
        </a>
        """
        
    html += """
        </div>
    </body>
    </html>
    """
    
    out_path = os.path.join(DIST_LAB, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("🏠 [LAB-INDEX] Index do Laboratório gerado.")

def main():
    print("🔬 Gutenberg LAB NEXT Engine v1.0...")
    clean_lab()
    copy_lab_assets()
    
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
        
        final_html = render_lab_lesson(lesson['meta'], lesson['body'], prev_url, next_url)
        
        out_path = os.path.join(DIST_LAB_SEMENTES, lesson['html_filename'])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        
        print(f"✅ [LAB-LESSON] {lesson['html_filename']}")

    # Build LAB Index
    build_lab_index(lessons_data)
    
    print("🚀 Laboratório de Design Atualizado!")

if __name__ == "__main__":
    main()
