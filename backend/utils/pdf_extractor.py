import pdfplumber
import docx2txt
import os
import re

def extract_text_from_file(file_path):
    text = ""
    is_suspicious = False
    hidden_char_count = 0
    
    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                # --- DEBUGGING START ---
                print(f"\n\n--- DEBUGGING PDF: {os.path.basename(file_path)} ---")
                
                # We inspect the first page to see what the "Hidden" text looks like
                if len(pdf.pages) > 0:
                    first_page = pdf.pages[0]
                    print("--- INSPECTING FIRST 500 CHARACTERS ---")
                    for i, char in enumerate(first_page.chars):
                        if i > 500: break # Stop after 500 chars to keep log readable
                        
                        # Print details of ANY character that looks small or white
                        # (Size < 9 OR Color is white/near-white)
                        size = char.get('size', 0)
                        color = char.get('non_stroking_color')
                        
                        # Check if it looks suspicious (just for printing to terminal)
                        looks_suspicious = False
                        if size < 9: looks_suspicious = True
                        if color == (1, 1, 1) or color == 1: looks_suspicious = True
                        
                        if looks_suspicious:
                            print(f"SUSPICIOUS CHAR: '{char['text']}' | Size: {size} | Color: {color}")
                # --- DEBUGGING END ---

                # Actual Extraction Logic
                for page in pdf.pages:
                    chars_to_keep = []
                    
                    for char in page.chars:
                        is_hidden = False
                        size = char.get('size', 0)
                        color = char.get('non_stroking_color')

                        # 1. Check Size (Threshold: 8pt)
                        if size < 8:
                            is_hidden = True
                            
                        # 2. Check Color (White or Transparent)
                        # (1, 1, 1) is RGB White. 1 is Grayscale White.
                        if color == (1, 1, 1) or color == 1:
                            is_hidden = True
                        
                        # Check for off-white (e.g. 0.99, 0.99, 0.99)
                        if isinstance(color, tuple) and len(color) == 3:
                            if all(c > 0.95 for c in color): # Very bright/white
                                is_hidden = True

                        if is_hidden:
                            hidden_char_count += 1
                        else:
                            chars_to_keep.append(char)
                    
                    # Extract text using only the "Visible" characters
                    page_text = pdfplumber.utils.extract_text(chars_to_keep, x_tolerance=2, y_tolerance=2)
                    if page_text:
                        text += page_text + "\n"
            
            print(f"--- TOTAL HIDDEN CHARS FOUND: {hidden_char_count} ---")
            print("---------------------------------------------------\n")
            
            # Threshold to flag as suspicious
            if hidden_char_count > 10:
                is_suspicious = True

        elif extension == '.docx':
            text = docx2txt.process(file_path)
        else:
            return None, False
        
        # Cleanup text
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text, is_suspicious

    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None, False