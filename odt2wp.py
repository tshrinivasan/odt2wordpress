#Program to convert a LibreOffice Document ODT file to a Wordpress Blog Post
#Author: T Shrinivasan 
#Email: tshrinivasan@gmail.com


import lxml.html.clean as clean
import codecs
import sys
import os
from os.path import basename
import subprocess 

def install_odt2html():
  print "odt2html not found - Installing..."
  subprocess.call("sudo apt-get install unoconv",shell=True)
  print "odt2html - Successfully Installed"
  subprocess.call(["odt2html",sys.argv[1]])

def install_wordpress_xmlrpc():
  print "module wordpress_xmlrpc not found - Installing"
  subprocess.call("sudo pip install python-wordpress-xmlrpc",shell=True)
  print "wordpress_xmlrpc - Successfully Installed"
  from wordpress_xmlrpc import Client, WordPressPost

try:
  subprocess.call(["odt2html",sys.argv[1]])
except:
  install_odt2html()


name = basename(sys.argv[1])
name = os.path.splitext(sys.argv[1])[0]

print name
file = codecs.open(name + ".html", encoding='utf-8', mode='r')
h = file.read()
C = clean.Cleaner(style = True, page_structure = True, remove_tags = ['FONT', 'font','span'])
h1 = C.clean_html(h)
outfile = codecs.open(name + "-stripped.html", encoding='utf-8', mode='w')
outfile.write(h1)
file.close()
outfile.close()



fn1 = name + "-stripped.html"
fn2 = name + "-clean.html"
     
f1 = open(fn1)
f2 = open(fn2, 'w')
outputList = [line.strip() for line in f1]
f1.close()
f2.write(" ".join(outputList))
f2.close()


try:
  from wordpress_xmlrpc import Client, WordPressPost
except ImportError:
  install_wordpress_xmlrpc()

from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
wp = Client('http://localhost/wordpress/xmlrpc.php', 'admin', 'admin')
f= open(name + "-clean.html")
test = f.read()
post = WordPressPost()

post.title = name
post.content = test
wp.call(NewPost(post))

