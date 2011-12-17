#! /usr/bin/python
# coding: utf-8
import sys
import os
import cgi
import base64
import urllib

fs = cgi.FieldStorage()

LOGO_PATH = './concentrate.png'

tmpl = """<!DOCTYPE html>
<head>
    <meta charset="utf-8"/>
    <title>集中線アイコンジェネレータ</title>
</head>
<body>
    <h1>集中線アイコンジェネレータ</h1>
    <p>
        強いられているんだ！
    </p>
    <p><img src="data:image/png;base64,%s"/>     <img src="data:image/png;base64,%s"/></p>
    <form method="get" action="%s">
        <p>ユーザ: <input type="text" name="screen_name" value="%s"/></p>
        <p><input type="submit" value="生成"/></p>
    </form>
    <div>
        %s
    </div>
    <br/>
    <div>
        <p><a href="http://twitpic.com/7im4v9">合成に使わせてもらった元画像</a></p>
    </div>
</body>
</html>
"""
tag = ''

screen_name = fs.getvalue('screen_name', '').strip()

if screen_name != '':
    # fetch user iamge via api    
    # see: http://tweetimag.es/
    url = 'http://img.tweetimag.es/i/%s_b' % screen_name
    pid = str(os.getpid())
    try:
        ico = urllib.urlopen(url).read()
        fout = open(pid, 'wb')
        fout.write(ico)
        fout.close()
        # process image
        os.system('convert %s %s.png' % (pid, pid)) # transparentize
        os.system('mv %s.png %s' % (pid, pid))
        #os.system('convert %s -matte -virtual-pixel transparent -distort Perspective "0,0 18,19 0,73 21,53 73,0 54,19 73,73 51,53" %s' % (pid, pid))
        os.system('convert %s %s -composite %s' % (pid, LOGO_PATH, pid))
        #os.system('convert -resize 73x73! %s %s' % (pid, pid))

        # encode icon image as base64
        enc = open(pid, 'rb').read().encode('base64')
        
        tag = '<img src="data:image/png;base64,%s"/>' % ico.encode('base64')
        tag += ' → '
        tag += '<img src="data:image/png;base64,%s"/>' % enc
    except Exception, e:
        sys.stderr.write(str(e))
    finally:
        if os.path.exists(pid):
            os.remove(pid)
        

print 'Content-Type: text/html; charset=utf-8'
print ''
print tmpl % (open('icon-b64.txt').read(), open('ic-b64.txt').read(), os.environ['SCRIPT_NAME'], screen_name, tag)

