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
pdf_files = ['bar_chart_report_2024-09-23_02-16-39.pdf',
              'stacked_line_chart_report_2024-09-23_02-14-51.pdf',
              'logarithmic_line_chart_report_2024-09-23_02-15-49.pdf'
              ] 
 # Add your PDF files here
merge_pdfs(pdf_files, 'merged_output.pdf')
