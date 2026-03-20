import os
import re

def parse_description(content):
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = parts[1]
        desc_match = re.search(r'^description:\s*(?:>|\|)?\s*(.*?)(?=^[a-z_]+:|\Z)', frontmatter, re.MULTILINE | re.DOTALL)
        if desc_match:
            old_desc_block = desc_match.group(0)
            old_desc_text = desc_match.group(1).strip()
            
            # Clean up newlines in old text
            clean_text = re.sub(r'\s+', ' ', old_desc_text)
            
            # Extract logic
            trigger_text = ""
            not_trigger_text = ""
            
            # 1. Try to find explicit TRIGGER WHEN / DO NOT TRIGGER WHEN
            tw_match = re.search(r'(?i)TRIGGER (?:WHEN|on):\s*(.*?)(?=(?:DO NOT TRIGGER(?: WHEN)?|$))', clean_text)
            dntw_match = re.search(r'(?i)DO NOT TRIGGER(?: WHEN)?:\s*(.*)', clean_text)
            
            if tw_match: trigger_text = tw_match.group(1).strip()
            if dntw_match: not_trigger_text = dntw_match.group(1).strip()
            
            # 2. Try to find "Use when" or "Use PROACTIVELY when" or "Use this when"
            if not trigger_text:
                use_match = re.search(r'(?i)(?:Use PROACTIVELY when|Use when|Use this when|Trigger when|Trigger on)\s+(.*?)(?=(?:\. |$))', clean_text)
                if use_match:
                    trigger_text = use_match.group(1).strip()
                    
            if not not_trigger_text:
                not_use_match = re.search(r'(?i)(?:Do NOT use when|DO NOT TRIGGER when)\s+(.*?)(?=(?:\. |$))', clean_text)
                if not_use_match:
                    not_trigger_text = not_use_match.group(1).strip()

            # Default fallbacks
            if not trigger_text:
                trigger_text = "the user requires assistance with tasks related to this domain."
            if not not_trigger_text:
                not_trigger_text = "the task is outside the specific scope of this component."

            # Remove extracted sentences from main description
            main_desc = clean_text
            main_desc = re.sub(r'(?i)(?:Use PROACTIVELY when|Use when|Use this when|Trigger when:|Trigger on:|TRIGGER WHEN:)\s+.*?(?:\. |$)', '', main_desc)
            main_desc = re.sub(r'(?i)(?:Do NOT use when|DO NOT TRIGGER when:|DO NOT TRIGGER:)\s+.*?(?:\. |$)', '', main_desc)
            
            main_desc = main_desc.strip()
            if main_desc and not main_desc.endswith('.'):
                main_desc += '.'

            # Reconstruct
            new_desc_text = f"{main_desc}\nTRIGGER WHEN: {trigger_text}\nDO NOT TRIGGER WHEN: {not_trigger_text}"
            
            # YAML format
            lines = new_desc_text.split('\n')
            indented_desc = '\n  '.join(lines)
            
            new_desc_block = f"description: >\n  {indented_desc}\n"
            
            new_frontmatter = frontmatter.replace(old_desc_block, new_desc_block)
            return f"---{new_frontmatter}---{parts[2]}"
            
    return None

modified_count = 0
for root, _, files in os.walk('plugins'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it has 'description:' and it's not already standardized completely
                if content.startswith('---'):
                    if 'TRIGGER WHEN:' in content and 'DO NOT TRIGGER WHEN:' in content:
                        continue # Already formatted
                        
                    new_content = parse_description(content)
                    if new_content and new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        modified_count += 1
                        print(f"Updated: {filepath}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

print(f"Total modified files: {modified_count}")
