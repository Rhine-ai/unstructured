from fastapi import FastAPI, File, UploadFile
from unstructured.partition.auto import partition

app = FastAPI()

def elements_to_markdown(elements):
    """
    Convert a list of document elements into a Markdown-formatted string.

    This function takes a list of elements (each typically representing a portion
    of text extracted from a document) and converts them into nicely formatted Markdown.
    Different element types (headers, titles, code snippets, etc.) are handled and
    formatted differently for improved readability.

    Args:
        elements (list): List of document elements obtained from the partition function.
                         Each element is expected to have at least a 'type' and 'text' attribute.
                         Metadata may also be present.

    Returns:
        str: A string containing the Markdown-formatted content.
    """

    # Define formatting functions for each element type.
    # Each function takes the element text and returns a Markdown-formatted string.
    def format_title(text):
        return f"# {text}"

    def format_header(text):
        # Consider using `##` for headers. Adjust as needed if you have multiple levels.
        return f"## {text}"

    def format_list_item(text):
        return f"- {text}"

    def format_code(text):
        # Wrap code snippets in triple backticks for Markdown code blocks.
        return f"```\n{text}\n```"

    def format_table(text):
        # For now, just return the text. You could improve this by converting to a Markdown table if possible.
        return text

    def format_figure_caption(text):
        return f"*Figure: {text}*"

    def format_formula(text):
        # Wrap formula in LaTeX-style math delimiters.
        return f"$$\n{text}\n$$"

    def format_address(text):
        # Use a blockquote style for addresses.
        return f"> {text}"

    def format_email_address(text):
        # Inline code format for emails, or could use a mailto link if desired.
        return f"`{text}`"

    def format_image(text):
        # If text contains a URL or image name, you might improve the formatting here.
        return f"![Image]({text})"

    def format_page_break(_):
        # A horizontal rule to denote a page break.
        return "---"

    def format_footer(text):
        return f"*Footer: {text}*"

    def format_narrative_text(text):
        # Narrative text is plain text, possibly multiple paragraphs.
        return text

    def format_uncategorized_text(text):
        # Similar to narrative text, just pass it through.
        return text

    # Map element types to their formatting functions.
    # If an element type isn't found here, it will fall back to plain text.
    formatters = {
        "Title": format_title,
        "Header": format_header,
        "ListItem": format_list_item,
        "CodeSnippet": format_code,
        "Table": format_table,
        "FigureCaption": format_figure_caption,
        "Formula": format_formula,
        "Address": format_address,
        "EmailAddress": format_email_address,
        "Image": format_image,
        "PageBreak": format_page_break,
        "Footer": format_footer,
        "NarrativeText": format_narrative_text,
        "UncategorizedText": format_uncategorized_text,
    }

    markdown_lines = []
    for element in elements:
        element_type = getattr(element, "type", None)
        text = getattr(element, "text", "").strip()

        # Skip empty elements
        if not text:
            continue

        # Select the appropriate formatting function based on element type.
        format_func = formatters.get(element_type, lambda x: x)

        # Apply formatting and add to the list.
        formatted_text = format_func(text)
        markdown_lines.append(formatted_text)

        # Add a blank line after each element to improve readability.
        markdown_lines.append("")

    # Join all lines, stripping trailing whitespace.
    # Also remove excessive empty lines at the end.
    markdown_output = "\n".join(line for line in markdown_lines if line is not None).strip() + "\n"

    return markdown_output

@app.post("/process-file")
async def process_file(file: UploadFile = File(...)):
    # Save the uploaded file
    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())
    
    # Process the file using `partition`
    elements = partition(filename=temp_file_path)
    #result = elements_to_markdown(elements)
    
    # Clean up the temporary file
    result = "\n\n".join([str(el) for el in elements])
    
    return {"elements": result}