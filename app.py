from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine, DateTime
import datetime

app = Flask(__name__)

app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost/concurso_poesia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
Base = declarative_base()
engine = create_engine('postgresql://postgres:password@localhost/concurso_poesia')
db = SQLAlchemy(app)

class Participants(Base,db.Model):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True)
    student_id = Column(String(250),nullable=False)
    name = Column(String(250),nullable=False)
    address =  Column(String(250),nullable=False)
    gender = Column(String(250),nullable=False)
    phone_number = Column(Integer,nullable=False)
    birthday = Column(String(250),nullable=False)
    faculty = Column(String(250),nullable=False)
    poetry_gender = Column(String(170),nullable=False)
    inscription_date =  Column(DateTime,nullable=False)
    presentation_date = Column(String(250),nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/', methods=['POST'])
def home(): 
       data = request.form
       delta_day = datetime.timedelta(days=5)

       inscription_date=datetime.datetime.now()

       poetry_gender=data['genero de poesia']

       newdate=delta_day+inscription_date

       stringdate=newdate.strftime("%A, %B %d, %Y")

       presentation_ends_3 =  datetime.datetime(2022,12,30)

       stringdate_ends_3 = presentation_ends_3.strftime("%A, %B %d, %Y")

       rest_presentations = datetime.datetime(2022,12,2)

       stringdate_rest=rest_presentations.strftime("%A, %B %d, %Y")

       student_id=data['carnet']
      
       if (student_id.endswith("1") or student_id.endswith("3") or student_id.endswith("9"))== True :
        if (student_id.endswith("1")==True and poetry_gender=="dramatica"): 
                presentation_date1=stringdate
        elif(student_id.endswith("3")==True and poetry_gender=="epica"):presentation_date1 = stringdate_ends_3
        else: presentation_date1= stringdate_rest
        if student_id[0] == "A" and student_id[2] == "5":
            new_participant = Participants(
            student_id=data['carnet'],
            name=data['nombre completo'], 
            address=data['direccion'], 
            gender=data['genero'], 
            phone_number=data['numero de telefono'], 
            birthday=data['fecha de nacimiento'], 
            faculty=data['carrera'], 
            poetry_gender=data['genero de poesia'], 
            inscription_date=datetime.datetime.now(),
            presentation_date=presentation_date1)
            db.session.add(new_participant)
            db.session.commit()
        else: return "El carnet es incorrecto, ingresalo de nuevo"

       else:return "El carnet es incorrecto, ingresalo de nuevo"

       if student_id.endswith("1") and poetry_gender=="dramatica":
        return f"La fecha de tu presentacion es {stringdate}."
       
       elif student_id.endswith("3") and poetry_gender=="epica":
        return f"La fecha de tu presentacion es {stringdate_ends_3}."
       
       
       return f"La fecha de tu presentacion es {stringdate_rest}."

@app.route('/participantes', methods=['GET'])
def participants():  
   participants = Participants.query.all()
   result = []   
   for participant in participants:   
       user_data = {   
      'id' : participant.id,
      'Nombre':participant.name, 
      'Carrera' : participant.faculty, 
      'Fecha de Nacimiento': participant.birthday,
      'Genero de Poesia' : participant.poetry_gender,
      'Fecha de Declamacion': participant.presentation_date,
       }
       result.append(user_data)   

   return jsonify({'Participantes': result})

if __name__ == "__main__":
    app.run(debug=True)