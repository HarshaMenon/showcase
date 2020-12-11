from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from pygame import mixer
import pygame as pg
from jiwer import wer 
import scipy.io.wavfile
import numpy



import os
sys.path.append(os.path.abspath('.')+"/OpenVokaturi-3-3/api")
import Vokaturi

import librosa
import time

class Welcome():
    def __init__(self,master):
        self.master=master
        self.master.title('Voice Recorder and Recognisation App')
        self.master.iconbitmap('mic.ico')
        #root.iconbitmap('mic.ico')
        #emo = tk.StringVar(root)
        self.master.style = ttk.Style()
        self.master.style.theme_use('classic')
        self.master.geometry('680x500')
        
        #self.button1=Button(self.master, text='record voice', width=10, fg='blue', command=self.gotoSecondWindow).grid(row=6, column=4)
        #self.button2=Button(self.master, text='check voice profile',width=10, fg='blue', command=self.gotoThirdWindow).grid(row=8, column=4)
        #self.button2=Button(self.master, text='quit',width=10, fg='blue', command=self.finish).grid(row=10, column=4)
        
        self.button1=Button(self.master, text='record voice', width=15, fg='blue', command=self.gotoSecondWindow).place(x=100, y=360)
        self.button2=Button(self.master, text='check voice profile',width=15, fg='blue', command=self.gotoThirdWindow).place(x=250, y=360)
        self.button2=Button(self.master, text='quit',width=15, fg='blue', command=self.finish).place(x=400, y=360)

        
    def gotoSecondWindow(self):
        root2 = Toplevel(self.master)
        myGUI=SecondWindow(root2)
        
    def gotoThirdWindow(self):
       root3 = Toplevel(self.master)
       myGUI2=ThirdWindow(root3)
        
    def finish(self):
        self.master.destroy()
        
    
class ThirdWindow():
    def __init__(self,master):
        self.master=master
        self.master.title('Voice Profiler')
        #root.iconbitmap('mic.ico')
        #emo = tk.StringVar(root)
        self.master.style = ttk.Style()
        self.master.style.theme_use('classic')
        self.master.geometry('680x1000')
        self.photo = PhotoImage(file='microphone.png').subsample(35, 35)
        self.WPM = DoubleVar()
        self.name = StringVar()
        #self.mixer
        
        t = 'This proverb is an important line which helps us in correcting '
        t =  t  + 'our life course. When our shirt or trousers get torn, we should mend then and '
        t =  t  + 'there. That way the shirt or trousers can be used for some more time to come.'
        t =  t  + 'But if we do not attend to a minor wear and tear, it will ultimately render '
        t =  t  + 'the garment completely unfit for use. In the same way, a minor repair in the '
        t =  t  + 'engine at the first detection of a defect, or the plugging of a crack or hole '
        t =  t  + 'in a boat, the moment it is noticed, will save many a future trouble.That is '
        t =  t  + 'why it is said, and rightly so, that a stitch in time saves nine.'      
       
        self.sample_text =  t
        self.label6 = Label(self.master, text='Know your Voice Profile :')
        self.label6.grid(row=18, column=0)
        
        self.label11 =  Label(self.master, text=' Read Following Text :',anchor=W, justify=LEFT, font = ( 'bold'))
        self.label11.grid(row=19, column=0)
        #self.entry7 =  Entry(self.master, width=40)
        #self.entry7.grid(row=19, column=1, columnspan=4)
        #self.entry7.focus()
        #self.entry7.delete(0, END)
        #self.entry7.insert(0, self.sample_text)  

        self.lbl = Label(self.master, text= t, wraplength = 500, anchor=W, justify=LEFT)
        self.lbl.grid(row=20, column=0, columnspan=5)
        
        self.MyButton4 = Button(self.master, image=self.photo, command=self.buttonClickRecogniseVoice)#, activebackground='#c1bfbf', overrelief='groove', relief='sunken')
        self.MyButton4.grid(row=29, column=1)

        self.MyButton5 = Button(self.master, text='Check', width=10, fg='blue', command=self.displayProfile)#, activebackground='#c1bfbf', overrelief='groove', relief='sunken')
        self.MyButton5.grid(row=29, column=2)
        
        self.lblError =  Label(self.master, text='',anchor=W, fg='red', justify=LEFT, font = ( 'bold'))
        self.lblError.grid(row=32, column=0)
    
        self.lblCapturedTexthdr =  Label(self.master, text=' You Said The Following Text :',anchor=W, justify=LEFT, font = ( 'bold'))
        self.lblCapturedTexthdr.grid(row=33, column=0)
    
        self.lblCapturedText = Label(self.master, text= '', wraplength = 500, anchor=W, justify=LEFT)
        self.lblCapturedText.grid(row=34, column=0, columnspan=5)
        
        self.text = Text(self.master)
        
        self.text.grid(row=36, column=0, columnspan=5)
       
        #root.mainloop()
        '''
        self.lblSub =  Label(self.master, text='',wraplength = 1000,anchor=W, fg='blue', justify=LEFT, font = ( 'bold'))
        self.lblSub.grid(row=38, column=0)
        
        self.lblDel=  Label(self.master, text='',wraplength = 1000,anchor=W, fg='red', justify=LEFT, font = ( 'bold'))
        self.lblDel.grid(row=40, column=0)
        
        self.lblIns=  Label(self.master, text='',wraplength = 1000,anchor=W, fg='green', justify=LEFT, font = ( 'bold'))
        self.lblIns.grid(row=42, column=0)
        '''
        self.label7 =  Label(self.master, text='Name :')
        self.label7.grid(row=42, column=0)
        self.NameEntry =  Entry(self.master, width=40)
        self.NameEntry.grid(row=42, column=1, columnspan=4)
        
        self.label8 =  Label(self.master, text='Word Count Per Min:')
        self.label8.grid(row=43, column=0)
        self.WPMEntry =  Entry(self.master, width=40)
        self.WPMEntry.grid(row=43, column=1, columnspan=4)
        
        
        self.label9 =  Label(self.master, text='Accuracy :')
        self.label9.grid(row=45, column=0)
        self.AccuracyEntry =  Entry(self.master, width=40)
        self.AccuracyEntry.grid(row=45, column=1, columnspan=4)

        self.label10 =  Label(self.master, text='Emotion :')
        self.label10.grid(row=47, column=0)
        self.EmoEntry =  Entry(self.master, width=40)
        self.EmoEntry.grid(row=47, column=1, columnspan=4)
        
        self.MyButton4 =  Button(self.master, text='quit', width=10,  fg='blue', command=self.myquit)
        self.MyButton4.grid(row=49, column=2)  
        
    def editDistance(self,r, h):
        '''
        This function is to calculate the edit distance of reference sentence and the hypothesis sentence.
        Main algorithm used is dynamic programming.
        Attributes: 
            r -> the list of words produced by splitting reference sentence.
            h -> the list of words produced by splitting hypothesis sentence.
        '''
        d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8).reshape((len(r)+1, len(h)+1))
        for i in range(len(r)+1):
            for j in range(len(h)+1):
                if i == 0: 
                    d[0][j] = j
                elif j == 0: 
                    d[i][0] = i
        for i in range(1, len(r)+1):
            for j in range(1, len(h)+1):
                if r[i-1] == h[j-1]:
                    d[i][j] = d[i-1][j-1]
                else:
                    substitute = d[i-1][j-1] + 1
                    insert = d[i][j-1] + 1
                    delete = d[i-1][j] + 1
                    d[i][j] = min(substitute, insert, delete)
        return d

    def getStepList(self,r, h, d):
        '''
        This function is to get the list of steps in the process of dynamic programming.
        Attributes: 
            r -> the list of words produced by splitting reference sentence.
            h -> the list of words produced by splitting hypothesis sentence.
            d -> the matrix built when calulating the editting distance of h and r.
        '''
        x = len(r)
        y = len(h)
        list = []
        while True:
            if x == 0 and y == 0: 
                break
            elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1]: 
                list.append("e")
                x = x - 1
                y = y - 1
            elif y >= 1 and d[x][y] == d[x][y-1]+1:
                list.append("i")
                x = x
                y = y - 1
            elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1]+1:
                list.append("s")
                x = x - 1
                y = y - 1
            else:
                list.append("d")
                x = x - 1
                y = y
        return list[::-1]
   
    def werCustom(self,actual, captured):
        """
        This is a function that calculate the word error rate in ASR.
        You can use it like this: wer("what is it".split(), "what is".split()) 
        """
        
        r =  actual.lower().split()
        h = captured.lower().split()
        
        # build the matrix
        d = self.editDistance(r, h)
    
        # find out the manipulation steps
        list = self.getStepList(r, h, d)
        newList =[]
        #print(list)
        #print(range(len(list)))
        rindex =0
        hindex =0
        #print(r[0])
        #print(h[0])
        for i in range(len(list)):
            #print(i,rindex,hindex)
            if list[i] == "e":
                newList.append( r[rindex])
                rindex = rindex + 1
                hindex = hindex + 1
            elif list[i] == "d":
                newList.append('#!<db>!#' + r[rindex]+ '#!<de>!#')
                rindex = rindex + 1
            elif list[i] == "s":
                newList.append( '#!<sb>!#'+h[hindex]+ '#!<se>!#')
                hindex = hindex + 1
                rindex = rindex + 1
            elif list[i] == "i":
                newList.append( '#!<ib>!#'+h[hindex]+ '#!<ie>!#')
                hindex = hindex + 1
                
        #print(newList)
        # print the result in aligned way
        result = float(d[len(r)][len(h)]) / len(r) * 100
        #result = str("%.2f" % result) + "%"    
        return result, newList
    
    def buttonClickRecogniseVoice(self):
        mixer.init()
        mixer.music.load('chime1.mp3')
        mixer.music.play()

        r = sr.Recognizer()
        r.pause_threshold = 0.7
        r.energy_threshold = 400
        with sr.Microphone() as source:
            try:                
                
            #Harsha code
   
                #audio = r.listen(source)
                #self.message = str(r.recognize_google(audio))
                self.message = "this proverb is an im portant line which helps in our life scores."
                mixer.music.load('chime2.mp3')
                mixer.music.play()
                self.lblCapturedText.focus()
                self.lblCapturedText['text'] =  self.message
                
           
                self.wordsList = self.message.split()
                #with open("microphone-results.wav", "wb") as self.f:
                 #   self.f.write(audio.get_wav_data())
            
            
            except sr.UnknownValueError:
                self.lblError.focus()
                self.lblError['text'] =  'Google Speech Recognition could not Understand audio'
                
                #self.print('Google Speech Recognition could not Understand audio')
            except sr.RequestError as e:
                self.lblError['text'] =  'Could not request result from Google Speech Recogniser Service'
                #self.print('Could not request result from Google Speech Recogniser Service')
            else:
                pass

            # Proyojit code here            
  

    def getStartEndIndexesforText(self,target, mark = None):
        if mark == None:
            mark= INSERT
        startIndex = self.text.search(" "+target+" ", mark) # search from insert cursor
        if mark == None:
            endIndex = startIndex + ('+%dc' % (len(target)-1)) # index beyond string found
        return  startIndex+ ('+%dc' % 1), endIndex 
    
    def displayProfile(self):  
    
            self.NameEntry.focus()
            self.NameEntry.delete(0, END)
            #self.NameEntry.insert(0, "Hi Mitali")
           
            
            self.WPMEntry.focus()
            self.WPMEntry.delete(0, END)
         
            self.Audio_Length_Secs = 150 #librosa.get_duration(filename='microphone-results.wav')
            self.Audio_Length_Mins = self.Audio_Length_Secs/60

            self.WPM.set(len(self.wordsList)/self.Audio_Length_Mins)
            self.WPMEntry.insert(0, "You are able to speak %.2f words per min" % self.WPM.get())
           
            self.AccuracyEntry.focus()
            self.AccuracyEntry.delete(0, END)
            
            #WER = wer(self.sample_text , self.message, standardize=True)
            WER, displayList = self.werCustom(self.sample_text , self.message)
            
            formattedText = " ".join(displayList)
            displayText =  formattedText.replace('#!<sb>!#', '').replace('#!<se>!#', '').replace('#!<db>!#', '').replace('#!<de>!#', '').replace('#!<ib>!#', '').replace('#!<ie>!#', '').replace('#!<sbe>!#', '')
            self.text.insert(INSERT, displayText)
            #self.text.insert(INSERT, formattedText)
            
            sbindexes =[m.start() for m in re.finditer('#!<sb>!#', formattedText)]
            seindexes =[m.start() for m in re.finditer('#!<se>!#', formattedText)]
            dbindexes =[m.start() for m in re.finditer('#!<db>!#', formattedText)]
            deindexes =[m.start() for m in re.finditer('#!<de>!#', formattedText)]
            ibindexes =[m.start() for m in re.finditer('#!<ib>!#', formattedText)]
            ieindexes =[m.start() for m in re.finditer('#!<ie>!#', formattedText)]
                            
            sub = ""
            Del = ""
            Ins = ""
            
            for i in range(len(sbindexes)): 
                sbText = re.findall(r'#!<sb>!#', formattedText[0:sbindexes[i]])
                dbText = re.findall(r'#!<db>!#', formattedText[0:sbindexes[i]])
                ibText = re.findall(r'#!<ib>!#', formattedText[0:sbindexes[i]])
                sbCount = len(sbText)+len(dbText)+len(ibText)
                
                b =  sbindexes[i]-(sbCount * 16) 
                e =  seindexes[i]-((sbCount * 16)+8)
                t = displayText[seindexes[i]-((sbCount * 16)+8): ]
      
                tagWord = displayText[sbindexes[i]-(sbCount * 16)  : seindexes[i]-((sbCount * 16)+8)]
                
                endIndex = self.text.search(t, INSERT)
                startIndex = endIndex + ('-%dc' % len(tagWord)) 
                
                sub = sub + "," + tagWord +"_" +str(e)+"-"+ startIndex + ":" + endIndex
                
                self.text.tag_add("substitutes", startIndex, endIndex) # tag and select found string
                self.text.focus() # select text widget itself
            #self.lblSub['text'] = sub
              
            for i in range(len(dbindexes)): 
                sbText = re.findall(r'#!<sb>!#', formattedText[0:dbindexes[i]])
                dbText = re.findall(r'#!<db>!#', formattedText[0:dbindexes[i]])
                ibText = re.findall(r'#!<ib>!#', formattedText[0:dbindexes[i]])
                sbCount = len(sbText)+len(dbText)+len(ibText) 
                
                b =  dbindexes[i]-(sbCount * 16) 
                e =  deindexes[i]-((sbCount * 16)+8)
                t = displayText[deindexes[i]-((sbCount * 16)+8): ]
                
               
                tagWord = displayText[dbindexes[i]-(sbCount * 16)  : deindexes[i]-((sbCount * 16)+8)]
                endIndex = self.text.search(t, INSERT)
                startIndex = endIndex + ('-%dc' % len(tagWord)) 
                
                Del = Del + "," + startIndex + ":" + endIndex
                
                self.text.tag_add("deletions", startIndex , endIndex )
                 
            for i in range(len(ibindexes)):
                sbText = re.findall(r'#!<sb>!#', formattedText[0:ibindexes[i]])
                dbText = re.findall(r'#!<db>!#', formattedText[0:ibindexes[i]])
                ibText = re.findall(r'#!<ib>!#', formattedText[0:ibindexes[i]])
                sbCount = len(sbText)+len(dbText)+len(ibText)
                
                b =  ibindexes[i]-(sbCount * 16) 
                e =  ieindexes[i]-((sbCount * 16)+8)
                t = displayText[ieindexes[i]-((sbCount * 16)+8): ]
                
                tagWord = displayText[ibindexes[i]-(sbCount * 16)  : ieindexes[i]-((sbCount * 16)+8)]
                endIndex = self.text.search(t, INSERT)
                startIndex = endIndex + ('-%dc' % len(tagWord)) 
                
                Ins = Ins + "," + startIndex + ":" + endIndex
                
                self.text.tag_add("insertions", startIndex , endIndex )
                
            #self.lblSub['text'] = sub
            #self.lblIns['text'] = Ins 
            #self.lblDel['text'] = Del
            
            self.text.tag_config("substitutes", background="yellow", foreground="blue")
           
            self.text.tag_config("deletions", background="red", foreground="green")
            self.text.tag_config("insertions", background="green", foreground="yellow")
           
            
            
            Acc = (1 - WER)*100
            self.AccuracyEntry.insert(0, "%f percent" % Acc)
            
            
            
            Vokaturi.load(os.path.abspath('.')+"/OpenVokaturi-3-3/lib/OpenVokaturi-3-3-mac64.dylib")


            (sample_rate, samples) = scipy.io.wavfile.read('microphone-results.wav')
            buffer_length = len(samples)
            c_buffer = Vokaturi.SampleArrayC(buffer_length)
            if samples.ndim == 1:
                c_buffer[:] = samples[:] / 32768.0  # mono
            else:
                c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0  # stereo
            
            #print("Creating VokaturiVoice...")
            voice = Vokaturi.Voice(sample_rate, buffer_length)
            
            #print("Filling VokaturiVoice with samples...")
            voice.fill(buffer_length, c_buffer)
            
            #print("Extracting emotions from VokaturiVoice...")
            quality = Vokaturi.Quality()
            emotionProbabilities = Vokaturi.EmotionProbabilities()
            voice.extract(quality, emotionProbabilities)
            
            if quality.valid:
                #print("Neutral: %.3f" % emotionProbabilities.neutrality)
                #print("Happy: %.3f" % emotionProbabilities.happiness)
                #print("Sad: %.3f" % emotionProbabilities.sadness)
                #print("Angry: %.3f" % emotionProbabilities.anger)
                #print("Fear: %.3f" % emotionProbabilities.fear)
                dictemotionProbabilities =  dict()
                dictemotionProbabilities['Neutral'] = emotionProbabilities.neutrality
                dictemotionProbabilities['Happy'] = emotionProbabilities.happiness
                dictemotionProbabilities['Sad'] = emotionProbabilities.sadness
                dictemotionProbabilities['Angry'] = emotionProbabilities.anger
                dictemotionProbabilities['Fear'] = emotionProbabilities.fear
                
                self.EmoEntry.focus()
                self.EmoEntry.delete(0, END)
                emo = max(dictemotionProbabilities, key=dictemotionProbabilities.get) 
                self.EmoEntry.insert(0, emo)     
            else:
                self.EmoEntry.focus()
                self.EmoEntry.delete(0, END)
                self.EmoEntry.insert(0, 'could not find emotion from the voice') 
            voice.destroy()
            

           
        
        

   
    def myquit(self):
        self.master.destroy()          
        


class SecondWindow():
    def __init__(self,master):
        self.master=master
        self.master.title('Voice Recorder')
        #root.iconbitmap('mic.ico')
        #emo = tk.StringVar(root)
        self.master.style = ttk.Style()
        self.master.style.theme_use('classic')
        self.master.geometry('680x500') 
        
        self.emo = tk.StringVar()
        self.photo = PhotoImage(file='microphone.png').subsample(35, 35)
        
        self.label1 = ttk.Label(self.master, text='Record and save your voice :')
        self.label1.grid(row=0, column=0)

        self.label4 = ttk.Label(self.master, text='You are speaking :')
        self.label4.grid(row=1, column=0)

        self.label5 = ttk.Label(self.master, text='Enter your name :')
        self.label5.grid(row=2, column=0)
    
        self.entry1 = ttk.Entry(self.master, width=40)
        self.entry1.grid(row=1, column=1, columnspan=4)

        self.entry2 = ttk.Entry(self.master, width=40)
        self.entry2.grid(row=2, column=1, columnspan=4)    
    
        self.MyButton3 = ttk.Button(self.master, image=self.photo, command=self.buttonClick)#, activebackground='#c1bfbf', overrelief='groove', relief='sunken')
        self.MyButton3.grid(row=0, column=2)
    
        self.MyButton1 = ttk.Button(self.master, text='Play', width=10, command=self.callback)
        self.MyButton1.grid(row=0, column=3)

        #self.emo.set('Angry')

        self.popupMenu = tk.OptionMenu(self.master, self.emo, *{'Angry':'Angry', 'Disgust':'Disgust', 'Joy':'Joy', 'Fear':'Fear',
                                       'Suspense':'Suspense', 'Neutral':'Neutral', 'Sad':'Sad'})
        self.popupMenu.grid(row=3, column=2)
        self.label3 = ttk.Label(self.master, text='Emotion')
        self.label3.grid(row=3, column=1)

        self.MyButton2 = ttk.Button(self.master, text='Save Audio', width=10, command=self.save_file)
        self.MyButton2.grid(row=4, column=3)
        
        self.MyButton4 = ttk.Button(self.master, text='quit', width=10, command=self.myquit)
        self.MyButton4.grid(row=5, column=3)


        
        #btn2 = tk.StringVar()

    def save_file(self):
        if len(self.entry2.get()) == 0:
            messagebox.showinfo("Error", "Enter Speaker's Name")
        else:
            list = os.listdir(self.emo.get())
            os.rename('microphone-results.wav', self.emo.get() + "/" + self.entry2.get() + str(len(list)) + ".wav")
            messagebox.showinfo("Saved", "Audio Saved as : " + self.emo.get() + "/" + self.entry2.get() + str(len(list)) + ".wav")


    def callback(self):
        try:
            os.system("start microphone-results.wav")
        except:
            print('No Audio File Found')

    def buttonClick(self):
        mixer.init()
        mixer.music.load('chime1.mp3')
        mixer.music.play()

        r = sr.Recognizer()
        r.pause_threshold = 0.7
        r.energy_threshold = 400
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, timeout=5)
                message = str(r.recognize_google(audio))
                mixer.music.load('chime2.mp3')
                mixer.music.play()
                self.entry1.focus()
                self.entry1.delete(0, END)
                self.entry1.insert(0, message)
                
            except sr.UnknownValueError:
                print('Google Speech Recognition could not Understand audio')
            except sr.RequestError as e:
                print('Could not request result from Google Speech Recogniser Service')
            else:
                pass

        with open("microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())

    def myquit(self):
        self.master.destroy()  


def main():
    root = tk.Tk()
    myGUIWelcome = Welcome(root)
    root.mainloop()

if __name__== '__main__':
    main()    
