from flask import Flask,render_template,request,redirect,url_for,session,send_file,flash
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

        if not text or not text.strip():
            flash('Please enter some text before generating a code.')
            return redirect(url_for('code_creation'))

        # Unique filename per submission so concurrent users never
        # read, overwrite, or download each other's generated codes.
        unique_name = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(GENERATED_DIR, unique_name)

        if action == 'qr_code':
            img = qrcode.make(text)
            img.save(filepath)
            session['code_filename'] = unique_name
            session['code_type'] = 'qr'

        elif action == 'bar_code':
            try:
                code = Code128(
                    text,
                    writer=ImageWriter()
                )
                # barcode's save() appends .png itself, so give it the path
                # without the extension.
                code.save(os.path.join(GENERATED_DIR, unique_name[:-4]))
            except Exception:
                flash('That text can\'t be encoded as a barcode. Try removing special characters.')
                return redirect(url_for('code_creation'))
            session['code_filename'] = unique_name
            session['code_type'] = 'barcode'

        else:
            flash('Please choose QR Code or Bar Code.')
            return redirect(url_for('code_creation'))

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
      filename = session.get('code_filename')
      code_type = session.get('code_type')
      if not filename:
           return redirect(url_for('code_creation'))
      return render_template('output.html', filename=filename, code_type=code_type)

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
      app.run(debug=False,
              host='0.0.0.0',
              port='5600'
        )