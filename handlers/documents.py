import os
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger 
import fitz
import ntpath


class PDF: 
    __tags = ['format', 'title', 'author','subject','keywords','creator','producer','creationDate','modDate','encryption']

    def __init__(self, pathname):
        assert ntpath.isfile(pathname), "given pathname doest not belong to a file"
        self.pathname = pathname
        self.filename, self.extension = ntpath.basename(pathname).rsplit('.', 1)
        self.directory = ntpath.dirname(pathname)
        self.metadata = {}  # Key=tag, Value=value for the tag
        self.toc = {}  # [heirarchy, "title", page]
        self.fileToMerge = {}
        self.addPagePdf = {}
        self.addPageIndex = {}
        self.watermark = {}
        
    #Function to add a watermark to a PDF Document
    #Parameters:
    #   self - file/path to add the watermark to
    #   ouput_pdf - file/path which is the output file (creates a copy of the file)
    #   watermark_pdf - pdf file which serves as the watermark
    def set_watermark(self, watermark_pdf):
        watermark = PdfFileReader(watermark_pdf)
        pdf = PdfFileReader(self.pathname)
        pdf_writer = PdfFileWriter()

        watermark_page = watermark.getPage(0)
        
        for page in range(pdf.getNumPages()):
            pdf_page = pdf.getPage(page)
            pdf_page.mergePage(watermark_page)
            pdf_writer.addPage(pdf_page)
            print("watermarking page: " + str(page) + " of " + str(pdf.getNumPages()))

        with open(self.pathname, 'wb') as fh:
            pdf_writer.write(fh)

    #Merge two pdf documents (one after the other)
    #Parameters:
    #   input_path1 - file/path of the document that will appear first
    #   input_path2 - file/path of the document that will appear after the first file
    def merge_pdf(self, fileToMerge):
        self.fileToMerge = fileToMerge
        # print(self.fileToMerge)
        file1 = PdfFileReader(self.pathname)
        file2 = PdfFileReader(fileToMerge)
        pdf_merger = PdfFileMerger()

        pdf_merger.append(file1)
        pdf_merger.append(file2)

        with open(self.pathname, 'wb') as fh:
            pdf_merger.write(fh)


    #Adds a page from one pdf to another pdf at a specified index
    #Parameters:
    #   input_path1: file to add the page to
    #   input path2: file to add
    #   pageIndex: where in file1 to add file2
    def addPageAfter(self, input_path2, pageIndex):
        self.addPagePdf = input_path2
        self.addPageIndex = pageIndex
        # print(self.addPagePdf + ": " + self.addPageIndex)
        file1 = PdfFileReader(self.pathname)
        file2 = PdfFileReader(input_path2)
        output = PdfFileWriter()

        for page in range(pageIndex):
            print("page " + str(page) + " of " + str(file1.getNumPages()))
            output.addPage(file1.getPage(page))

        output.addPage(file2.getPage(0))    

        for page in range(pageIndex, file1.getNumPages()):
            print("page " + str(page) + " of " + str(file1.getNumPages()))
            output.addPage(file1.getPage(page))

        with open(self.pathname, 'wb') as fh:
            output.write(fh)
    
    #update the files' table of contents
    #parameters:
    #   file: file to edit table of contents
    #   toc: table of contents to add.  [hierarchy-level, title, page-number]
    #Example of ToC: [[1,"title",3], [2, "desc", 5]]
    def set_toc(self,toc):
        # = [hierarchy-level, title, page-number]
        self.toc = toc
        
    
    def get_data(self):
        doc = fitz.open(self.pathname)
        #get metadata 
        metadata = doc.metadata
        #get ToC
        toc = doc.getToC()
        #print both
        print(toc)
        print(metadata)
        
    #method to get a specific tag from a file    
    def get_tag(self, tag):
        assert tag in self.__tags, "tag is not supported"
        ttr = self.metadata[tag]
        print(self.metadata[tag])
        return ttr if ttr else None

    #set a specific tag to a data value
    def set_tag(self, tag, data):
        assert tag in self.__tags, "tag is not supported"
        self.metadata[tag] = data
        print(self.metadata)
    
    #edit metadata from a file by passing it a key-value paired object as parameter
    #parameters:
        #file : file to edit
        #data: metadata to change
        #Example: {"author":"John Smith", "title", "Sample Title"}
    def save(self):
        signature = "[MyTag]"
        out_name = signature + self.filename + '.' + self.extension
        #output = os.path.join(self.directory, out_name)
        output = PdfFileWriter()

        doc = fitz.open(self.pathname)
        if self.metadata:
            doc.setMetadata(self.metadata)
        
        if self.toc:
            doc.setToC(self.toc)

        doc.save(doc.name, incremental=True)

        # #if self.fileToMerge:
        #     file1 = PdfFileReader(self)
        #     file2 = PdfFileReader(self.fileToMerge)
        #     pdf_merger = PdfFileMerger()

        #     pdf_merger.append(file1)
        #     pdf_merger.append(file2)
        #     pdf_merger.write("document-output.pdf")

        #if self.addPageAfter:
        #     file1 = PdfFileReader(self)
        #     file2 = PdfFileReader(self.addPagePdf)

        #     for page in range(self.addPageIndex):
        #         print("page " + str(page) + " of " + str(file1.getNumPages()))
        #         output.addPage(file1.getPage(page))

        #     output.addPage(file2.getPage(0))    

        #     for page in range(self.addPageIndex, file1.getNumPages()):
        #         print("page " + str(page) + " of " + str(file1.getNumPages()))
        #         output.addPage(file1.getPage(page))

        # with open("output_pdf", 'wb') as fh:
        #     output.write(fh)

        #if self.watermark:
        #     watermark = PdfFileReader(self.watermark)
        #     pdf = PdfFileReader(self)

        #     watermark_page = watermark.getPage(0)
        
        #     for page in range(pdf.getNumPages()):
        #         pdf_page = pdf.getPage(page)
        #         pdf_page.mergePage(watermark_page)
        #         output.addPage(pdf_page)
        #         print("watermarking page: " + str(page) + " of " + str(pdf.getNumPages()))

        # with open(output_pdf, 'wb') as fh:
        #     pdf_writer.write(fh)
        
    