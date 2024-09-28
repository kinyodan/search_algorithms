import PyPDF2


def merge_pdfs(pdf_list, output_path):
    pdf_writer = PyPDF2.PdfWriter()

    for pdf in pdf_list:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    with open(output_path, 'wb') as out_file:
        pdf_writer.write(out_file)


# Example usage
pdf_files = ['stacked_line_chart_report_2024-09-28_23-30-34.pdf',
             'bar_chart_report_2024-09-28_23-29-46.pdf',
             'line_with_markers_report_2024-09-28_23-31-50.pdf'
             ]
# Add your PDF files here
merge_pdfs(pdf_files, 'merged_output.pdf')
