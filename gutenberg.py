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
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_SEMENTES)
    print(f"🧹 [CLEAN] Pasta {DIST_DIR} recriada.")

def copy_assets():
    """Copia o CSS e Assets."""
    shutil.copy(os.path.join(TEMPLATE_DIR, "style.css"), os.path.join(DIST_DIR, "style.css"))
    # Copiar Assets (Se existirem - placeholder por enquanto)
    # shutil.copytree("assets", os.path.join(DIST_DIR, "assets"))
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
    
    # Processar Admonitions Customizados do Reino (ex: > [!RITUAL])
    # Simples replace para transformar em blockquotes estilizados
    html_content = html_content.replace("<blockquote>\n<p>[!RITUAL]", "<blockquote class='ritual'>\n<p><strong>🕯️ RITUAL</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!MESTRA]", "<blockquote class='mestra'>\n<p><strong>👩‍🏫 MESTRA</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!NARRATIVA]", "<blockquote class='narrativa'>\n<p><strong>📖 NARRATIVA</strong>")
    html_content = html_content.replace("<blockquote>\n<p>[!ATIVIDADE]", "<blockquote class='atividade'>\n<p><strong>🛠️ ATIVIDADE</strong>")
    
    return metadata, html_content

def build_lesson(filename):
    """Constrói uma única lição."""
    filepath = os.path.join(SOURCE_DIR, filename)
    metadata, body_html = parse_markdown(filepath)
    
    # Filtro de Versão (Apenas V3.6+ e Canônico)
    # version = metadata.get("versao", "0")
    # if "3.6" not in version or metadata.get("status") != "Canônico":
    #     print(f"⏩ [SKIP] {filename} (Versão: {version})")
    #     return None

    # Ler Template Base
    with open(os.path.join(TEMPLATE_DIR, "layout_base.html"), "r", encoding="utf-8") as f:
        template = f.read()
    
    # Injetar Dados (Jinja2 primitivo com replace)
    output_html = template
    output_html = output_html.replace("{{ titulo }}", metadata.get("titulo", "Sem Título"))
    output_html = output_html.replace("{{ fase }}", metadata.get("fase", "Sementes"))
    output_html = output_html.replace("{{ meta }}", metadata.get("meta", ""))
    output_html = output_html.replace("{{ guardia }}", metadata.get("guardia", "Misterioso"))
    output_html = output_html.replace("{{ tempo }}", metadata.get("tempo", "15 min"))
    output_html = output_html.replace("{{ local }}", metadata.get("local", "O Reino"))
    output_html = output_html.replace("{{ versao }}", metadata.get("versao", "3.6"))
    output_html = output_html.replace("{{ conteudo }}", body_html)
    
    # Salvar
    output_filename = filename.replace(".md", ".html")
    with open(os.path.join(DIST_SEMENTES, output_filename), "w", encoding="utf-8") as f:
        f.write(output_html)
        
    print(f"✅ [BUILD] {output_filename}")
    
    metadata['filename'] = output_filename
    return metadata

def build_index(lessons):
    """Constrói a página inicial."""
    with open(os.path.join(TEMPLATE_DIR, "layout_index.html"), "r", encoding="utf-8") as f:
        template = f.read()

    # Construir lista de cards (Lógica Jinja2 simulada)
    # O template espera {% for %} mas nosso script é simples.
    # Vamos recriar o bloco de cards manualmente.
    
    cards_html = ""
    for licao in lessons:
        card = f"""
        <a href="sementes/{licao['filename']}" class="card">
            <span style="font-size: 0.8rem; text-transform: uppercase; color: var(--color-green); font-weight: bold;">{licao.get('id', '???')}</span>
            <h3>{licao.get('titulo')}</h3>
            <p style="font-size: 0.95rem; color: #555;">{licao.get('meta')}</p>
            <div class="meta">
                <span>🛡️ {licao.get('guardia')}</span>
                <span>⏱️ {licao.get('tempo')}</span>
            </div>
        </a>
        """
        cards_html += card

    # Replace no template (Hack para substituir o bloco jinja)
    # Assumindo que o template tem um placeholder ou vamos substituir o bloco todo
    # Como escrevi o template com Jinja, vou usar regex para substituir o bloco.
    
    pattern = r"{% for licao in licoes %}(.*?){% endfor %}"
    # Não vamos usar regex complexo. Vamos simplesmente substituir um placeholder que vou criar agora se não existir.
    # Mas como já escrevi o arquivo com {% %}, vou sobrescrever o arquivo na memória.
    
    # Recarregando template como string crua
    final_index = template
    # Remover o loop Jinja
    final_index = re.sub(pattern, cards_html, final_index, flags=re.DOTALL)
    
    final_index = final_index.replace("{{ data_build }}", datetime.now().strftime("%d/%m/%Y %H:%M"))

    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_index)
    
    print(f"🏠 [INDEX] Home page gerada com {len(lessons)} lições.")

def main():
    print("🦁 Iniciando Gutenberg Engine v1.0...")
    clean_dist()
    copy_assets()
    
    lessons = []
    
    # Ler pasta Sementes
    files = sorted(os.listdir(SOURCE_DIR))
    for filename in files:
        if filename.endswith(".md"):
            # Ignorar templates e drafts se houver
            meta = build_lesson(filename)
            if meta:
                lessons.append(meta)
    
    build_index(lessons)
    print("🚀 Build Concluído! Pasta /dist pronta para deploy.")

if __name__ == "__main__":
    main()
