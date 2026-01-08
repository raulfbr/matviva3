import os
import shutil
from pathlib import Path

# Try importing Pillow
try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("⚠️ [WARN] Pillow (PIL) não encontrado. As imagens serão apenas copiadas, não otimizadas.")

def optimize_images(source_dir, dest_dir, max_width=800, quality=80):
    """
    Otimiza imagens: Converte para WebP, redimensiona se necessário.
    """
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    # Garantir que destino existe
    dest_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🖼️ [IMG] Processando imagens de '{source_dir}' para '{dest_dir}'...")

    if not source_path.exists():
        print(f"❌ [ERR] Fonte não encontrada: {source_dir}")
        return

    count = 0
    saved_space = 0

    for file_path in source_path.glob('*'):
        if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
            output_filename = file_path.stem + ".webp"
            output_path = dest_path / output_filename
            
            # Se o arquivo de destino já existe e é mais recente que a fonte, PULA
            if output_path.exists():
                src_mtime = file_path.stat().st_mtime
                dst_mtime = output_path.stat().st_mtime
                if dst_mtime >= src_mtime:
                    # print(f"   -> [SKIP] {file_path.name} (Já otimizado)")
                    continue

            try:
                with Image.open(file_path) as img:
                    # Converter para RGB se for RGBA e salvar como JPG (não, WebP suporta transparência)
                    # WebP suporta RGBA.
                    
                    # Redimensionar se muito grande
                    if img.width > max_width:
                        ratio = max_width / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Salvar como WebP
                    img.save(output_path, 'WEBP', quality=quality)
                    
                    original_size = file_path.stat().st_size
                    new_size = output_path.stat().st_size
                    saved = original_size - new_size
                    saved_space += saved
                    
                    print(f"   -> [OPT] {file_path.name} -> {output_filename} ({new_size//1024}KB)")
                    count += 1
            except Exception as e:
                print(f"❌ [ERR] Falha ao processar {file_path.name}: {e}")
                # Fallback Copy
                shutil.copy(file_path, dest_path / file_path.name)

    if HAS_PILLOW:
        print(f"✨ [DONE] {count} imagens otimizadas. Economia: {saved_space//1024}KB.")
    else:
        print(f"✨ [DONE] Imagens copiadas sem otimização.")

if __name__ == "__main__":
    # Teste isolado
    SOURCE = "curriculo/_SISTEMA/imagens"
    DEST = "dist/assets/img"
    optimize_images(SOURCE, DEST)
