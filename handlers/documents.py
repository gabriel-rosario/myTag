

from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger 

class PDF: 
    #Function to add a watermark to a PDF Document
    #Parameters:
    #   input_pdf - file/path to add the watermark to
    #   ouput_pdf - file/path which is the output file (creates a copy of the file)
    #   watermark_pdf - pdf file which serves as the watermark
    def watermark(self, input_pdf, output_pdf, watermark_pdf):
        #create writer and reader instances for the input file and watermark file and output
        watermark = PdfFileReader(watermark_pdf)
        pdf = PdfFileReader(input_pdf)
        pdf_writer = PdfFileWriter()

        #get specific page for the watermark
        watermark_page = watermark.getPage(0)
        
        #loop through each page add/mergin the watermark page to the input file
        for page in range(pdf.getNumPages()):
            pdf_page = pdf.getPage(page)
            pdf_page.mergePage(watermark_page)
            pdf_writer.addPage(pdf_page)
            print("watermarking page: " + str(page) + " of " + str(pdf.getNumPages()))

        #create output file     
        with open(output_pdf, 'wb') as fh:
            pdf_writer.write(fh)

    #Merge two pdf documents (one after the other)
    #Parameters:
    #   input_path1 - file/path of the document that will appear first
    #   input_path2 - file/path of the document that will appear after the first file
    def pdfmerger(self, input_path1, input_path2):
        #create reader instances of both input files
        file1 = PdfFileReader(input_path1)
        file2 = PdfFileReader(input_path2)
        pdf_merger = PdfFileMerger()

        #add the first file, followed by the second file, to what will be the output file
        pdf_merger.append(file1)
        pdf_merger.append(file2)

        #create the output file
        pdf_merger.write("document-output.pdf")


    #Adds a page from one pdf to another pdf at a specified index
    #Parameters:
    #   input_path1: file to add the page to
    #   input path2: file to add
    #   pageIndex: where in file1 to add file2
    def addPageAfter(self, input_path1, input_path2, pageIndex):
        #create reader and writer instances of pdf files
        file1 = PdfFileReader(input_path1)
        file2 = PdfFileReader(input_path2)
        output = PdfFileWriter()

        #loop through pages and copy to output file until the desired page (parameter) is reached
        for page in range(pageIndex):
            print("page " + str(page) + " of " + str(file1.getNumPages()))
            output.addPage(file1.getPage(page))

        #add desired page to add (input_path2)
        output.addPage(file2.getPage(0))    

        #add remaining pages to output file
        for page in range(pageIndex, file1.getNumPages()):
            print("page " + str(page) + " of " + str(file1.getNumPages()))
            output.addPage(file1.getPage(page))

        #write the output file
        with open("output_pdf", 'wb') as fh:
            output.write(fh)
    
    #update the files' table of contents
    #parameters:
    #   file: file to edit table of contents
    #   toc: table of contents to add.  [hierarchy-level, title, page-number]
    #Example of ToC: [[1,"title",3], [2, "desc", 5]]
    def createToC(self, file,toc):
        # = [hierarchy-level, title, page-number]
        #open file
        doc = fitz.open(file)
        #for t in toc: print(t)  //prints all the table of contents to see before

        #set new ToC according to the object passed as parameter
        doc.setToC(toc)

        #print ToC again to check 
        for t in toc: print(t)

        #update existing input file
        doc.save(doc.name, incremental=True) 
    
    #method to get metadata and table of contents from a file
    def getData(self, file):
        #open file
        doc = fitz.open(file)
        #get metadata 
        metadata = doc.metadata
        #get ToC
        toc = doc.getToC()
        #print both
        print(toc)
        print(metadata)
    
    #edit metadata from a file by passing it a key-value paired object as parameter
    #parameters:
        #file : file to edit
        #data: metadata to change
        #Example: {"author":"John Smith", "title", "Sample Title"}
    def editPdfMetadata(self, file, data):
        #open file
        doc = fitz.open(file)

        #get metadata
        metadata = doc.metadata

        #print(metadata) print data to check before

        #update metadata with new one presented in parameter
        doc.setMetadata(data)
        #update file
        doc.save(doc.name, incremental=True)
        
        #print to check
        #print(metadata)