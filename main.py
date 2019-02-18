from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from functools import partial
import os
import datetime
import dropbox


class RootWidget(GridLayout):



#run when done with page two
  def submit_form(self):


    fields=(
      'tech',
      'cust',
      'addy',
      'phone',
      'resp',
      'aqi',
      'temp',
      'relh',
      'hchoc',
      'tvcoc',
      'cell0',
      'cells',
      'swabs',
      )
    
    radios=(
      'area1',
      'area2',
      'area3',
      'hchos',
      'hchou',
      'tvcos',
      'tvcou',
      )
      
    file='per/{}_Form.txt'.format(self.fname)
    dfile='/{}/Form.txt'.format(self.fname)
      
    with open(file,'w+') as f:
      
      #for all the normal text inputs
      for k in fields:
        
        #record it
        #name
        n=eval('self.{}.text'.format(k))
        #value
        v=eval('self.{}i.text'.format(k))
        f.write(n+' '+v+'\n')

      #for all the radios 
      for k in radios:

        #if its selected
        if eval('self.{}i.active'.format(k)):
          #record it
          line=eval('self.{}.text'.format(k))+' '+eval('self.{}.text'.format(k))
          f.write(line+'\n')

    with open(file,'rb') as f:
      
      b=f.read()
      self.db.files_upload(b,dfile)



#page two b
  def show_camera(self):

    
    self.clear_widgets()
    self.rows=3
    self.cols=1
    

    def capture():
      
      #date
      prep=str(datetime.datetime.now()).split('.')[0].split(' ')
      prep=prep[1].replace(':','_')
      
      #local img
      self.imgname = '{}/Image_{}'.format(self.fname, prep)
      self.pngnames=[]
      self.camera.export_to_png('per/{}_{}'.format(self.fname, self.imgname))
      png='per/{}_{}.png'.format(self.fname, self.imgname)
      with open(lefile,'rb') as f:
        f=f.read()
        self.db.files_upload(f,'/'+self.imgname)

    self.camera=Camera()
    self.camera.bind(on_press=lambda *x: capture())
    self.add_widget(self.camera)
    b=Button(
      text='Take Picture',
      halign='center',
      valign='middle',
      )
    b.bind(on_press=lambda *x: capture())
    self.add_widget(b)
    s=Button(
      text='Show Form',
      halign='center',
      valign='middle',
      )
    s.bind(on_press=lambda *x: self.show_form())
    self.add_widget(s)
                                                        


#page two a
  def show_form(self):
      
      
    #clear old screen
    self.clear_widgets()


    #init persistent aesthetics
    self.cols=1
    self.rows=1
    Window.clearcolor=(1,1,1,1)
    self.background_color=(1,1,1,1)
                                                        
   
    #scroll
    self.scroll=ScrollView(
      size_hint=(1,None),
      size=(Window.width,Window.height))
    self.add_widget(self.scroll)
      
      
    #to hold key/value columns and submit button
    self.archgrid=GridLayout(
      rows=3,
      cols=1,
      size_hint_y=None,
      spacing=0,
      height=Window.height)
    self.archgrid.bind(minimum_height=self.archgrid.setter('height'))
    self.scroll.add_widget(self.archgrid)
      
    
    #separate key from value
    elf=self.grid=GridLayout(
      cols=2,
      rows=1,
      size_hint_y=None,
      height=Window.width*16/9)
    self.archgrid.add_widget(elf)
      
     
    #key column
    elf.labels=cola=GridLayout(
      cols=1,
      size_hint=(1,None),
      spacing=10,
      height=Window.width*16/9)
    elf.add_widget(elf.labels)
      
     
    #value column
    elf.inputs=colb=GridLayout(
      cols=1,
      size_hint=(2,None),
      spacing=10,
      height=Window.width*16/9)
    elf.add_widget(elf.inputs)
      
     
    #tech name
    self.tech=Label(text='Tech Name:',color=(.5,.5,.5,1))
    cola.add_widget(self.tech)
    self.techg=GridLayout(cols=1,rows=3)
    self.techg.add_widget(Label())
    self.techi=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.techg.add_widget(self.techi)
    self.techg.add_widget(Label())
    colb.add_widget(self.techg)
      
     
    #customer name
    self.cust=Label(text='Customer Name:',color=(.5,.5,.5,1))
    cola.add_widget(self.cust)
    self.custg=GridLayout(cols=1,rows=3)
    self.custg.add_widget(Label())
    self.custi=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.custg.add_widget(self.custi)
    self.custg.add_widget(Label())
    colb.add_widget(self.custg)
      
      
    #address
    self.addy=Label(text='Address:',color=(.5,.5,.5,1))
    cola.add_widget(self.addy)
    self.addyg=GridLayout(cols=1,rows=3)
    self.addyg.add_widget(Label())
    self.addyi=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.addyg.add_widget(self.addyi)
    self.addyg.add_widget(Label())
    colb.add_widget(self.addyg)
     
    
    #phone
    self.phone=Label(text='Cust Phone #:',color=(.5,.5,.5,1))
    cola.add_widget(self.phone)
    self.phoneg=GridLayout(cols=1,rows=3)
    self.phoneg.add_widget(Label())
    self.phonei=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.phoneg.add_widget(self.phonei)
    self.phoneg.add_widget(Label())
    colb.add_widget(self.phoneg)
      
     
    #area
    self.area=Label(text='Contaminated Area:',color=(.5,.5,.5,1))
    cola.add_widget(self.area)
    cola.add_widget(Label())
    colb.area=GridLayout(cols=2,rows=3)
    self.areag=colb.area
    self.area1=Label(text='Level 1',color=(0,0,0,1))
    self.areag.add_widget(self.area1)
    self.area1i=CheckBox(group='area',color=(0,0,0,3))
    self.areag.add_widget(self.area1i)
    self.area2=Label(text='Level 2',color=(0,0,0,1))
    self.areag.add_widget(self.area2)
    self.area2i=CheckBox(group='area',color=(0,0,0,3))
    self.areag.add_widget(self.area2i)
    self.area3=Label(text='Level 3',color=(0,0,0,1))
    self.areag.add_widget(self.area3)
    self.area3i=CheckBox(group='area',color=(0,0,0,3))
    self.areag.add_widget(self.area3i)
    colb.add_widget(self.areag)
    colb.add_widget(Label())
    
    
    #respirable particulates
    self.resp=Label(text='Respirable Particulates:',color=(.5,.5,.5,1))
    cola.add_widget(self.resp)
    self.respg=GridLayout(cols=1,rows=3)
    self.respg.add_widget(Label())
    self.respi=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.respg.add_widget(self.respi)
    self.respg.add_widget(Label())
    colb.add_widget(self.respg)
      
      
    #aqi
    self.aqi=Label(text='A.Q.I.:',color=(.5,.5,.5,1))
    cola.add_widget(self.aqi)
    self.aqig=GridLayout(cols=1,rows=3)
    self.aqig.add_widget(Label())
    self.aqii=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.aqig.add_widget(self.aqii)
    self.aqig.add_widget(Label())
    colb.add_widget(self.aqig)
      
    
    #temp
    self.temp=Label(text='Temperature:',color=(.5,.5,.5,1))
    cola.add_widget(self.temp)
    self.tempg=GridLayout(cols=1,rows=3)
    self.tempg.add_widget(Label())
    self.tempi=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.tempg.add_widget(self.tempi)
    self.tempg.add_widget(Label())
    colb.add_widget(self.tempg)
      
    
    #relative humidity
    self.relh=Label(text='Relative Humidity:',color=(.5,.5,.5,1))
    cola.add_widget(self.relh)
    self.relhg=GridLayout(cols=1,rows=3)
    self.relhg.add_widget(Label())
    self.relhi=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.relhg.add_widget(self.relhi)
    self.relhg.add_widget(Label())
    colb.add_widget(self.relhg)
      
  
    #hcho
    self.hcho=Label(
      text='HCHO:',color=(.5,.5,.5,1))
    cola.add_widget(self.hcho)
    #some spacer labels have been removed for aesthetic testing
    #cola.add_widget(Label())
    self.hchog=GridLayout(cols=2,rows=2)
    self.hchos=Label(text='Safe',color=(0,0,0,1))
    self.hchosi=CheckBox(group='hcho',color=(0,0,0,3))
    self.hchou=Label(text='Unsafe',color=(0,0,0,1))
    self.hchoui=CheckBox(group='hcho',color=(0,0,0,3))
    self.hchog.add_widget(self.hchos)
    self.hchog.add_widget(self.hchosi)
    self.hchog.add_widget(self.hchou)
    self.hchog.add_widget(self.hchoui)
    colb.add_widget(self.hchog)
    #colb.add_widget(Label())
    
    
    #hcho count
    self.hchoc=Label(text='HCHO Count:',color=(.5,.5,.5,1))
    cola.add_widget(self.hchoc)
    self.hchocg=GridLayout(cols=1,rows=3)
    self.hchocg.add_widget(Label())
    self.hchoci=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.hchocg.add_widget(self.hchoci)
    self.hchocg.add_widget(Label())
    colb.add_widget(self.hchocg)
      
    
    #tvco
    self.tvco=Label(
    text='TVCO:',color=(.5,.5,.5,1))
    cola.add_widget(self.tvco)
    #cola.add_widget(Label())
    self.tvcog=GridLayout(cols=2,rows=2)
    self.tvcos=Label(text='Safe',color=(0,0,0,1))
    self.tvcosi=CheckBox(group='tvco',color=(0,0,0,3))
    self.tvcou=Label(text='Unsafe',color=(0,0,0,1))
    self.tvcoui=CheckBox(group='tvco',color=(0,0,0,3))
    self.tvcog.add_widget(self.tvcos)
    self.tvcog.add_widget(self.tvcosi)
    self.tvcog.add_widget(self.tvcou)
    self.tvcog.add_widget(self.tvcoui)
    colb.add_widget(self.tvcog)
    #colb.add_widget(Label())
      
    
    #tvco count
    self.tvcoc=Label(text='TVCO Count:',color=(.5,.5,.5,1))
    cola.add_widget(self.tvcoc)
    self.tvcocg=GridLayout(cols=1,rows=3)
    self.tvcocg.add_widget(Label())
    self.tvcoci=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.tvcocg.add_widget(self.tvcoci)
    self.tvcocg.add_widget(Label())
    colb.add_widget(self.tvcocg)
      
     
    #control cell
    self.cell0=Label(text='Control Cell:',color=(.5,.5,.5,1))
    cola.add_widget(self.cell0)
    self.cell0g=GridLayout(cols=1,rows=3)
    self.cell0g.add_widget(Label())
    self.cell0i=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.cell0g.add_widget(self.cell0i)
    self.cell0g.add_widget(Label())
    colb.add_widget(self.cell0g)
      
     
    #number of cells
    self.cells=Label(text='Number of Cells:',color=(.5,.5,.5,1))
    cola.add_widget(self.cells)
    self.cellsg=GridLayout(cols=1,rows=3)
    self.cellsg.add_widget(Label())
    self.cellsi=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.cellsg.add_widget(self.cellsi)
    self.cellsg.add_widget(Label())
    colb.add_widget(self.cellsg)
      
      
    #number of swabs
    self.swabs=Label(text='Number of swabs:',color=(.5,.5,.5,1))
    cola.add_widget(self.swabs)
    self.swabsg=GridLayout(cols=1,rows=3)
    self.swabsg.add_widget(Label())
    self.swabsi=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    self.swabsg.add_widget(self.swabsi)
    self.swabsg.add_widget(Label())
    colb.add_widget(self.swabsg)
      
      
    #camera button
    submit=self.scroll.submit=Button(
      text='Take Pictures',
      size_hint=(1,None),
      height=Window.width/6,
      background_color=(2,2,2,1),
      color=(.2,.2,.2,1),
      )
    submit.bind(on_press=lambda *x: self.show_camera())
    self.archgrid.add_widget(submit)


    #done button
    done=self.scroll.done=Button(
      text='Done',
      size_hint=(1,None),
      height=Window.width/6,
      background_color=(2,2,2,1),
      color=(.2,.2,.2,1),
      )
    done.bind(on_press=lambda *x: self.submit_form())
    self.archgrid.add_widget(done)



#run when done w page one
  def sign_contract(self):


    #init
    self.fname=(self.n.i.text.split(' ')[1].capitalize()+','+self.n.i.text.split(' ')[0].capitalize())
    if self.a.i.text:
      self.fname+=('-'+self.a.i.text)
    
    self.fields={
      'n':'Print Name Owner/Agent: ',
      'a':'Address: ',
      'd':'Date: ',
      'p':'Customer Phone: ',
      'l':'Claim #: ',
      'ni':'Insurance Name: ',
      'np':'Insurance Phone: ',
      }

    def find_start(key):
      return self.txt.index(key)+len(key)
    

    #populate contract
    with open('per/contract.txt','r') as f:
      self.txt=f.read()
    
    for k in self.fields.keys():
      start=find_start(self.fields[k])
      self.txt=list(self.txt)
      for i,char in enumerate(list('self.{}.i.text'.format(k))):
        self.txt[start+i]=char
      self.txt=''.join(self.txt)
    
    with open('per/newcontract.txt','w') as f:
      f.write(self.txt)
      
    
    #change to pdf
    os.system('python per/txt2pdf/txt2pdf.py per/newcontract.txt -o per/newcontract.pdf')
    

    #display loading
    self.clear_widgets()
    self.add_widget(Label(text="Uploading...",width=Window.width))

    
    #upload to dropbox
    token='tmb24v3GWVAAAAAAAAAACo39DcRf542tDsVBKRuYwPrCFE1zBQ_VeoImypDesKxR'
    print(self.fname)
    dest_file='/{}/Contract.pdf'.format(self.fname)
    self.db=dropbox.Dropbox(token)
    with open('per/newcontract.pdf','rb') as f:
      f=f.read()
      self.db.files_upload(f,dest_file)

    
    #show page two         
    self.show_form()




#page one
  def show_contract(self):

    
    #start fresh
    self.clear_widgets()
    self.cols=1
    self.rows=1

    
    #scroll
    s=ScrollView(
      size_hint=(1,None),
      size=(Window.width,Window.height))
    self.add_widget(s)

    
    #main grid
    g=GridLayout(
      cols=1,
      rows=3,
      size_hint=(1,None),
      height=Window.height)
    g.bind(minimum_height=g.setter('height'))
    s.add_widget(g)
    
    
    #contract
    c=Label(
      size_hint=(1,None),
      halign='center',
      )
    with open('per/contract.txt','r') as f:
      c.text=f.read().split('Print Name Owner')[0]
    c.bind(width=lambda *x: c.setter('text_size')(c, (c.width, None)))
    c.bind(texture_size=lambda *x: c.setter('height')(c, c.texture_size[1]))
    g.add_widget(c)


    #standing divisor
    r=GridLayout(
      cols=2,
      rows=2,
      size_hint=(1,None),
      height=Window.height)
    r.bind(minimum_height=r.setter('height'))
    g.add_widget(r)


    #keys
    k=GridLayout(
      cols=1,
      rows=7,
      size_hint=(1,None),
      height=Window.height)
    k.bind(minimum_height=k.setter('height'))
    r.add_widget(k)


    #values
    v=GridLayout(
      cols=1,
      rows=7,
      size_hint=(1,None),
      height=Window.height)
    v.bind(minimum_height=v.setter('height'))
    r.add_widget(v)
    
    
    #name
    n=self.n=Label(text='Customer Name:',color=(.5,.5,.5,1))
    
    n.g=GridLayout(cols=1,rows=3)
    
    n.i=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    
    n.g.add_widget(Label())
    n.g.add_widget(n.i)
    n.g.add_widget(Label())
    
    k.add_widget(n)
    v.add_widget(n.g)
    
    
    #addy
    a=self.a=Label(text='Customer Address:',color=(.5,.5,.5,1))
    
    a.g=GridLayout(cols=1,rows=3)
    
    a.i=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    
    a.g.add_widget(Label())
    a.g.add_widget(a.i)
    a.g.add_widget(Label())
    
    k.add_widget(a)
    v.add_widget(a.g)
    
    
    #phone
    p=self.p=Label(text='Customer Phone #:',color=(.5,.5,.5,1))
    
    p.g=GridLayout(cols=1,rows=3)
    
    p.i=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    
    p.g.add_widget(Label())
    p.g.add_widget(p.i)
    p.g.add_widget(Label())
    
    k.add_widget(p)
    v.add_widget(p.g)

    
    #claim
    l=self.l=Label(text='Insurance Claim #:',color=(.5,.5,.5,1))
    
    l.g=GridLayout(cols=1,rows=3)
    
    l.i=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    
    l.g.add_widget(Label())
    l.g.add_widget(l.i)
    l.g.add_widget(Label())
    
    k.add_widget(l)
    v.add_widget(l.g)
    
    
    #insurance name
    ni=self.ni=Label(text='Insurance Name:',color=(.5,.5,.5,1))
    
    ni.g=GridLayout(cols=1,rows=3)
    
    ni.i=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    
    ni.g.add_widget(Label())
    ni.g.add_widget(ni.i)
    ni.g.add_widget(Label())
    
    k.add_widget(ni)
    v.add_widget(ni.g)
    
    
    #insurance phone
    np=self.np=Label(text='Insurance Phone #:',color=(.5,.5,.5,1))
    
    np.g=GridLayout(cols=1,rows=3)
    
    np.i=TextInput(
      text='',
      foreground_color=(0,0,0,1))
    
    np.g.add_widget(Label())
    np.g.add_widget(np.i)
    np.g.add_widget(Label())
    
    k.add_widget(np)
    v.add_widget(np.g)
    
    
    #date
    d=self.d=Label(text='Date:',color=(.5,.5,.5,1))
    
    d.g=GridLayout(cols=1,rows=3)
    
    d.i=TextInput(foreground_color=(0,0,0,1))
    x=str(datetime.datetime.now()).split(' ')[0].split('-')
    self.rightdate='/'.join(['/'.join(x[1:]),str(x[0])])
    d.i.text=self.rightdate
    
    d.g.add_widget(Label())
    d.g.add_widget(d.i)
    d.g.add_widget(Label())
    
    k.add_widget(d)
    v.add_widget(d.g)
           
    
    #button
    b=Button(
      size_hint=(1,None),
      text='Sign Contract')
    b.bind(on_press=lambda *x: self.sign_contract())
    g.add_widget(b)
           


#start the app at page one
  def __init__(self,**kwargs):

    
    #safe init
    super(RootWidget,self).__init__(**kwargs)
    self.show_contract()

      
class RoofMasterApp(App):
  def build(self):
    return RootWidget()
  

if __name__=='__main__':
  RoofMasterApp().run()
