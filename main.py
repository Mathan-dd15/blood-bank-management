from flask import Flask,request,render_template,session,abort,redirect,url_for
from models import user,Req_donner_details,Active_donner_details,fund_donation,db,Feedback
from sqlalchemy import and_



app = Flask(__name__)

app.secret_key ='Mathan'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/blood_bank'
db.init_app(app)

with app.app_context():
        db.create_all()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route("/about")
def About():
    return render_template('about.html')

@app.route('/admin')
def admin():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('admin.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():

    Error = None
    name = request.form['username']
    password = request.form['password']
    
    User = user.query.filter_by(username=name).first()
    if User:
        if User.password == password:
            session['username'] = name
            return redirect(url_for('dashboard'))
        else:
            Error = 'Invalied Password'
    else:
        Error = 'Invalied Username'

    return render_template('admin.html',error = Error)
    
@app.route('/logout')
def logout():
    session.pop('username',None)
    return render_template ('admin.html')
      
@app.route('/Blood_Donor')
def blood_Donor():
    return render_template('Req_donor_details.html')

@app.route('/add_donor_details', methods=['POST'])
def req_donor_details():

    name = request.form['name']
    gender = request.form['gender']
    email = request.form['email']
    address = request.form['address']
    state = request.form['state']
    district = request.form['district']
    bloodgroup = request.form['bloodgroup']
    message = request.form['message']
    phone = request.form['phone']

    new_data = Req_donner_details(
        Name=name,
        Email=email,
        Gender=gender,
        Address=address,
        State=state,
        District=district,
        BloodGroup=bloodgroup,
        Message=message,
        Phone=phone
    )

    db.session.add(new_data)
    db.session.commit()

    return render_template('add_data.html')

@app.route('/verify_donnor/<id>')
def verify_donnor(id):
    donnor = Req_donner_details.query.filter_by(id=id).first()
    return render_template('verify.html',Req_Donnor = donnor)

@app.route('/cancel_req/<id>')
def cancel_req(id):
    del_req = Req_donner_details.query.filter_by(id = id).first()
    db.session.delete(del_req)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route('/approve_req/<id>')
def approve_req(id):
    donor = Req_donner_details.query.filter_by(id=id).first()
    new_data = Active_donner_details(
        Name=donor.Name,
        Email=donor.Email,
        Gender=donor.Gender,
        Address=donor.Address,
        State=donor.State,
        District=donor.District,
        BloodGroup=donor.BloodGroup,
        Message=donor.Message,
        Phone=donor.Phone
        )
    db.session.add(new_data)
    db.session.commit()

    del_req = Req_donner_details.query.filter_by(id = id).first()
    db.session.delete(del_req)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/user_active_Donors',methods = ['POST','GET'])
def user_active_Donors():
    if request.method == 'POST':
        blood,location = request.form['BloodGroup'],request.form['District']

        if blood == 'None' and location == 'None':
            donors = Active_donner_details.query.all()

        elif blood != 'None' and location == 'None':
            donors = Active_donner_details.query.filter_by(BloodGroup = blood).all()
        
        elif blood == 'None' and location != 'None':
            donors = Active_donner_details.query.filter_by(District = location).all()

        else:
            donors = Active_donner_details.query.filter(and_(Active_donner_details.District == location, Active_donner_details.BloodGroup == blood)).all()
    
    else:
        donors = Active_donner_details.query.all()
    
    return render_template('user_active_Donors.html',Donor = donors)


@app.route('/user_view/<id>')
def user_view(id):
    donors = Active_donner_details.query.filter_by(id = id).first()
    return render_template('user_view.html',Donor = donors)

@app.route('/dashboard')
def dashboard():
    
    donation,donnor = fund_donation.query.all(),Req_donner_details.query.all()
    
    total = len(Active_donner_details.query.all())

    a_positive = len(Active_donner_details.query.filter_by(BloodGroup = 'A+').all())
    a_negative = len(Active_donner_details.query.filter_by(BloodGroup = 'A-').all())
    b_positive = len(Active_donner_details.query.filter_by(BloodGroup = 'B+').all())
    b_negative = len(Active_donner_details.query.filter_by(BloodGroup = 'B-').all())
    ab_positive = len(Active_donner_details.query.filter_by(BloodGroup = 'AB+').all())
    ab_negative = len(Active_donner_details.query.filter_by(BloodGroup = 'AB-').all())
    o_positive = len(Active_donner_details.query.filter_by(BloodGroup = 'O+').all())
    o_negative = len(Active_donner_details.query.filter_by(BloodGroup = 'O-').all())

    return render_template('dashboard.html', Donners=donnor, Donation=donation, Total=total, A_Positive=a_positive, A_Negative=a_negative, B_Positive=b_positive, B_Negative=b_negative,AB_Positive = ab_positive, AB_Negative = ab_negative, O_Positive = o_positive, O_Negative = o_negative)

@app.route('/admin_active_Donors/<filter>')
def admin_active_Donors(filter):
    if filter == 'None':
        donors = Active_donner_details.query.all()
    else:
        donors = Active_donner_details.query.filter_by(BloodGroup = filter).all()
    return render_template('admin_active_donors.html',Donor = donors)


@app.route('/admin_view/<id>')
def admin_view(id):
    donors = Active_donner_details.query.filter_by(id=id).first()
    return render_template('admin_view.html',Donor = donors)

@app.route('/del_active_donor/<id>')
def del_active_donor(id):
    del_req = Active_donner_details.query.filter_by(id=id).first()
    db.session.delete(del_req)
    db.session.commit()
    return redirect(url_for("admin_active_Donors", filter='None'))


@app.route('/Donation')
def Donation():
    return render_template('fund_donation.html')

@app.route('/payment',methods = ['POST'])
def payment():
    session['name'] = request.form['name']
    session['email'] = request.form['email']
    session['amount'] = request.form['amount']
    session['message'] = request.form['message']
    session['payment_method'] = request.form['paymentMethod']
    if session['payment_method'] == "Credit_Card" or session['payment_method'] == "Debit_Card":
        return render_template('payment.html')
    elif session['payment_method'] == "UPI":
        return render_template('UPI.html')

@app.route('/donation_recived')
def donation_recived():
    Fund = fund_donation.query.all()
    return render_template('fund.html',fund = Fund)

@app.route('/success',methods = ['POST'])
def success():
    if session['payment_method'] == "Credit_Card" or session['payment_method'] == "Debit_Card":
                
        cardholder_name = request.form['cardholder-name']
        card_number = request.form['card-number']
        expiry = request.form['expiry']
        cvv = request.form['cvv']

        error = None
        if not cardholder_name:
            error = 'Cardholder name is required.'
        elif not card_number:
            error = 'Card number is required.'
        elif not expiry:
            error = 'Expiry date is required.'
        elif not cvv:
            error = 'CVV is required.'
        elif len(card_number) != 16:
            error = 'Card number must be 16 digits.'
        elif not card_number.isdigit():
            error = 'Card number must contain only digits.'
        elif len(expiry) != 5 or not expiry[0:2].isdigit() or not expiry[3:].isdigit() or expiry[2] != '/':
            error = 'Expiry date must be in the format MM/YY.'
        elif len(cvv) != 3 or not cvv.isdigit():
            error = 'CVV must be a 3-digit number.'

        if error:
            return render_template('payment.html',error = error)
        else:
            name = session['name']
            email = session['email']
            amount = session['amount']
            message = session['message']
            
            new_data = fund_donation(
                Name=name,
                Email=email,
                Donation_amount = amount,
                Message=message
            )

            db.session.add(new_data)
            db.session.commit()

            return render_template('success.html')
    
@app.route('/upi',methods = ['POST'])
def UPI_success():
    if request.method == 'POST':
    
        upi = request.form['upiId']
        if "@" in upi:
            error = None
        else:
            error = 'Invalid UPI ID.'

        if error:
            return render_template('UPI.html', error=error)
        else:
            name = session['name']
            email = session['email']
            amount = session['amount']
            message = session['message']

            new_data = fund_donation(
                Name=name,
                Email=email,
                Donation_amount=amount,
                Message=message
            )

            db.session.add(new_data)
            db.session.commit()

            return render_template('success.html')
    
    return render_template("UPI.html")

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/add_feedback',methods = ['POST'])
def add_feedback():

    name,email = request.form['name'],request.form['email']
    feedback_type,feedBack = request.form['feedback-type'],request.form['comments']

    new_data = Feedback(Name = name, Email = email, Type = feedback_type, Commends = feedBack)

    db.session.add(new_data)
    db.session.commit()
    return render_template('thank_feedback.html')

@app.route('/admin_view_feedback')
def admin_view_feedback():
    data = Feedback.query.all()
    return render_template('admin_feedback.html',feedback = data)

if __name__=='__main__':
    app.run(debug=True)