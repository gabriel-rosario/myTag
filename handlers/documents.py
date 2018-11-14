

from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger 

class PDF: 
    #Function to add a watermark to a PDF Document
    #Parameters:
    #   input_pdf - file/path to add the watermark to
    #   ouput_pdf - file/path which is the output file (creates a copy of the file)
    #   watermark_pdf - pdf file which serves as the watermark
    def watermark(self, input_pdf, output_pdf, watermark_pdf):
        watermark = PdfFileReader(watermark_pdf)
        watermark_page = watermark.getPage(0)
    
        pdf = PdfFileReader(input_pdf)
        pdf_writer = PdfFileWriter()
    
        for page in range(pdf.getNumPages()):
            pdf_page = pdf.getPage(page)
            pdf_page.mergePage(watermark_page)
            pdf_writer.addPage(pdf_page)
            print("watermarking page: " + str(page) + " of " + str(pdf.getNumPages())) 
        with open(output_pdf, 'wb') as fh:
            pdf_writer.write(fh)

    #Merge two pdf documents (one after the other)
    #Parameters:
    #   input_path1 - file/path of the document that will appear first
    #   input_path2 - file/path of the document that will appear after the first file
    def pdfmerger(self, input_path1, input_path2):
        pdf_merger = PdfFileMerger()
        file1 = PdfFileReader(input_path1)
        file2 = PdfFileReader(input_path2)

        pdf_merger.append(file1)
        pdf_merger.append(file2)

        pdf_merger.write("document-output.pdf")


    def addPageAfter(self, input_path1, input_path2, pageIndex):
        file1 = PdfFileReader(input_path1)
        file2 = PdfFileReader(input_path2)

        output = PdfFileWriter()

        for page in range(pageIndex):
            print("page " + str(page) + " of " + str(file1.getNumPages()))
            output.addPage(file1.getPage(page))

        output.addPage(file2.getPage(0))    

        for page in range(pageIndex, file1.getNumPages()):
            print("page " + str(page) + " of " + str(file1.getNumPages()))
            output.addPage(file1.getPage(page))

        with open("output_pdf", 'wb') as fh:
            output.write(fh)  
    