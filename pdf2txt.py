import sys
import io
#import StringIO
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

# main
class Pdf2txt():
    def __init__(self, filenameList):
        debug = 0
        pagenos = set()
        maxpages = 0
        password = ""
        caching = True
        codec = 'utf-8'
        laparams = LAParams()
        imagewriter = None
        rotation = 0
        #
        PDFDocument.debug = debug
        PDFParser.debug = debug
        CMapDB.debug = debug
        PDFPageInterpreter.debug = debug
        #
        rsrcmgr = PDFResourceManager(caching=caching)

        self.outfp = io.StringIO()

        device = TextConverter(rsrcmgr, self.outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)
        for fname in filenameList:
            #print(fname)
            fp = open(fname, 'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, pagenos,
                                          maxpages=maxpages, password=password,
                                          caching=caching, check_extractable=True):
                page.rotate = (page.rotate+rotation) % 360
                interpreter.process_page(page)
            fp.close()
        device.close()
        self.outfp.seek(0,0)

    def __del__(self):
        self.outfp.close()

if __name__ == '__main__': sys.exit(main(sys.argv))
