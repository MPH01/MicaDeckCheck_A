pycode = "Mica DeckCheck_v0.01.py"
#-Demo GUI interface for sharing. Feel free to steel or namipulate this however
#   you please. Try not to do to much evil.
#-General intent is to show how to wrap an interface around some programming logic
#   you want to preserve and re-use.
#-The GUI or interface is using python Tkinter. This is the lowest and likely most
#   primative flavor. There are may alternatives and likely some are much easier to
#   use. But this should always be available.
#-To generate the EXE file I'm using pyInstaller. Also freeware of course. But it is
#   easy to use. Reviews seem to indicate it makes smaller files than some think py2exe.
#   The one catch is you do need to install pyWin32 or pyWin64. Also freeware and installes
#   easy enough. Just FYI it is needed.
#-General functionality I'm building into this demo is the ability to read Nastran input
#   decks, get some info from it, then show it to you. Basically some of the same things
#   I would search for with TextPad/Notepad/Notepad++. But can them in this interface.
#-Do keep in mind I have no training in programming. So my method may be in bad form:)
#   I generaly try to keep everyint in on PY file, avoid Class's (because I have no class)
#   and loosely organize in the order of a process. But I do make fairly extensive use of
#   DEFs. These are just functions that are called someplace else in the code. I do have a
#   a kind of standard set I find useful. So you may find I have some in the code but they
#   are not called.


HelpTopGeneralMSG = "General Information\nFrom code: "+pycode+"\n\nDemo GUI interface for sharing. \
Feel free to steel or namipulate this however you please. Try not to do to much evil.\n\nGeneral \
intent is to show how to wrap an interface around some programming logic you want to preserve and \
re-use.\n\nThe GUI or interface is using python Tkinter. This is the lowest and likely most primative \
flavor. There are may alternatives and likely some are much easier to use. But this should always be \
available.\n\nTo generate the EXE file I'm using pyInstaller. Also freeware of course. But it is easy \
to use. Reviews seem to indicate it makes smaller files than some think py2exe. The one catch is you \
do need to install pyWin32 or pyWin64. Also freeware and installes easy enough. Just FYI it is \
needed.\n\nGeneral functionality I'm building into this demo is the ability to read Nastran input \
decks, get some info from it, then show it to you. Basically some of the same things I would search \
for with TextPad/Notepad/Notepad++. But can them in this interface.\n\nDo keep in mind I have no \
training in programming. So my method may be in bad form:) I generaly try to keep everyint in on \
PY file, avoid Class's (because I have no class) and loosely organize in the order of a process. \
But I do make fairly extensive use of DEFs. These are just functions that are called someplace \
else in the code. I do have a kind of standard set I find useful. So you may find I have some \
in the code but they are not called."

PopFileInfoMSG = "Program is using python os.startfile(path_file) to try and open the file for you. This seems to \
use what your machine does when you double-click on a file. So you may get mixed results. Sorry if it doesn't work \
for you.\n\n And if you have a better suggestion let me know:)\n\nIf you know the path or variable+path that \
should work for your machine or machines you intend on using this will subprocess and os.open can be used. It \
just depends on how much work you want to do tracking down the executable path and making it reliably work."

SelectFilesInfoMSG = "Initial process intends for you to select a single file. But you could modify the process to \
select multiple files. So you would get same general information for each BDF selected. Just a thought."

PropertiesHelpInfoMSG = "Properties info"

    #A Tuple of stuff I may search for in text editor or want to know how many I got
    # Many ways to organize this. Tuples are like Lists but you can not modify them. Just recreate. Hence I like Lists better. But itteration is
    #   the same. So it is easy to switch.
    # A better method, because some stuff is only approparite in specific BDF sections, is a Dictionary. Maybe I'll turn this into a Dictionary.
    #   I generally avoid these for storing large amoutns of data though. It is like a fully populated matrix. Where as a List of Lists is
    #   much smaller.
Txt_Srch_Sections = ("CEND","BEGIN BULK")
Txt_Srch_Fundimentals = ("SOL","TITLE","SUBTITLE","Subcase name","SUBCASE","include","Patran","Nastran","SET","CORD2R")
Txt_Srch_Props = ("Properties","PSHELL","PCOMP","PBAR","PBEAM","PSOLID","PBUSH","PSHEAR","PSHLN1","PSHLN2","PSLDN1")
Txt_Srch_Elms = ("Elements","CBAR","CBEAM","CTRIA","CQUAD","CTETRA","CHEXA","CPENTA")
Txt_Srch_LBCs = ("LBCs","SPC","LOAD","PLOAD1","PLOAD4","TEMP","TEMPERATURE")
Txt_Srch_Other = ("GRIDs","GRID")
Txt_Srch_Contact = ("BCPARA","BCTABLE","BCBODY","BSURF","CORD2R","BCONTACT","SLAVE","MASTERS")


from Tkinter import *
import tkFileDialog
import tkMessageBox
import time
import os
import shutil
import tkFont #font = tkFont.Font ( family="Helvetica",size=36, weight="bold",underline=1,slant="italic" )

root = Tk()
root.title('GUI from: '+pycode )
    ### Global variable below to Tkinter. So have to go after that call.
filepick = StringVar()
junkloc = "C:\*.*"
filepick.set(junkloc)
filepath = StringVar()   #Set at multiple locations below. joy
fileext = StringVar()   #Set at multiple locations below. joy
#UpdatePlot = IntVar()
#UpdatePlot.set(0)
#TextOutput1 = StringVar()

frame=Frame(root,width=300,height=600)

def TupleMLmaxWtoT(Tin,PadSpace = 4):  #Not GUI centric
    #Short version, convert column of data to a row then find widest one. Most spaces needed for
    #   column width so you can see everything. Then add this width to first line of list. So this
    #   first line must be treated special. Rest treated a different simpler way.
    #print "Tin: "+str(Tin)
    ListE =[]
    TupleW2=()
    for i in Tin:
        ListE.append( list(i) )
    ListEt = [[row[i] for row in ListE] for i in range( len( ListE[0]) )]
    #print "ListEt: "+str(ListEt)
    for i in ListEt:
        maxW = 0
        for j in i:
            if len(str(j)) > maxW:
                maxW = len(str(j)) +PadSpace
        TupleW2 = TupleW2 +(maxW,)
    #print "TupleW2: "+ str(TupleW2)
    zipped = zip( list(Tin[0]) , list(TupleW2) )
    Tout = (tuple(zipped),)+Tin[1:]
    #print "Tout: "+str(Tout)
    return Tout

def WriteResFiles2(loc,dataL):
    #Assume data is in list of lists. Create comma separated string with no last "," and EOL \n
    #print str(loc)
    FdataL=[]
    for l in dataL:
        lasString=''
        if type(l).__name__ == "list":
            for c in l:
                lasString+=str(c)+','
            lasString=lasString[:-1]+'\n'
        else:
            lasString=l+"\n"
        FdataL.append(lasString)
    write=open(loc,'w')
    write.writelines(FdataL)
    write.close()
    return

def CrossCheckMasterTuple(chk,MasterT,Intials=0,TagNA="?"):  #Not GUI centric
    #DEPENDENT on InitialsNameManip
    Output = chk+TagNA
    Problem = 1
    for a in MasterT:
        if Intials:
            if chk == InitialsNameManip(a):
                Problem = 0
                Output = InitialsNameManip(a,0)
        else:
            if chk == a:
                Problem = 0
                Output = chk
    return (Problem,Output)

def InitialsNameManip(INwName,Initials = 1):  #Not GUI centric
    #From something like JS(Joe Someone) get either JS or Joe Someone
    if not "(" in INwName and not ")" in INwName:
        return INwName
    elif Initials:
        OUTname = INwName[:INwName.find("(")]
    else:
        OUTname = INwName[INwName.find("(")+1:INwName.find(")")]
    return OUTname

def DeconstructFileFromFullPath(FFpath):  #Not GUI centric
    Path=FFpath[:FFpath.rfind('/')+1]
    File=FFpath[FFpath.rfind('/')+1:FFpath.rfind('.')]
    Extension=FFpath[FFpath.rfind('.'):]
    return(Path,File,Extension)

def DeconstructFileFromFullPath2(FFpath):       #GUI centric but does not pop a GUI
    #print "DeconstructFileFromFullPath2 (in): "+str(FFpath)
    FFpath = FFpath.replace("/","\\")
    Path = FFpath[:FFpath.rfind('\\')+1]
    File = FFpath[FFpath.rfind('\\')+1:FFpath.rfind('.')]
    Extension = FFpath[FFpath.rfind('.'):]
    #print "(out): "+str(Path)+" | "+str(File)+" | "+str(Extension)
    filepath.set(Path)
    fileext.set(Extension)

def Fix_askopenfilenames1(FunkyString):     #Not GUI centric
    #At least on windows the returned list of path_file comes back as a string with {} around
    # path_file that don't follow old standards. So they need "" around them. Okay paths with
    # no spaces or funy charactors ($ % # & , . _) get no {}. So this little DEF sorts that out.
    if not type(FunkyString).__name__ == tuple:
        FunkyString = FunkyString.replace(' {','|"')
        FunkyString = FunkyString.replace('}','"?')
        FunkyString = FunkyString.replace('{','"')
        FunkyL1 = FunkyString.split("|")
        #print "FunkyL1: "+str(FunkyL1)
        FunkyL2=[]
        for i in FunkyL1:
            if '"' in i and not "?" in i:
                FunkyL2.append(i)
            elif '"' in i and "?" in i:
                FunkyS1 = i.replace('?','|')
                FunkyL3 = FunkyS1.split('|')
                for j in FunkyL3:
                    if '"' in j:
                        FunkyL2.append(j)
                    else:
                        FunkyL2b = j.split(' ')
                        FunkyL2.extend(FunkyL2b)
            else:
                FunkyL2.extend(i.split(' '))
        OkayTuple = ()
        for i in range( len(FunkyL2)):
            add_me = FunkyL2[i].strip()
            if len(add_me) >= 1:
                OkayTuple = OkayTuple + (add_me,)
        return OkayTuple
    else:
        return FunkyString

                        # # # DEFs to create and manage the different GUI windows # # #
def HelpMenu1():
        #General HELP button at base or top GUI
    helpm = Toplevel()
    hmheight = 300
    helpm.minsize(width=700, height=hmheight )
    helpm.maxsize(width=700, height=hmheight )
    helpm.title('Help')
    Hscrollbar = Scrollbar(helpm)
    Hscrollbar.pack(side=RIGHT, fill=Y)
    ct1 = Text(helpm, yscrollcommand=Hscrollbar.set,wrap=WORD ,background='white')
    ct1.insert(INSERT, HelpTopGeneralMSG )
                #Call it up
    ct1.pack()
    Hscrollbar.config(command=ct1.yview)
                #Top Menu - Help Dialogue
    helpmbar = Menu(helpm)
    helpmbar.add_command(label="Done!", command=helpm.quit)
    helpm.config(menu=helpmbar)
    helpm.mainloop()
    helpm.destroy()



            #Top Menu - Main interface (Need at end so it can call up to other DEFs)
menubar = Menu(root)
menubar.add_command(label="Quit!", command=root.quit)
menubar.add_command(label="Help", command=HelpMenu1)
root.config(menu=menubar)
                ##   Main interface Big Buttons

                    ##  Select Files
BDFin = StringVar()  #Files for CSV. Unprocessed. Format from file select is a Tuple but a String with Global
def SelectBDFs():
    FilesSelected = tkFileDialog.askopenfilenames(title = "Select File(s)", filetypes=[("allfiles","*")] )
    FilesSelected = Fix_askopenfilenames1( FilesSelected )
    #print "--SelectFilesForCSV(in DEF)[after fix]:"
    #for i in FilesSelected:
    #    print i
    BDFin.set( FilesSelected )   

BDFSelect = Button(root,width = 12, text='Select File(s)...',command=SelectBDFs)
BDFSelect.grid(row=0,column=0, sticky = W)

def SelectFilesInfo():
    tkMessageBox.showinfo(title = "Selection for CSV", message = SelectFilesInfoMSG )
PopFilesHelp = Button(root, text='!',fg="red",bg="white",font=tkFont.Font(size=10,weight="bold"), command=SelectFilesInfo )
PopFilesHelp.grid(row=0,column=3, sticky = W)

    
                        ##  Display list of files selected
def DisplayListFiles():
    DisplayFiles = Toplevel()
    DisplayFiles.title('Unprocessed files for CSV consideration')
                ### Display files - BDF + INCLUDE
    DisplayFilesbar = Menu(DisplayFiles)
    DisplayFilesbar.add_command(label="Cancel/Done!", command=DisplayFiles.quit)
    DisplayFiles.config(menu=DisplayFilesbar)
    
    scrollbarDz = Scrollbar(DisplayFiles)
    scrollbarDz.pack( side = RIGHT, fill=Y )

    Zdlist = Listbox(DisplayFiles, width = 128, yscrollcommand = scrollbarDz.set )
    if len(BDFin.get()) <= 1:
        Zdlist.insert( END, "No files selected, dude!" )
    else:
        for z in eval(BDFin.get()):
           Zdlist.insert( END, str(z) )

    Zdlist.pack( side = LEFT, fill = BOTH )
    scrollbarDz.config( command = Zdlist.yview )

    DisplayFiles.mainloop()
    DisplayFiles.destroy()

CSVmkSelected = Button(root,width = 25,relief=RAISED,bd=4, text='Display file(s) with path...',command=DisplayListFiles)
CSVmkSelected.grid(row=1,column=0,columnspan=2, sticky = W)

PropertiesHelpInfoMSG
                        ##  Properties in BDF
wLabelc = Label(root,text="Properties:")
wLabelc.grid(row=3,column=0, sticky = W)
        #Buttons - List Box
PropVar = StringVar()
PropVar.set(Txt_Srch_Props[0])

PropListBox = OptionMenu( root,PropVar,*Txt_Srch_Props)#, command=PayeeEntryBoxC() )
PropListBox.grid(row=3,column=2, sticky = W)
def PropertiesHelpInfo():
    tkMessageBox.showinfo(title = "CSV Payee Info", message = PropertiesHelpInfoMSG)
PropertiesHelp = Button(root, text='?',fg="darkblue",bg="white",font=tkFont.Font(size=10,weight="bold"),command=PropertiesHelpInfo )
PropertiesHelp.grid(row=3,column=3, sticky = W)

    
                        ##  Zip All Files
#rButtonZIP = Button(root,width=40, text='Package (ZIP) files...',command=PackageZipFile1) #
#rButtonZIP.grid(row=2,column=0)

root.mainloop()
root.destroy()


print "Done!"
