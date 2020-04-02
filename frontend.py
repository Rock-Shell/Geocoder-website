import os
from flask import Flask,render_template,request
from werkzeug import secure_filename
import pandas
from geopy.geocoders import Nominatim
geolocator=Nominatim(user_agent="geocoder")
def find(name,path=r'D:\udemy\App10_GeoCoderWebService'):
    for root,dirs,files in os.walk(path,topdown=True):
        if name in files:
            return (os.path.join(root,name),root)

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")
@app.route('/success-table',methods=["POST","GET"])
def success():
    dict={}
    if request.method=="POST":
        #s=request.get_json(silent=True)
        file=request.files['myfile']
        filename=secure_filename(file.filename)#return str(filename)

        #file.save(os.path.join("wherever","you","want",filename))
        y=find(filename)
        x=y[0]

        a=pandas.read_csv(x)

        id=list(a.ID)
        id.insert(0,"ID")
        dict['ID']=id[1:]

        add=list(a.Address)
        add.insert(0,"ADDRESS")
        dict["Address"]=add[1:]

        name=list(a.Name)
        name.insert(0,"NAME")
        dict['Name']=name[1:]

        emp=list(a.Employees)
        emp.insert(0,"EMPLOYEES")
        dict['Employ']=emp[1:]

        n=len(id)
        lon=["LONGITUDE"]
        lat=["LATITUDE"]

        for i in range(1,n):
            location=geolocator.geocode(add[i])
            lon.append(location.longitude)
            lat.append(location.latitude)
        dict['Lon']=lon[1:]
        dict['Lat']=lat[1:]
        #df=pandas.DataFrame(dict)
        #a=y[1]+r'\file.csv'
        #df.to_csv(a)
        return render_template("success.html",id=id,add=add,name=name,emp=emp,n=n,lon=lon,lat=lat)

#@app.route('/download')
#def download():
#    None
if __name__=="__main__":
    app.run(debug=True)
