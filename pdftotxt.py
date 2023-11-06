import sys
import PyPDF2


def extract_text_from_pdf(pdf_path, start_page, end_page, output_path):
    """
    Extracts text from a range of pages in a given PDF and writes to a .txt file.
    :param pdf_path: path to the PDF file.
    :param start_page: start page number (1-indexed).
    :param end_page: end page number (1-indexed).
    :param output_path: path to save the extracted text.
    """
    with open(pdf_path, "rb") as pdf_file:
        # Initialize PDF reader using the updated class name
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        total_pages = len(pdf_reader.pages)

        # Adjust end_page if out of range
        if end_page > total_pages:
            end_page = total_pages

        # Ensure the start page is valid
        if start_page < 1 or start_page > end_page:
            print("Invalid start page!")
            return

        text = ""

        # Extract text from the specified range
        for page_num in range(start_page - 1, end_page):  # 0-indexing in PyPDF2
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        # Write text to output file
        with open(output_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python script_name.py <path_to_pdf> <start_page> <end_page> <output_path.txt>"
        )
        sys.exit(1)

    pdf_path = sys.argv[1]
    start_page = int(sys.argv[2])
    end_page = int(sys.argv[3])
    output_path = sys.argv[4]

    extract_text_from_pdf(pdf_path, start_page, end_page, output_path)
