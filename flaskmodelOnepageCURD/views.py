from flask import flash,render_template,redirect,url_for
from app import app,db
from models import Message
from forms import HelloForm

@app.route('/',methods=['GET','POST'])
def index():
    messages=Message.query.order_by(Message.timestamp.desc()).all()
    form=HelloForm()
    if form.validate_on_submit():
        name=form.name.data
        body=form.body.data
        message=Message(body=body,name=name)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
        return redirect(url_for('index'))
    return render_template('index.html',form=form,messages=messages)
