"""
====================================================================================================
SAMOS DATAOPS: multi_modal.py
Integration: Universal Document Converter
Description: Converts PDF, Docx, Excel, Code, and Text files into the factory CSV format.
====================================================================================================
"""

import os
import pandas as pd
import glob
from datetime import datetime
from typing import Any

# Optional dependencies
try:
    import openpyxl  # pyright: ignore[reportMissingModuleSource]
except ImportError:
    openpyxl = None
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    from docx import Document
except ImportError:
    Document = None

class UniversalConverter:
    def __init__(self, raw_dir: str = "data/raw", bronze_file: str = "data/bronze_data.csv") -> None:
        self.raw_dir = raw_dir
        self.bronze_file = bronze_file
        os.makedirs(self.raw_dir, exist_ok=True)

    def extract_text_from_pdf(self, file_path: str) -> str:
        if not PyPDF2:
            return "[PyPDF2 Missing]"
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                if reader.is_encrypted:
                    return f"[Encrypted PDF: {os.path.basename(file_path)}]"
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            return f"[PDF Error: {e}]"
        return text

    def extract_text_from_docx(self, file_path: str) -> str:
        if not Document:
            return "[python-docx Missing]"
        try:
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"[DOCX Error: {e}]"

    def _process_single_file(self, file_path: str) -> dict[str, Any]:
        """Processes a single file based on its extension."""
        ext = os.path.splitext(file_path)[1].lower()
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / (1024 * 1024) # MB
        
        print(f"  📥 Converting: {filename} ({file_size:.2f} MB)")
        content = ""

        if ext in ['.txt', '.cpp', '.js', '.py', '.md'] and file_size > 50:
            content = self._handle_large_file(file_path, file_size)
        elif ext in ['.pdf']:
            content = self.extract_text_from_pdf(file_path)
        elif ext in ['.docx']:
            content = self.extract_text_from_docx(file_path)
        elif ext in ['.xlsx', '.xls']:
            content = self._handle_excel_file(file_path)
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

        return {
            "timestamp": datetime.now().isoformat(),
            "source_file": filename,
            "content_type": ext.replace('.', ''),
            "raw_content": content,
            "churn": 0, "user_id": 9999, "age": 0, "income": 0
        }

    def _handle_large_file(self, file_path: str, file_size: float) -> str:
        """Safely reads large files in chunks."""
        print(f"  ⚠️ Large file detected ({file_size:.2f} MB). Reading in chunks...")
        content = ""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                content += line
                if i > 100000:
                    content += "\n... [Content Truncated for Safety] ..."
                    break
        return content

    def _handle_excel_file(self, file_path: str) -> str:
        """Processes multi-sheet Excel files."""
        content = ""
        excel_data = pd.read_excel(file_path, sheet_name=None)
        for sheet, df_sheet in excel_data.items():
            content += f"--- Sheet: {sheet} ---\n"
            content += df_sheet.to_csv(index=False) + "\n"
        return content

    def convert_all(self) -> None:
        """Main entry point for multi-modal conversion."""
        print(f"🧩 SAMOS Multi-Modal: Scanning {self.raw_dir} for non-CSV sources...")
        
        extensions = ['*.pdf', '*.docx', '*.xlsx', '*.xls', '*.txt', '*.cpp', '*.js', '*.py', '*.md']
        files = []
        for ext in extensions:
            files.extend(glob.glob(os.path.join(self.raw_dir, ext)))

        if not files:
            print("✨ No multi-modal files found. System idle.")
            return

        all_data = []
        for file_path in files:
            try:
                record = self._process_single_file(file_path)
                all_data.append(record)
            except Exception as e:
                print(f"  ❌ Error converting {os.path.basename(file_path)}: {e}")

        if all_data:
            self._save_to_bronze(all_data)

    def _save_to_bronze(self, all_data: list[dict[str, Any]]) -> None:
        """Appends converted data to the bronze lake."""
        df_new = pd.DataFrame(all_data)
        if os.path.exists(self.bronze_file):
            df_existing = pd.read_csv(self.bronze_file)
            df_final = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_final = df_new
        df_final.to_csv(self.bronze_file, index=False)
        print(f"✅ Hardened Multi-modal integration complete. {len(all_data)} files fused.")

if __name__ == "__main__":
    converter = UniversalConverter()
    converter.convert_all()
