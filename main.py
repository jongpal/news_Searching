from news import search_results
from flask import Flask,request,render_template,redirect
#import math



app=Flask("searchnews_withkeyword")


db={}

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/request')
def rqst():
  word=request.args.get('search')
  ds=request.args.get('ds')
  de=request.args.get('de')
  
  if word is None:
    return redirect('/')
  else:
    word=word.lower()
    if db.get(word+ds+de):
      news=db[word+ds+de]
      #pgnumber= math.ceil(len(news)/2)
      return render_template("rqst.html",len=len(news), searching=word,news=news)
    else:
      news=search_results(word,ds,de)
      if news is None:
        return render_template("rqst.html",len=0, searching=word,news= "No")
      #pgnumber= math.ceil(len(news)/2)
      else:
        db[word+ds+de]=news    
        return render_template("rqst.html",len=len(news), searching=word,news=news)


app.run(host='0.0.0.0')

