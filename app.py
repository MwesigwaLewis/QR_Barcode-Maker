from flask import Flask,render_template,request,redirect,url_for,session,send_file
import barcode
from barcode.writer import ImageWriter
from barcode.codex import Code128
import qrcode



app=Flask(__name__)
app.secret_key="hNJKDSNjdbcjhdfvbjfhdjkKJNKgdfg5df5g45dfjgbjknkfg5g15fdjbhbgfctgyJ545454"


@app.route('/', methods=['GET','POST'])
def code_creation():
   
    if request.method == 'POST':
        text=request.form.get('text-input')
        action=request.form.get('action')

        if text is None:
            return('Invalid Input')
        
        if action == 'qr_code':
            img = qrcode.make(text)
            img.save("static/code.png")
            session['qr_created']=True

        if action == 'bar_code':
            code = Code128(
                text,
                writer=ImageWriter()
            )
            code.save('static/code')
            session['bar_created']=True

        return redirect(url_for('output'))

    return render_template('index.html')
    
 


'''
@app.route('/', methods=['GET','POST'])
def make_barcode():
    if request.method == 'POST':
        text=request.form.get('text-input')
        code = Code128(
              text,
              writer=ImageWriter()
         ) 
        code.save("static/barcode")
        session['bar_created']=True
        return redirect(url_for('output'))
    return render_template('index.html')
'''


@app.route('/output')
def output():
      if not session.get('bar_created') or session.get('qr_created'):
           return redirect(url_for('code_creation'))
      return render_template('output.html')

@app.route('/download')
def download():
     return send_file(
        "static/code.png",
        as_attachment=True,
        download_name="Your_Code.png"
     )

if __name__=="main":
      app.run(debug=True,
              host='0.0.0.0',
              port='5600'
        )
