"""
Gutenberg Lab V3 Engine — 3 Zonas
Based on: matematica-viva.netlify.app reference

ZONES:
1. Preparação (Card): Objetivo, Materiais, Dica do Dia
2. Imersão (Fluida): Jornada → Hora de Fazer → Conversa → Despedida
3. Reflexão (Cards): O que você fez, Por que importa, Auditoria

FEATURES:
- H2 titles converted to scene markers (— Title —)
- Blockquote labels removed for fluidity
- "Hora de Fazer" sections get special wrapper
- Post-ritual sections get card treatment
"""

import os
import shutil
import markdown
import re
import glob
from datetime import datetime

# --- CONFIG LAB V3 ---
SOURCE_DIR = "curriculo/01_SEMENTES_TESTE"
TEMPLATE_DIR = "curriculo/_SISTEMA/TEMPLATES"
DIST_DIR = "dist"
DIST_LAB_V3 = os.path.join(DIST_DIR, "lab_v3")
DIST_LAB_V3_SEMENTES = os.path.join(DIST_LAB_V3, "sementes")

def clean_lab_v3():
    """Limpa apenas a pasta lab_v3."""
    if os.path.exists(DIST_LAB_V3):
        shutil.rmtree(DIST_LAB_V3, ignore_errors=True)
    os.makedirs(DIST_LAB_V3_SEMENTES, exist_ok=True)
    print(f"✨ [LAB-V3] Pasta {DIST_LAB_V3} limpa.")

def copy_lab_v3_assets():
    """Copia o CSS do Lab V3."""
    shutil.copy(os.path.join(TEMPLATE_DIR, "style_lab_v3.css"), os.path.join(DIST_LAB_V3, "style_lab_v3.css"))
    print(f"🎨 [LAB-V3] style_lab_v3.css copiado.")

def parse_markdown_v3(filepath):
    """Lê um arquivo MD e processa para estrutura de 3 zonas.
    
    NOVA ESTRUTURA (10/Jan/2026):
    - Seções 1-2: Zona 1 (preparação) - handled separately
    - Seções 3-10: hora-fazer (classe especial)
    - Seção 11: catedra-pais (classe especial)
    - Seção 12: auditoria (details colapsável)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract frontmatter
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

    # Convert markdown to HTML
    html_content = markdown.markdown(body_md, extensions=['fenced_code', 'tables', 'admonition'])
    
    # === ZONA PROCESSING ===
    
    # 1. Remove first H1 (duplicate of title)
    html_content = re.sub(r'^<h1[^>]*>.*?</h1>\s*', '', html_content, count=1)
    
    # 2. Process ALL admonition tags (remove them completely)
    inline_admonitions = [
        (r'\[!NOTE\]', ''),
        (r'\[!PAI\]', ''),
        (r'\[!NARRAÇÃO\]', ''),
        (r'\[!TIP\]', ''),
        (r'\[!IMPORTANT\]', ''),
        (r'\[!WARNING\]', ''),
        (r'\[!RITUAL\]', ''),
        (r'\[!MESTRA\]', ''),
        (r'\[!CONCEITO\]', ''),
        (r'\[!ATIVIDADE\]', ''),
        (r'\[!NARRATIVA\]', ''),
        (r'\[!FECHAMENTO\]', ''),
        (r'\[!AUDIO\]', ''),
        (r'\[!SE-QUISER-VOAR\]', ''),
    ]
    for pattern, replacement in inline_admonitions:
        html_content = re.sub(pattern, replacement, html_content)
    
    # 3. Convert markdown list asterisks to bullets
    html_content = re.sub(r'\*\s{2,}<strong>', '• <strong>', html_content)
    html_content = re.sub(r'^\*\s+', '• ', html_content, flags=re.MULTILINE)
    
    # 4. Convert checkboxes
    html_content = re.sub(r'\[\s*\]\s*<strong>', '☐ <strong>', html_content)
    html_content = re.sub(r'\[x\]\s*<strong>', '☑ <strong>', html_content)
    html_content = re.sub(r'\[\s*\]\s+', '☐ ', html_content)
    
    # 5. Clean file:/// paths and convert images
    html_content = re.sub(
        r'src="file:///[^"]*[/\\]imagens[/\\]([^"]+)"',
        r'src="../../assets/img/\1"',
        html_content
    )
    # Convert .png to .webp
    html_content = re.sub(r'\.png"', '.webp"', html_content)
    
    # Remove broken file:/// links
    html_content = re.sub(
        r'<a href="file:///[^"]*">([^<]+)</a>',
        r'\1',
        html_content
    )
    html_content = re.sub(
        r'<img[^>]*src="file:///[^"]*"[^>]*>',
        '',
        html_content
    )
    
    # 6. Remove HR (replaced by whitespace in CSS)
    html_content = re.sub(r'<hr\s*/?s*>', '', html_content)
    
    # 7. Process H2 sections for proper zone assignment
    # Sections 3-10 get scene-marker treatment and are inside hora-fazer
    # Section 11 gets catedra-pais wrapper
    # Section 12 stays as is (will go to details in template)
    
    h2_pattern = r'<h2>([^<]+)</h2>'
    
    # Find all H2 for analysis
    h2_matches = list(re.finditer(h2_pattern, html_content))
    
    # Define section markers
    section_markers = {
        '3': 'Ritual de Entrada',
        '4': 'A Jornada', 
        '5': 'A Ideia Viva',
        '6': 'Caminho Dourado',
        '7': 'Se Quiser Voar',
        '8': 'Momento de Conversa',
        '9': 'Despedida',
        '10': 'Ritual de Encerramento',
    }
    
    # Process from last to first to preserve indices
    for i, match in enumerate(reversed(h2_matches)):
        original_idx = len(h2_matches) - 1 - i
        h2_text = match.group(1)
        
        # Extract section number
        section_num = re.search(r'(\d+)\.', h2_text)
        section_id = section_num.group(1) if section_num else str(original_idx + 1)
        
        # Sections 3-10: Convert to scene markers (for hora-fazer)
        if section_id in ['3', '4', '5', '6', '7', '8', '9', '10']:
            clean_title = re.sub(r'^[^\s]+\s*\d*\.?\s*', '', h2_text).strip()
            scene_marker = f'<p class="scene-marker">— {clean_title} —</p>'
            html_content = html_content[:match.start()] + scene_marker + html_content[match.end():]
        
        # Section 11: Keep H2 but will be wrapped with catedra-pais
        elif section_id == '11' or 'importa' in h2_text.lower():
            # Will be handled by wrapper below
            pass
        
        # Section 12: Keep H2 (goes to auditoria)
        elif section_id == '12' or 'auditoria' in h2_text.lower():
            pass
        
        # Sections 1-2: Keep for Zona 1
        else:
            pass
    
    # 8. Wrap hora-fazer around sections 3-10
    # Find "Ritual de Entrada" scene marker and wrap from there to "Ritual de Encerramento"
    ritual_entrada_match = re.search(r'(<p class="scene-marker">— (?:O )?Ritual de Entrada[^<]*</p>)', html_content)
    ritual_encerramento_match = re.search(r'(<p class="scene-marker">— Ritual de Encerramento[^<]*</p>.*?</blockquote>)', html_content, re.DOTALL)
    
    if ritual_entrada_match and ritual_encerramento_match:
        start_pos = ritual_entrada_match.start()
        end_pos = ritual_encerramento_match.end()
        
        hora_fazer_content = html_content[start_pos:end_pos]
        html_content = (
            html_content[:start_pos] + 
            '<div class="hora-fazer">\n' + 
            hora_fazer_content + 
            '\n</div>' + 
            html_content[end_pos:]
        )
    
    # 9. Wrap catedra-pais around section 11
    catedra_match = re.search(r'(<h2>[^<]*(?:importa|Cátedra)[^<]*</h2>.*?)(?=<h2>|$)', html_content, re.DOTALL | re.IGNORECASE)
    if catedra_match:
        catedra_content = catedra_match.group(1)
        # Clean the H2 for catedra
        catedra_clean = re.sub(r'<h2>[^<]*11\.\s*', '<h2>🏛️ ', catedra_content)
        # Clean internal blockquote for cleaner UI (Box-in-Box removal)
        catedra_clean = re.sub(r'<blockquote>\s*', '', catedra_clean)
        catedra_clean = re.sub(r'\s*</blockquote>', '', catedra_clean)
        
        wrapped_catedra = f'<div class="catedra-pais">\n{catedra_clean}</div>'
        html_content = html_content[:catedra_match.start()] + wrapped_catedra + html_content[catedra_match.end():]
    
    return metadata, html_content

def render_lab_v3_lesson(meta, body_html, prev_url, next_url):
    """Renderiza a lição usando o template do Lab V3."""
    template_path = os.path.join(TEMPLATE_DIR, "layout_lab_v3.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # For v3, we use a simplified template approach
    # Just inject the processed content into the fluid zone
    html = template
    html = html.replace("{{ titulo }}", meta.get("titulo", "Sem Título"))
    html = html.replace("{{ meta }}", meta.get("meta", ""))
    html = html.replace("{{ fase }}", meta.get("fase", "Sementes"))
    html = html.replace("{{ guardia }}", meta.get("guardia", "Melquior"))
    html = html.replace("{{ tempo }}", meta.get("tempo", "15 min"))
    html = html.replace("{{ tgtb }}", meta.get("tgtb", "N/A"))
    
    # Placeholder content for structured parts
    html = html.replace("{{ objetivo }}", meta.get("meta", "Explorar a ideia viva do dia."))
    html = html.replace("{{ materiais }}", "Vela, sementes, Passaporte do Reino")
    html = html.replace("{{ dica_dia }}", "Respire fundo antes de começar. A jornada é curta, mas profunda.")
    
    # Main content goes to fluid zone
    html = html.replace("{{ conteudo_fluido }}", body_html)
    
    # Reflection cards (simplified for now)
    html = html.replace("{{ o_que_fez }}", "<ul><li>Apresentou a ideia viva de forma sensorial</li><li>Conectou matemática com narrativa</li></ul>")
    html = html.replace("{{ porque_importa }}", "<p>Charlotte Mason ensina que a criança aprende melhor quando toca o que estuda.</p>")
    html = html.replace("{{ auditoria }}", "<ul><li>☐ Atenção mantida</li><li>☐ Hábito respeitado</li><li>☐ Ideia Viva presente</li></ul>")
    
    html = html.replace("{{ prev_url }}", prev_url)
    html = html.replace("{{ next_url }}", next_url)
    
    return html

def build_lab_v3_index(lessons):
    """Gera um index para o Lab V3."""
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lab v3: 3 Zonas | MatViva</title>
        <link rel="stylesheet" href="style_lab_v3.css">
        <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@700;900&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            .index-grid { 
                display: grid; 
                grid-template-columns: 1fr; 
                gap: 1.5rem; 
                margin-top: 3rem; 
            }
            .index-card { 
                background: var(--color-card-bg);
                backdrop-filter: blur(10px);
                padding: 2rem;
                border-radius: 16px;
                border-left: 4px solid var(--color-gold);
                text-decoration: none;
                color: var(--color-ink);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .index-card:hover {
                transform: translateX(8px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.08);
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
            <span class="lab2-meta">LAB V3 • 3 ZONAS</span>
        </header>

        <main class="lab2-content" style="max-width: 700px;">
            <div class="lab2-title-block" style="border-bottom: none; padding-bottom: 0;">
                <h1>Lab v3: Redesign 3 Zonas</h1>
                <p class="subtitle">Preparação → Imersão → Reflexão</p>
            </div>

            <div class="index-grid">
    """
    
    for l in lessons:
        # Skip administrative files
        if l['filename'].startswith('ATA_') or l['filename'].startswith('LOG_'):
            continue
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
    
    out_path = os.path.join(DIST_LAB_V3, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("🏠 [LAB-V3-INDEX] Index gerado.")

def main():
    print("📖 Gutenberg LAB V3 Engine (3 Zonas)...")
    clean_lab_v3()
    copy_lab_v3_assets()
    
    files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.md")))
    lessons_data = []
    
    for f in files:
        meta, body = parse_markdown_v3(f)
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
        
        final_html = render_lab_v3_lesson(lesson['meta'], lesson['body'], prev_url, next_url)
        
        out_path = os.path.join(DIST_LAB_V3_SEMENTES, lesson['html_filename'])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        
        print(f"✅ [LAB-V3] {lesson['html_filename']}")

    build_lab_v3_index(lessons_data)
    
    print("🚀 Lab V3 (3 Zonas) Concluído!")

if __name__ == "__main__":
    main()
