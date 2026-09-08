import os

STORAGE_DIR = os.environ.get('PDF_STORAGE_DIR', 'storage/applications')

def save_pdf(filename, pdf_bytes):
    os.makedirs(STORAGE_DIR, exist_ok=True)
    file_path = os.path.join(STORAGE_DIR, filename)
    with open(file_path, 'wb') as f:
        f.write(pdf_bytes)
    
    return file_path

