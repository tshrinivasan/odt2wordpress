#Program to convert a LibreOffice Document ODT file to a Wordpress Blog Post

import lxml.html.clean as clean
import codecs
import sys
import os
from os.path import basename
from subprocess import call
call(["odt2html",sys.argv[1]])
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



from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
wp = Client('http://localhost/wordpress/xmlrpc.php', 'admin', 'admin')
f= open(name + "-clean.html")
test = f.read()
post = WordPressPost()

post.title = name
post.content = test
wp.call(NewPost(post))

