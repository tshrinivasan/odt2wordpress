#Program to convert a LibreOffice Document ODT file to a Wordpress Blog Post
#Author: T Shrinivasan
#Email: tshrinivasan@gmail.com


import lxml.html.clean as clean
import codecs
import sys
import os
from os.path import basename
from subprocess import call
import os
import urllib
import sys
from BeautifulSoup import BeautifulSoup
import shutil

call(["odt2html", sys.argv[1]])
name = basename(sys.argv[1])
name = os.path.splitext(sys.argv[1])[0]

print name
file = codecs.open(name + ".html", encoding='utf-8', mode='r')
h = file.read()
C = clean.Cleaner(style = True, page_structure = True, remove_tags = ['FONT', 'font', 'span'])
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


from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo


wordpress_rpc_url = "TYPE XML RPC URL FOR WORDPRESS HERE"
wordpress_username = "TYPE WORDPRESS USERNAME HERE"
wordpress_password = "TYPE WORDPRESS PASSWORD HERE"

wp = Client('wordpress_rpc_url', 'wordpress_username', 'wordpress_password')

for image in os.listdir("."):
    if image.endswith(".png") or image.endswith(".gif") or image.endswith(".jpg"):

        image_url = urllib.pathname2url(image)
        filename = image

        data = {
        'name': image,
        'type': 'image/png',  # mimetype
        }

        # read the binary file and let the XMLRPC library encode it into base64
        with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

        response = wp.call(media.UploadFile(data))
# response == {
#       'id': 6,
#       'file': 'picture.jpg'
#       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
#       'type': 'image/jpg',
# }
        attachment_id = response['id']
        url = response['url']
        image_file = response['file']
#        print response
        clean_file = name + "-clean.html"
        contents = open(clean_file).read()
        soup = BeautifulSoup(contents)

        for img in soup.findAll('img'):
#            print image_url
            if img['src'] == image_url or img['src'] == image_file :
                img['src'] = url
#                print url
                img['align'] = "center"

#        print soup
        new_contents = str(soup)
        output_filename = name + "-clean.html"
        open(output_filename, "w").write(new_contents)






def clean():
    print "cleaning"
    for image in os.listdir("."):
        if image.endswith(".png") or  image.endswith(".html") or image.endswith(".gif") or image.endswith(".jpg"):
            source = image
            destination = "./uploaded/" + image
            if os.path.isdir("uploaded"):
                shutil.move(source, destination)
            else:
                os.mkdir("uploaded")
                shutil.move(source, destination)
#print "Moving the file " + image + " to the folder 'uploaded' "


f= open(name + "-clean.html")
test = f.read()
post = WordPressPost()

post.title = name
post.content = test
#post.post_status = 'publish'

try:
	wp.call(NewPost(post))
except:
    clean()

clean()	


