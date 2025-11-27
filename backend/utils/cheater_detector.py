import pdfplumber
import docx2txt
import os
import re
from docx import Document
from docx.shared import RGBColor

def extract_text_from_file(file_path):
    print(f"\n🔥🔥🔥 ANALYZING: {os.path.basename(file_path)} 🔥🔥🔥")
    
    text = ""
    is_suspicious = False
    hidden_count = 0
    
    extension = os.path.splitext(file_path)[1].lower()

    try:
        # ==========================================
        # 📄 LOGIC FOR PDF FILES
        # ==========================================
        if extension == '.pdf':
            print("--- SCANNING PDF LAYER ---")
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Filter Logic: checking char by char
                    chars_to_keep = []
                    
                    for char in page.chars:
                        is_hidden = False
                        
                        # 1. Size Check (< 6pt is suspicious)
                        if char.get('size', 0) < 6: 
                            is_hidden = True
                        
                        # 2. Color Check (White or Transparent)
                        color = char.get('non_stroking_color')
                        if color == (1, 1, 1) or color == 1: is_hidden = True # White
                        if isinstance(color, tuple) and len(color) == 3:
                            if all(c > 0.95 for c in color): is_hidden = True # Very bright/off-white

                        if is_hidden:
                            hidden_count += 1
                        else:
                            # Keep only visible chars for the Resume Parser
                            chars_to_keep.append(char)
                    
                    # Extract text only from the "clean" characters
                    page_text = pdfplumber.utils.extract_text(chars_to_keep, x_tolerance=2, y_tolerance=2)
                    if page_text:
                        text += page_text + "\n"

        # ==========================================
        # 📝 LOGIC FOR DOCX FILES
        # ==========================================
        elif extension == '.docx':
            print("--- SCANNING DOCX XML ---")
            
            # 1. Get Raw Text (We use docx2txt because it's robust for reading)
            # Note: For DOCX, it's hard to "delete" hidden text from the output string
            # accurately without breaking layout, so we extract ALL text but flag the user.
            text = docx2txt.process(file_path)
            
            # 2. Analyze Formatting (Using python-docx to find cheats)
            try:
                doc = Document(file_path)
                for paragraph in doc.paragraphs:
                    for run in paragraph.runs:
                        # Check A: Tiny Font (< 6pt)
                        # (run.font.size returns Emu units, we convert to Pt)
                        if run.font.size and run.font.size.pt < 6:
                            print(f"   [!] Found Tiny Font: {run.font.size.pt}pt")
                            hidden_count += 5 # Add weight
                        
                        # Check B: White Color (Hex FFFFFF)
                        if run.font.color and run.font.color.rgb == RGBColor(255, 255, 255):
                            print(f"   [!] Found White Text")
                            hidden_count += 10
                            
                        # Check C: The specific "Hidden" attribute in Word
                        if run.font.hidden:
                            print(f"   [!] Found 'Hidden' Attribute")
                            hidden_count += 10
            except Exception as docx_e:
                print(f"Warning: Could not analyze DOCX styles: {docx_e}")

        else:
            return None, False
        
        # ==========================================
        # 🏁 FINAL DECISION
        # ==========================================
        print(f"--- TOTAL SUSPICIOUS SCORE: {hidden_count} ---")
        
        # If we found enough evidence, mark it
        if hidden_count > 10:
            is_suspicious = True
            print("🚨 MALPRACTICE DETECTED: Flagged as Suspicious 🚨")
        else:
            print("✅ File looks clean.")
        
        # Final Cleanup
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text, is_suspicious

    except Exception as e:
        print(f"Error extracting text: {e}")
        return None, False