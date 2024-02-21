import re

def extract_references(tex_file):
    references = {'parencite': [], 'textcite': []}
    
    with open(tex_file, 'r') as file:
        tex_content = file.read()
        
        # Extract references using regular expressions
        parencite_refs = re.findall(r'\\parencite\{([^}]*)\}', tex_content)
        textcite_refs = re.findall(r'\\textcite\{([^}]*)\}', tex_content)
        
        references['parencite'] = parencite_refs
        references['textcite'] = textcite_refs
        
    references = list(set(references['parencite'] + references['textcite']))
    return references


def parse_bib_file(bib_file):
    references = {}
    
    with open(bib_file, 'r') as file:
        bib_content = file.read()
        
        # Split content into individual references
        bib_references = bib_content.split('@')
        
        for ref in bib_references[1:]:
            # Extract reference key
            key = ref.strip().split("{", 1)[1].split(",", 1)[0]
            
            # Store the whole reference
            references[key] = f"@{ref}"
        
    return references

def get_reference_info(bib_file, keys):
    references = {}
    
    with open(bib_file, 'r') as file:
        bib_content = file.read()
        
        # Split content into individual references
        bib_references = re.split(r'@(\w+)\{([^,]+),\n', bib_content)
        # print(bib_references[:5])
        for i in range(1, len(bib_references), 3):
            # Extract reference key
            key = bib_references[i+1].strip()
            
            # If the key is in the list of keys extracted from the tex file, add it to references
            if key in keys:
                references[key] = f"@{bib_references[i]}{bib_references[i+1]},{bib_references[i+2]}"
    
    return references

def save_first_five_references(bib_references, output_file):
    with open(output_file, 'w') as file:
        count = 0
        for key, info in bib_references.items():
            file.write(info + "\n\n")
            count += 1
            if count == 5:
                break\
                

def save_all_references(bib_references, output_file):
    with open(output_file, 'w') as file:
        for info in bib_references.values():
            file.write(info + "\n\n")


if __name__ == "__main__":

    tex_file = "main.tex"  # Replace with the path to your .tex file
    bib_file = "library.bib"  # Replace with the path to your .bib file
    
    # Extract references from the .tex file
    extracted_references = extract_references(tex_file)
    print(extracted_references)
    
    # Parse the .bib file
    bib_references = parse_bib_file(bib_file)

    print(bib_references.keys(), bib_references.items())

    
    # # Retrieve information for each reference
    parencite_info = get_reference_info(bib_file, extracted_references)
    # textcite_info = get_reference_info(bib_references, extracted_references['textcite'])
    
    # print("Information for references extracted from \\parencite:")
    # for key, info in parencite_info.items():
    #     print(f"{key}: {info}")
        
    # print("\nInformation for references extracted from \\textcite:")
    # for key, info in textcite_info.items():
    #     print(f"{key}: {info}")
    final_references_keys = [ref for ref in bib_references.keys() if ref in extracted_references]
    final_references = {key: bib_references[key] for key in final_references_keys}
    
    output_file = "all_references.bib"
    save_all_references(final_references, output_file)