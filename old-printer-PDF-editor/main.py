import PyPDF2 as pdf
from CustomFrame import WarningWindow
import tkinter as tk
import os 
from tkinter import filedialog

class MainApp(tk.Frame):
    def __init__(self, root) -> None:
        '''
        Default Constructor for MainApp.

        Parameter(s):
            root - the root of this Frame
        '''
        tk.Frame.__init__(self, root)
        self.root = root
        self._currPdfLoc = None
        self._draw()   

    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        filename = filedialog.askopenfile(filetypes=[('PDF File', '*.pdf')])
        if filename:
            self.updatePdf(filename.name)

    def updatePdf(self, newLoc:str):
        self._currPdfLoc = newLoc
        self._currPdfText.configure(text=f'Current pdf: {newLoc}')

    def processPDF(self):
        #Check if there is a selected pdf
        if self._currPdfLoc == None:
            WarningWindow(root =self.root, msg="NO pdf is selected")
            return

        with open(self._currPdfLoc , 'rb') as readfile:
            currPDF = pdf.PdfFileReader(readfile)
            num_Pages = currPDF.getNumPages()

            #if the pdf is not even # then warning window and does nothing
            #the scan should be all front page + all back page
            if num_Pages % 2 != 0:
                WarningWindow(root =self.root, msg="This pdf is in wrong format.\nIt does not have even # of pages.")
                return

            #create the new pdf
            partSize = int(num_Pages/2)
            output_pdf = pdf.PdfFileWriter()
            for i in range(partSize):
                output_pdf.addPage(currPDF.getPage(i))
                output_pdf.addPage(currPDF.getPage(num_Pages -1 -i))

            #save to a file
            i = 0
            preFileName = self._currPdfLoc.split('.pdf')[0]
            finished_pdf_path = preFileName + '_completed.pdf'
            while os.path.exists(finished_pdf_path):
                i = i + 1
                finished_pdf_path = preFileName + f'_completed({i}).pdf'

            with open(finished_pdf_path, "wb") as writefile:
                output_pdf.write(writefile)


    def _draw(self):
        root = self.root

        self._currPdfText = tk.Label(master=root, text=f'Current pdf: {self._currPdfLoc}')
        self._currPdfText.pack(fill=tk.X, side=tk.TOP)

        buttonZoon = tk.Frame(master=root)
        buttonZoon.pack(fill=tk.BOTH, side=tk.TOP)

        open_button = tk.Button(master=buttonZoon, text="Open a PDF", width=20)
        open_button.configure(command=self.open_profile)
        open_button.pack(fill=tk.BOTH, padx=5, pady=5)

        open_button = tk.Button(master=buttonZoon, text="Process File", width=20)
        open_button.configure(command=self.processPDF)
        open_button.pack(fill=tk.BOTH, padx=5, pady=5)
        pass

if __name__ == '__main__':
    main = tk.Tk()
    main.title("Fix My PDF")
    main.geometry("300x100")

    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()

'''
    #initial prototype
    #part_one_pdf_path = input('Enter the 1st half pdf: ')
    #part_two_pdf_path = input('Enter the pdf to be reversed: ')
    user = 'Dad'
    part_one_pdf_path = f'F://Scan//$$$//2020//{user}2020HighComFront.pdf'
    part_two_pdf_path = f'F://Scan//$$$//2020//{user}2020HighComBack.pdf'


    #create the part 2 pdf in reverse order save into reversed_pdf_path
    finished_pdf_path = part_one_pdf_path.split('.pdf')[0] + '_completed.pdf'
    reversed_pdf_path = part_two_pdf_path.split('.pdf')[0] + '_reversed.pdf'
    output_pdf = pdf.PdfFileWriter()
    with open(part_two_pdf_path, 'rb') as readfile:
        input_pdf = pdf.PdfFileReader(readfile)
        total_pages = input_pdf.getNumPages()
        for page in range(total_pages - 1, -1, -1):
            output_pdf.addPage(input_pdf.getPage(page))
        with open(reversed_pdf_path, "wb") as writefile:
            output_pdf.write(writefile)
    
    #Merge part 1 with the reversed pdf
    with open(part_one_pdf_path , 'rb') as part_One_file:
        with open(reversed_pdf_path , 'rb') as part_Two_file:
            part_One_pdf = pdf.PdfFileReader(part_One_file)
            part_Two_pdf = pdf.PdfFileReader(part_Two_file)

            part_1_Num_Pages = part_One_pdf.getNumPages()
            part_2_Num_Pages = part_Two_pdf.getNumPages()
            maxPage = part_1_Num_Pages
            if part_2_Num_Pages > part_1_Num_Pages:
                maxPage = part_2_Num_Pages

            output_pdf = pdf.PdfFileWriter()

            for i in range(maxPage):
                if i < part_1_Num_Pages:
                    output_pdf.addPage(part_One_pdf.getPage(i))
                if i < part_2_Num_Pages:
                    output_pdf.addPage(part_Two_pdf.getPage(i))
            with open(finished_pdf_path, "wb") as writefile:
                output_pdf.write(writefile)
'''
