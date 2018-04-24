from flask import Flask, render_template, request
import json

w = json.load(open("worldl.json"))
for c in w:
	c['tld'] = c['tld'][1:]
cba = sorted(list(set([c['name'][0] for c in w])))
print(cba)
page_size = 20
app = Flask(__name__)

@app.route('/')
def mainPage():
	return render_template('index.html',
		w = w[0:page_size],
		page_number = 0,
		page_size = page_size,
                cba = cba)

@app.route('/begin/<b>')
def beginPage(b):
	bn = int(b)
	return render_template('index.html',
		w = w[bn:bn+page_size],
		page_number = bn,
		page_size = page_size,
                cba = cba)

@app.route('/continent/<a>')
def continentPage(a):
	cl = [c for c in w if c['continent']==a]
	return render_template(
		'continent.html',
		length_of_cl = len(cl),
		cl = cl,
		a = a
		)

@app.route('/country/<i>')
def countryPage(i):
	return render_template(
		'country.html',
		c = w[int(i)])

@app.route('/countrybyalpha/<a>')
def countrybyalpha(a):
	cl = [c for c in w if c['name'][0]==a]
	return render_template(
		'countrybyalpha.html',
		length_of_cl = len(cl),
		cl = cl,
		a = a
		)

@app.route('/countryByName/<n>')
def countryByNamePage(n):
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	return render_template(
		'country.html',
		c = c)

@app.route('/delete/<n>')
def deleteCountry(n):
        i = 0
        for c in w:
                if c['name']==n:
                        break
                i = i+1
        del w[i]
        return render_template('index.html',
                               w = w[0:page_size],
                               page_number = 0,
                               page_size = page_size)

@app.route('/editcountrybyname/<n>')
def editCountryByName(n):
        c = None
        for x in w:
                if x['name'] == n:
                        c=x
        return render_template('countryedit.html',
                               c = c)

@app.route('/updatecountrybyname')
def updateCountryByName():
        n = request.args.get('name')
        c = None
        for x in w:
                if x['name']==n:
                        c = x
        c['capital'] = request.args.get('capital')
        c['continent'] = request.args.get('continent')
        c['area'] = request.args.get('area')
        c['population'] = request.args.get('population')
        c['gdp'] = request.args.get('gdp')
        c['tld'] = request.args.get('tld')
        return render_template('country.html',
                               c = c)
@app.route('/createcountrybyname')
def createcountrybyname():
        return render_template('create.html', c=c)

@app.route('/docountrybyname')
def doCountryByName():
        n = request.args.get('name')
        c = {}
        c['name'] = request.args.get('name')
        c['capital'] = request.args.get('capital')
        c['continent'] = request.args.get('continent')
        c['area'] = request.args.get('area')
        c['population'] = request.args.get('population')
        c['gdp'] = request.args.get('gdp')
        c['tld'] = request.args.get('tld')
        w.append(c)
        w.sort(key=lambda c:c['name'])
        return render_template('country.html',
                               c = c)


app.run(host='0.0.0.0', port=5627, debug=True)






