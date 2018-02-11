from pdf2txt import Pdf2txt
import re
from datetime import datetime
from BankRecord import BankRecord

class BelfiusParser:
    def parseRecords(self, fileNames):
        currentRecords = []
        if fileNames:
           for fnames in fileNames:
               pdf2txt = Pdf2txt([fnames])
               currentComment = ""
               curRec = None
               accountNumber = "NotFilledIn"
               for line in pdf2txt.outfp:
                   #print(line.strip("\n"))
                   REGEX_ACC = r"-+\s+([A-Z0-9]{4}\s+[A-Z0-9]{4}\s+[A-Z0-9]{4}\s+[A-Z0-9]{4})\s+-+"
                   #0001  04-12-2017  (VAL. 03-12-2017)                             -   44,70
                   REGEX_REC = r"(\d{4})\s+(\d{2}-\d{2}-\d{4})\s+\(.*(\d{2}-\d{2}-\d{4})\)\s+([+-])\s*(.*)"
                   m = re.match(REGEX_ACC, line)
                   #print(m)
                   if m:
                       accountNumber = m.group(1)
                   m = re.match(REGEX_REC, line)
                   #print("2")
                   #print(m)
                   if m:
                       if curRec:
                           curRec.comment = currentComment
                           currentRecords += [curRec]
                           curRec = None
                       currentComment = ""
                       date = datetime.strptime(m.group(2), "%d-%m-%Y")
                       curRec = BankRecord("Belfius", m.group(1), accountNumber, date, m.group(4)+m.group(5), "toBeAdded")
                   else:
                       comM = re.match("(.*)", line)
                       if comM:
                           if curRec:
                               lastParseComment = comM.group(1).strip()
                               if len(lastParseComment) == 0 and curRec:
                                   curRec.comment = currentComment
                                   currentRecords += [curRec]
                                   curRec = None
                               else:
                                   currentComment += lastParseComment
                                   currentComment += "\n"
        return currentRecords

    def getFileTypeToOpen(self):
        return "Belfius PDF files (*.pdf *.pdf *.PDF *.PDF)]"
