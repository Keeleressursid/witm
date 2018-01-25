#!/usr/bin/python3
# -*- coding: utf-8 -*-

#	kirjuta
def k(tekst):
	print(tekst, end="")

#	kirjuta rida
def kr(tekst):
	print(tekst)

#	kirjuta arv
def a(arv):
	print(arv, sep='',end="")

def pais(title):
	k("<html lang=\"et\">\n <head>\n  <title>")
	k(title)
	k("</title>")
	kr(" <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>")
	kr(" <link rel=\"stylesheet\" href=\"/witm.css\" type=\"text/css\">")
	kr(" <style type=\"text/css\" media=\"screen\">")
	kr(" </style>")
	kr(" </head>\n<body>")
	s = ""
	return s

def päis(title):
	kr("<html lang=\"et\">")
	k(" <head>\r\n <title>")
	k(title)
	kr(" </title>")
	kr(" <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>")
	kr(" <link rel=\"stylesheet\" href=\"/witm.css\" type=\"text/css\">")
	kr(" <style type=\"text/css\" media=\"screen\">")
	kr(" </style>")
	kr(" </head>")
	kr("<body>")

def kehaalgus():
	kr("<div id=\"keha\">")
	kr("<div id=\"kast\">")
	kr("<div id=\"yl\">")

def avalehealgus():
	kr("<h3>Võro keele paralleelkorpused ja masintõlked</h3>")
	kr("</div>")	# yl
	kr("<br>")

def tõlkemasinalähtetekstiaken():
	viide = "/?z=t"
	vorm(viide)
	kr("<a href = \"tmkommentaarid.html\">Tõlkemasina kommentaarid</a>")
	tabel_a()
	tr_a()
	tr_l()
	tabel_l()
	tabel_a()
	kr("<tr><td><textarea cols=\"72\" rows=\"3\" name='tekst'></textarea></td></tr>")
	submit('2','tõlgi')
	tabel_l()

# Enne avalikustamist välja võtta..., kui vro-etiga edasi töötada, siis normaalsem tugi kirjutada
def tõlkemasinalähtetekstiaken_vroet():
	viide = "/vroet.py?z=t"
	vorm(viide)
	kr("<a href = \"tmkommentaarid.html\">Tõlkemasina kommentaarid</a>")
	tabel_a()
	tr_a()
	tr_l()
	tabel_l()
	tabel_a()
	kr("<tr><td><textarea cols=\"72\" rows=\"3\" name='tekst'></textarea></td></tr>")
	submit('2','tõlgi')
	tabel_l()

def jalus():
	kr("</div>\r\n</div>\r\n</body>\r\n</html>\r\n")

def viide(hüperviide,kiri):
	k("<a href = \"")
	k(hüperviide)
	k("\">")
	k(kiri)
	k("</a>")

def ftd(sisu,klass):
	import string
	sisu = str(sisu)
	sisu = sisu[0:19]
	k("<td class=\"")
	k(klass)
	k("\">")
	k(sisu)
	kr("</td>")

def vtd(sisu,klass):
	import string
	sisu = str(sisu)
	sisu = sisu[0:8]
	k("<td class=\"")
	k(klass)
	k("\">")
	k(sisu)
	kr("</td>")

def td(sisu,klass):
	if sisu == None:
		k("<td class=\"")
		k(klass)
		kr("\"></td>")
	else:
		k("<td class=\"")
		k(klass)
		k("\">")
		k(sisu)
		k("</td>")

def atd(klass,hüperviide,viide):
	k("<td class=\"")
	k(klass)
	k("\"><a href = \"")
	k(hüperviide)
	k("\">")
	k(viide)
	kr("</a></td>")

def tabel_a():
	kr("<table>")

def tabel_l():
	kr("</table>")

def tr_a():
	k("<tr>")

def tr_l():
	k("</tr>")

def inputval(nimi,vaartus,suurus,makspikkus):
	k("<td><input type=\"text\" size=\"")
	k(suurus)
	k("\" maxlenght=\"")
	k(makspikkus)
	k("\" name=\"")
	k(nimi)
	k("\" value=\"")
	k(vaartus)
	kr("\"></td>")

# inaktiivne, vale viitega, aga võibolla läheb veel vaja...
def selectval(name,selected,paring):
	import f
	k("<td>")
	k("<select name='")
	k(name)
	kr("'>")
	for r in f.sqlp(paring):
		if int(selected) == int(r[0]):
			k("<option selected value='")
			k(r[0])
			k("'>")
			k(r[1])
			kr("</option>")
		else:
			k("<option value='")
			k(r[0])
			k("'>")
			k(r[1])
			k("</option>")

	kr("</select>")
	kr("</td>")

def textarea(nimi,vaartus,cols,rows):
	k("<textarea name=\"")
	k(nimi)
	k("\" cols=\"")
	k(cols)
	k("\" rows=\"")
	k(rows)
	k("\">")
	k(vaartus)
	kr("</textarea>")

def textareatd(nimi,vaartus,cols,rows):
	k("<td><textarea name=\"")
	k(nimi)
	k("\" cols=\"")
	k(cols)
	k("\" rows=\"")
	k(rows)
	k("\">")
	k(vaartus)
	kr("</textarea></td>")

def radbox(nimi,vaartus):
	# ei pruugi töötada
	k("<input type=\"radio\" name=\"")
	k(nimi)
	k("\" value=\"")
	k(vaartus)
	kr("\" method=\"post\" />")

def radboxonclick(nimi,vaartus,onclick):
	k("<input type=\"radio\" name=\"")
	k(nimi)
	k("\" value=\"")
	k(vaartus)
	k("\" method=\"post\" onclick=\"location.href='")
	k(onclick)
	kr("'\">")

def chbox(nimi,vaartus):
	k("<input type=\"checkbox\" name=\"")
	k(nimi)
	k("\" value=\"")
	k(vaartus)
	kr("\" method=\"post\" />")

def submit(colspan,kiri):
	k("<tr><td colspan=\"")
	k(colspan)
	k("\"><input type=\"submit\" value=\"")
	k(kiri)
	kr("\"></td></tr>")

def h1(kiri):
	k("<h1>")
	k(kiri)
	kr("</h1>")

def h2(kiri):
	k("<h2>")
	k(kiri)
	kr("</h2>")

def h3(kiri):
	k("<h3>")
	k(kiri)
	kr("</h3>")

def h4(kiri):
	k("<h4>")
	k(kiri)
	kr("</h4>")

def h5(kiri):
	k("<h5>")
	k(kiri)
	kr("</h5>")

def h6(kiri):
	k("<h6>")
	k(kiri)
	kr("</h6>")

def vorm(action):
	k("<form action=\"")
	k(action)
	kr("\" method=\"post\" enctype=\"multipart/form-data\">")
def vormget(action):
	k("<form action=\"")
	k(action)
	kr("\" method=\"get\" enctype=\"multipart/form-data\">")
