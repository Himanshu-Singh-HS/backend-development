r"""src/monolith/file_generator/drafting_export.py"""

# importing standard modules ==================================================
from typing import List, Dict, Any
import re,json
import pdfkit
 
config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')  

def extract_claims(claims_data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Extract independent, dependent claims and their figures for method and system claims."""
    sys_ind_claims, sys_dep_claims, sys_figs = [], [], []
    met_ind_claims, met_dep_claims, met_figs = [], [], []

    for claim in claims_data:
        claim_type = claim.get("claim_type")
        tag = claim.get("tag")
        text = claim.get("text", "")
        index = claim.get("index", "")
        latex_details = claim.get("generated_figures_data", {}) or {}
        latex_details = latex_details.get("latex_details", [])

        figs = [
            url
            for latex_detail in latex_details
            if latex_detail.get("images_urls", [])
            for url in latex_detail.get("images_urls", [])
        ]
        text = f"{index}. {text}"

        if claim_type == "method":
            if tag == "dependent":
                met_dep_claims.append(text)
            elif tag == "independent":
                met_ind_claims.append(text)
            if figs:
                met_figs.extend(figs)

        elif claim_type == "system":
            if tag == "dependent":
                sys_dep_claims.append(text)
            elif tag == "independent":
                sys_ind_claims.append(text)
            if figs:
                sys_figs.extend(figs)

    return {
        "sys_ind_claims": sys_ind_claims,
        "sys_dep_claims": sys_dep_claims,
        "sys_figs": sys_figs,
        "met_ind_claims": met_ind_claims,
        "met_dep_claims": met_dep_claims,
        "met_figs": met_figs,
    }

 
def extract_description(description_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Extract method, system, and invention descriptions."""
    method_desc, system_desc, invention_desc = [], [], []

    for key, value in description_data.items():
        if key == "method_desc":
            method_desc.extend(value.get("text", "").split("\n\n"))
        elif key == "system_desc":
            system_desc.extend(value.get("text_list", []))
        elif key == "invention_desc":
            invention_desc.extend(value.get("text", "").split("\n\n"))

    return {
        "method_desc": method_desc,
        "system_desc": system_desc,
        "invention_desc": invention_desc,
    }


 
def extract_list_of_figures(list_of_figures_data: Any) -> List[str]:
    """Extract list of figures."""
    if isinstance(list_of_figures_data, list):
        return list_of_figures_data
    return []


 
def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process the entire data set to extract claims, descriptions, and list of figures."""
    result = {
        "sys_ind_claims": [],
        "sys_dep_claims": [],
        "sys_figs": [],
        "met_ind_claims": [],
        "met_dep_claims": [],
        "met_figs": [],
        "method_desc": [],
        "system_desc": [],
        "invention_desc": [],
        "list_of_figures": [],
    }

    for key, value in data.items():
        if key == "description":
            desc_result = extract_description(value)
            result.update(desc_result)
        elif key == "claims":
            claims_result = extract_claims(value)
            result.update(claims_result)
        elif key == "list_of_figures":
            result["list_of_figures"] = extract_list_of_figures(value)
        elif isinstance(value, dict):
            result[key] = value.get("text", "").split("\n\n")
        else:
            result[key] = value.split("\n\n")

    return result


def generate_numbered_html_section(
    start_number: int, field_data_heading: str, field_data: list
) -> tuple:
    """
    Generates an HTML section with a heading and a list of items formatted with numbered paragraphs.
    Also returns the updated start number after processing all items.

    Args:
        start_number (int): The starting number for the list.
        field_data_heading (str): The heading text to be displayed.
        field_data (list): The list of items to be included in the HTML.

    Returns:
        tuple: A tuple containing:
            - str: The generated HTML section.
            - int: The updated start number.
    """
    heading = f"<p><b><span >{field_data_heading}</span></b></p>"
    if field_data_heading in {"ABSTRACT", "CLAIMS"}:
        heading = f'<p style="text-align:center;" ><b><span >{field_data_heading}</span></b></p>'

    if field_data_heading in {"FIGURES", "CLAIMS", "ABSTRACT"}:
        page_break = '<div style="page-break-before: always;"></div>'
        heading = page_break + heading

    if field_data_heading == "FIGURES":
        image_tags = "".join(
            f'<a href={fig} download="fig" > <img style="display: block; margin-left: auto; margin-right: auto; width: 60%;" src="{fig}" alt="Figure"></a>'
            for fig in field_data
        )
        html_section = heading + image_tags
        updated_start_number = start_number
    elif field_data_heading == "CLAIMS":

        def format_claims(field_data):
            formatted_claims = []
            for claim in field_data:
                split_claims = re.split(r",\s*and\s*|[;:]", claim)
                if split_claims:
                    formatted_claims.append(
                        f"<p>&nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;{split_claims[0]}</p>"
                    )
                    for claim_text in split_claims[1:]:
                        formatted_claims.append(f"<p>{claim_text}</p>")
            return "".join(formatted_claims)

        claim_body = f"""<div >
                {heading}
                <p><span
                        >What is claimed is: </span></p>
                   {format_claims(field_data)}
                
            </div>"""
        html_section = claim_body
        updated_start_number = start_number
    else:
        is_abstract = True if field_data_heading == "ABSTRACT" else False
        formatted_p_tags = [
            f'<p><b><span >{f"[{str(start_number + i).zfill(4)}]&nbsp;" if not is_abstract else "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"}</span></b>'
            f"<b></b>"
            f"<span >{item}</span></p>"
            for i, item in enumerate(field_data)
        ]
        html_section = heading + "".join(formatted_p_tags)
        updated_start_number = start_number + len(field_data)

    return html_section, updated_start_number

def generate_final_html(data) -> str:
    """
    Combines all HTML sections into a final HTML document.

    Args:
        fields (list): A list of dictionaries where each dictionary contains:
            - 'heading': The heading text.
            - 'data': The list of items to be included in the HTML.

    Returns:
        str: The final HTML document.
    """
    keys_to_exclude = {
        "insert_timestamp",
        "last_update_timestamp",
        "_id",
        "user_id",
        "search_id",
        "components",
        "id",
        "status",
    }

    filtered_dict = {k: v for k, v in data.items() if k not in keys_to_exclude}

    processed_data = process_data(filtered_dict)
    css_styles = """
    <style>
         @page {
            size: A4;
            margin: 25.4mm;
        }
        body {
            font-family: 'Times New Roman', serif;
            font-size: 20px;
        }
   
        p{
            text-align:justify;
            line-height:1.8;
            
        }
        
    </style>
    """

    fields = [
        {
            "heading": "BACKGROUND",
            "data": processed_data.get("technical_field", "")
            + processed_data.get("background", ""),
        },
        {"heading": "BRIEF SUMMARY", "data": processed_data.get("summary", [])},
        {
            "heading": "BRIEF DESCRIPTION OF THE SEVERAL VIEWS OF THE DRAWINGS",
            "data": processed_data.get("list_of_figures", []),
        },
        {
            "heading": "DETAILED DESCRIPTION",
            "data": processed_data.get("method_desc", [])
            + processed_data.get("system_desc", [])
            + processed_data.get("invention_desc", []),
        },
        {
            "heading": "CLAIMS",
            "data": processed_data.get("sys_ind_claims", [])
            + processed_data.get("sys_dep_claims", [])
            + processed_data.get("met_ind_claims", [])
            + processed_data.get("met_dep_claims", []),
        },
        {"heading": "ABSTRACT", "data": processed_data.get("abstract", "")},
        {
            "heading": "FIGURES",
            "data": processed_data.get("met_figs", [])
            + processed_data.get("sys_figs", []),
        },
    ]
    start_number = 1
    html_sections = []

    for field in fields:
        html_section, start_number = generate_numbered_html_section(
            start_number, field["heading"], field["data"]
        )
        html_sections.append(html_section)

    title_html = f"""<p style="text-align:center;"><b><span>{processed_data.get('title', 'Document')[0].upper()}</span></b></p>"""
    final_html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title></title>{css_styles}</head><body>"""
    final_html += title_html

    for i, section in enumerate(html_sections):
        final_html += section

    final_html += "</body></html>"

    return final_html
 

# Generate and save PDF
def save_pdf_from_html(html_content, output_filename="output.pdf"):
    pdfkit.from_string(html_content, output_filename, configuration=config)
    print("PDF generated successfully.")

# Load JSON data from a file
def json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

data = json_data("./eP-pdf/ep.json")
result=generate_final_html(data)
save_pdf_from_html(result) 

