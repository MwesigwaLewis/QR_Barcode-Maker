from flask import Flask,render_template,request,redirect,url_for,session,send_file
import barcode
from barcode.writer import ImageWriter
from barcode.codex import Code128
import qrcode
import os
import uuid



app=Flask(__name__)
app.secret_key="hNJKDSNjdbcjhdfvbjfhdjkKJNKgdfg5df5g45dfjgbjknkfg5g15fdjbhbgfctgyJ545454"

GENERATED_DIR = os.path.join('static', 'generated')
os.makedirs(GENERATED_DIR, exist_ok=True)

@app.route('/', methods=['GET','POST'])
def code_creation():
   
    if request.method == 'POST':
        text=request.form.get('text-input')
        action=request.form.get('action')

        if text is None:
            return('Invalid Input')

        unique_name= f'{uuid.uuid4().hex}.png'
        file_path = os.path.join(GENERATED_DIR, unique_name)
        
        if action == 'qr_code':
            img = qrcode.make(text)
            img.save(file_path)
            session['code_filename'] = unique_name
            session['code_type'] = 'qr'

        if action == 'bar_code':
            code = Code128(
                text,
                writer=ImageWriter()
            )
            code.save(os.path.join(GENERATED_DIR, unique_name[:-4]))  # Save without the .png extension, that's the meaning of the unique_name[:-4] part
            session['code_filename'] = unique_name
            session['code_type'] = 'barcode'

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
<<<<<<< HEAD
      filename= session.get('code_filename')

      if not filename:
=======
      if not session.get('bar_created') or session.get('qr_created'):
>>>>>>> 9467b2f356157dfa4c5466df15a333f4a6255a95
           return redirect(url_for('code_creation'))
      return render_template('output.html', filename=filename)

@app.route('/download')
def download():
     filename = session.get('code_filename')
     if not filename:
         return redirect(url_for('code_creation'))
     return send_file(
        os.path.join(GENERATED_DIR, filename),
        as_attachment=True,
        download_name="Your_Code.png"
     )

if __name__=="__main__":
<<<<<<< HEAD
    app.run(debug=True,
            host='0.0.0.0',
            port='5600'
    )
=======
      app.run(debug=True,
              host='0.0.0.0',
              port='5600'
        )
>>>>>>> 9467b2f356157dfa4c5466df15a333f4a6255a95
