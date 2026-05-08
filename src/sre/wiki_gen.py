import os

def generate_model_wiki():
    """Phase 25: Knowledge Management - Model Wiki Generator."""
    print("📚 Phase 25: Evolving the Model Intelligence Wiki...")
    
    wiki_content = ["# 📖 Global Model Intelligence Wiki\n"]
    wiki_content.append("## 🏗️ Table of Contents\n")
    
    model_cards = []
    if os.path.exists("models"):
        for file in os.listdir("models"):
            if file.endswith(".md"):
                model_cards.append(file)
                
    for card in model_cards:
        wiki_content.append(f"- [{card}](#{card.replace('.', '').lower()})")
        
    wiki_content.append("\n---\n")
    
    for card in model_cards:
        wiki_content.append(f"## 📄 {card}\n")
        with open(f"models/{card}", "r") as f:
            wiki_content.append(f.read())
        wiki_content.append("\n---\n")
        
    with open("MODEL_WIKI.md", "w") as f:
        f.write("\n".join(wiki_content))
        
    print("✅ Model Wiki evolved: MODEL_WIKI.md")

if __name__ == "__main__":
    generate_model_wiki()
