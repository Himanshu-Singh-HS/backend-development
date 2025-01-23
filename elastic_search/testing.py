import json
from bs4 import BeautifulSoup
def get_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)
    
def extract_text_from_markup(abstracts):
    extracted_texts = []
    for abstract in abstracts:
        markup = abstract.get('paragraph_markup', '')
        # Parse the HTML and extract plain text
        soup = BeautifulSoup(markup, 'html.parser')
        extracted_texts.append(soup.get_text().strip())
    return " ".join(extracted_texts)

def extract_claims_text(claims_section):
    """
    Extract and clean paragraph_markup content from claims in the given claims_section.
    
    :param claims_section: List containing claims dictionaries.
    :return: List of cleaned claims text.
    """
    claims_text = []
    # Safely access the first element of claims_section and its 'claims' field
    if claims_section and isinstance(claims_section, list) and len(claims_section) > 0:
        claims_data = claims_section[0].get('claims', [])
        for claim in claims_data:
            paragraph_markup = claim.get('paragraph_markup', '')
            if paragraph_markup:
                # Clean the HTML tags using BeautifulSoup
                soup = BeautifulSoup(paragraph_markup, 'html.parser')
                clean_text = soup.get_text().strip()
                claims_text.append(clean_text)
    return " ".join(claims_text)

data = get_data('elastic_search/US9289510B2.json')
ucids=data['patent_number']
print("this is ucids",ucids)
print()
print()
titles=data["titles"][0]['text']
print("this is titles ",titles)
print()
print()
abstracts=data['abstracts']
cleaned_abstracts = extract_text_from_markup(abstracts)
print("this is abstrxact",cleaned_abstracts,type(cleaned_abstracts))
print()
print()
descriptions=data['descriptions']
cleaned_abstracts = extract_text_from_markup(descriptions)
print("this is description",cleaned_abstracts)
print()
print()
claims=data['claims']
cleaned_claims=extract_claims_text(claims)
print("this is cliams ",cleaned_claims)





