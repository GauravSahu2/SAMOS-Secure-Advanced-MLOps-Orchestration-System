"""
====================================================================================================
FILE: src/ml_ops/memory.py
ROLE: The Neural Memory Engine (Offline RAG)
TRIGGER: Triggered by src/sre/serve.py during 'predict' calls.
====================================================================================================
"""

import os            # Imports OS for directory and file path management.
import json          # Imports JSON to manage the persistent 'vault' storage.
import hashlib       # Imports Hashlib to create unique IDs for memory entries.
from typing import List, Dict # Type hinting for High-Assurance code quality.

# 📂 STORAGE LOCATIONS
MEMORY_DIR = "memory"                    # Directory where memory is archived.
MEMORY_FILE = os.path.join(MEMORY_DIR, "neural_vault.json") # The physical Brain file.

class NeuralMemory:
    """Handles the long-term knowledge persistence for the SAMOS Swarm."""
    
    def __init__(self):
        # [TRIGGER] Checks if the directory exists, creates it if not.
        if not os.path.exists(MEMORY_DIR):
            os.makedirs(MEMORY_DIR)
        
        # [TRIGGER] Calls _load_vault() to bring knowledge into RAM.
        self.vault = self._load_vault()

    def _load_vault(self) -> List[Dict]:
        """Reads the knowledge vault from the local disk."""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f) # Decodes JSON into a Python list.
        return [] # Returns empty list if vault is new.

    def save_to_vault(self, text: str, source: str = "user_interaction"):
        """Commits a new memory entry to the offline storage."""
        # Create a unique SHA256 hash ID for this memory block.
        entry_id = hashlib.sha256(text.encode()).hexdigest()
        
        # Build the memory data structure.
        entry = {
            "id": entry_id,
            "content": text,
            "source": source
        }
        
        self.vault.append(entry) # Add to RAM cache.
        
        # [TRIGGER] Writes the updated vault back to 'memory/neural_vault.json'.
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.vault, f, indent=4)
        
        print(f"🧠 [MEMORY] Synced entry: {entry_id[:8]}")

    def search_vault(self, query: str) -> str:
        """Recalls context using local keyword matching (Offline RAG)."""
        # [TRIGGER] Iterates through self.vault entries to find relevant matches.
        query_words = set(query.lower().split()) # Normalize query for search.
        for entry in self.vault:
            # Simple intersection check for offline efficiency.
            if query_words.intersection(set(entry["content"].lower().split())):
                # If a match is found, return the memory content as context.
                return f"--- RECALLED MEMORY ---\n{entry['content']}\n-----------------------"
        return "" # Return empty if no knowledge matches.
