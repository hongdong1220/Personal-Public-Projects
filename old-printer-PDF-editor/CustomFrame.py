##Created by: Hong Dong 
##Email: hsdong1@uci.edu

'''
CutomFram.py contains different custom tkinter widget classes.
'''
from  tkinter import *
import tkinter as tk

class WarningWindow(tk.Frame):
    '''
    A Custom tkinter widget. A pop up window with a highlighted message and a button to close
    '''
    def __init__(self, root, msg:str, charColor:str = 'red', texthighlight:str = 'black', bg:str = 'gray'):
        '''
        The default constructor for WarningWindow.

        Parameter(s):
        root - the root frame for widget 
        msg:str - the warning message
        charColor:str - font color
        texthighlight:str - the color of the texts' hightlight
        bg:str - the background color of the Widget
        '''
        self.charCL = charColor
        self.txtHL = texthighlight

        self.bg = bg
        self.root = root
        self.warning = msg

        #self.top is the popup window
        self.top= tk.Toplevel(root)
        tk.Frame.__init__(self, root)
        self.top.title("ERROR")
        self.top.geometry("350x120")
        self.top.update()
        self._draw()
        self.top.minsize(self.top.winfo_width(), self.top.winfo_height())
        
    def _draw(self):
        '''
        Draw a pop up window with a highlighted message and a button to close the window to screen
        '''
        center = tk.Frame(master=self.top,bg= self.bg)
        center.pack(fill=tk.BOTH,expand=True)
        
        #UPPER area------------------------------
        msgArea = tk.Frame(master=center)
        msgArea.pack(fill=tk.BOTH,expand=False, side=tk.TOP)

        warningLabel = tk.Label(master= msgArea, text= self.warning,font=25, fg=self.charCL, bg=self.txtHL)
        warningLabel.pack()
        #Bot Area (under account info)----------------------------
        #this area contain input area, Done button
        bottomArea = tk.Frame(master=center)
        bottomArea.pack(fill=tk.BOTH,expand=True)
            #Done button
        done_button = tk.Button(master=bottomArea, text="OK", width=20)
        done_button.pack(fill=tk.BOTH)
        done_button.configure(command=self.done)

    def done(self):
        '''
        Simply close the pop up window
        '''
        self.top.destroy()

class ScrollTextBox(tk.Frame):
    '''
    A Custom Genearl TextBox with a scroll bar widget 
    '''
    def __init__(self, root, totalwidth:int = 0, height:int = 0, bg = '', fg = ''):
        '''
        The default constructor for ScrollTextBox.

        Parameter(s):
        root - the root frame for widget
        totalwidth:int - the with of this widget
        height:int - the height of this widget
        bg:str - Background color of this widget
        fg:str - font color of this widget
        '''
        self.root = root
        self.width = totalwidth
        self.height = height
        self.bg = bg
        self.fg = fg
        tk.Frame.__init__(self, root)
        self._draw()
    
    def get_text(self) ->str:
        """
        Get the text that is currently in the text widget.
        """
        return self.entry_editor.get('1.0', 'end').rstrip()
    
    def set_text(self, text:str):
        """
        Sets the text to be displayed in the text box.
        This method is useful for clearing the widget, just pass an empty string.

        Parameter(s):
            text :str - the text to fill this text box with
        """
        self.entry_editor.delete('1.0', 'end')
        self.entry_editor.insert('1.0' , text)

    def _draw(self):
        '''
        Draw the text box and scrollbar to root
        '''

        #editor_frame is the area for text entry
        editor_frame = tk.Frame(master= self.root, height=self.height,width=self.width, bg=self.bg)
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        #scroll_frame is the area for scrollbar
        scroll_frame = tk.Frame(master= self.root, width=10, bg=self.bg)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, height=0, width=0, bg=self.bg, fg=self.fg)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

    def change_color(self, fg:str ='', bg:str=''):
        '''
        Update color according to the input

        Parameter(s):
            bg:str - background color of this widget
            fg:str - font color of this widget
        '''
        self.fg = fg
        self.bg = bg

class GeneralWindow(tk.Frame):
    '''
    A custom tkinter widget that create a new window and ask for needed inputs.
    '''
    def __init__(self, root, winTitle:str = '' , topMsg:str = '', input_needed:list = None, call_back = None, minW:str = '350', minH:str = '120'):
        '''
        The default constructor for GeneralWindow.

        Parameter(s):
        root - the root frame for widget 
        winTitle :str - The title of the window 
        topMsg :str - The message to be put on top
        input_needed:list - the list of prompt that this GeneralWindow will ask
        call_back - the fucntion to call back when the done button is presed
        minW :str - the minimum width this GeneralWindow should follow
        minH :str - the minimum height this GeneralWindow should follow
        '''
        self.root = root
        self.title = winTitle
        self._infoMsg = topMsg
        self._inputList = input_needed
        self._call_back = call_back

        #self.top is the popup window
        self.top= tk.Toplevel(root)
        tk.Frame.__init__(self, root)
        self.top.title( self.title)
        self.top.geometry(f"{minW}x{minH}")
        self.top.update()
        self._draw()
        self.top.minsize(self.top.winfo_width(), self.top.winfo_height())
        
    def _draw(self):
        '''
        Draw a new window for the widget. It follows the format: Text info -> list of inputs boxes -> Finish button
        '''
        center = tk.Frame(master=self.top)
        center.pack(fill=tk.BOTH,expand=True)
        
        #account info area------------------------------
        accountArea = tk.Frame(master=center)
        accountArea.pack(fill=tk.BOTH,expand=False,side=tk.TOP)

        accountInfoLabel = tk.Label(master=accountArea, text=self._infoMsg)
        accountInfoLabel.pack(fill=tk.BOTH,expand=True)

        #Bot Area (under account info)----------------------------
        #this area contain input area, Done button
        bottomArea = tk.Frame(master=center)
        bottomArea.pack(fill=tk.BOTH,expand=True)

            #Input  Area
        inputArea = tk.Frame(master=bottomArea)
        inputArea.pack(fill=tk.X,expand=True)

        self.inputBoxes = []
        for word in self._inputList:
            boxArea = tk.Frame(master=inputArea)
            boxArea.pack(fill=tk.BOTH,expand=True)
            label = tk.Label(master=boxArea, text= word)
            label.pack(fill=tk.BOTH,expand=False,side=tk.LEFT)

            inputBox = tk.Text(master=boxArea, height=1)
            inputBox.pack(fill=tk.X,expand=True)
            self.inputBoxes.append(inputBox)

            #Done button
        done_button = tk.Button(master=bottomArea, text="Done", width=20)
        done_button.pack(fill=tk.BOTH)
        done_button.configure(command=self.done)

    def done(self):
        '''
        This is the done fucntion which handles call_back fucntion.
        Afterward it will close the window it sits in
        '''
        if self._call_back is not None:
            ans = []
            for box in self.inputBoxes:
                inputSTR = box.get('1.0', 'end').rstrip()
                ans.append(inputSTR)
            self._call_back(ans)
        self.top.destroy()

if __name__ == "__main__":
    root=Tk()
    GeneralWindow(root,'GENERAL TEST' , 'THIS IS INFO SESSION', ['Ans: ', 'ans2: '], print)
    root.geometry("720x480")
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()


