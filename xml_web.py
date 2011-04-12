from xml.sax.handler import ContentHandler
from xml.sax import parse
import os

class Dispatcher: 

    # Basic Event Handlers startElement and endElement are implemented
    # startElement calls a method dispatch() which finds the appropriate
    # handler, ie. 'startName'

    def startElement(self, name, attrs): 
        self.dispatch('start', name, attrs)
    def endElement(self, name): 
        self.dispatch('end', name)
    def dispatch(self, prefix, name, attrs=None): 
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        # sets method to self.mname
        method = getattr(self, mname, None)
        # checks if self.mname exists as a method, creates argument tuple list
        if callable(method): args = ()
        else: 
            method = getattr(self, dname, None)
            #args is a tuple with string name
            args = name,
        # if startTag handler,add in the attrs to the argument tuple (args)     
        if prefix == 'start': args += attrs,
        if callable(method): method(*args)

class WebsiteConstructor(Dispatcher, ContentHandler): 

    passthrough = False

    def __init__(self, directory): 
        # takes the 'first' (not self) argument of WebsiteConstructor(arg)
        # which is a stringa and creates a list with that one element.
        self.directory = [directory]
        self.ensureDirectory()
        
    def ensureDirectory(self): 
        # creates the directory path thru the directory list variable
        # path variable is the list joined thru arguement splicing (*)
        path = os.path.join(*self.directory)
        if not os.path.isdir(path): os.makedirs(path)

    def characters(self, chars):
        if self.passthrough: self.out.write(chars)

    # -------------------------
    # encapsulated the original code to write all other tags inside the <page>
    # tag into handlers defaultStart and defaultEnd
    # original code was in pagemaker.py
    # -------------------------        
    def defaultStart(self, name, attrs): 
        if self.passthrough: 
            self.out.write('<' + name)
            for key, val in attrs.items(): 
                self.out.write(' %s="%s"' % (key, val))
            self.out.write('>')
            
    def defaultEnd(self, name): 
        if self.passthrough: 
            self.out.write('</%s>' % name)

    # -------------------------
    # Two directory handlers
    # -------------------------
    def startDirectory(self, attrs): 
        # updates the directory variable with the current path and checks
        # that it exists
        self.directory.append(attrs['name'])
        self.ensureDirectory()

    def endDirectory(self): 
        self.directory.pop()

    # -------------------------
    # Two page handlers
    # startPage() writes the HTML Header, sets the passthrough variable to True
    # for xhtml elements, and opens (/and creates) the associated HTML file
    # -------------------------    
    
    def startPage(self, attrs): 
        # os.path.join joins several paths with the correct separator
        # uses directory list and adds in the page name.html
        filename = os.path.join(*self.directory+[attrs['name']+'.html'])
        self.out = open(filename, 'w')
        #takes the 'title' key value pair, passes the title name to writeHeader
        self.writeHeader(attrs['title'])
        self.passthrough = True

    def endPage(self): 
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    # -------------------------
    # Encapsulated methods that write Header and Footer HTML
    # -------------------------    
        
    def writeHeader(self, title): 
        self.out.write("<html>\n  <head>\n    <title>")
        self.out.write(title)
        self.out.write("</title>\n  </head>\n  <body>\n")

    def writeFooter(self): 
        self.out.write("\n  </body>\n</html>\n")

parse('SportsPortal.xml', WebsiteConstructor('SportsPortal_html'))

