from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
from PIL import Image
app = Flask(__name__)
 
upload_folder = os.path.join('static', 'uploads')
predict_folder = os.path.join('static', 'predicted')
app.config['UPLOAD'] = upload_folder
app.config['PREDICT']=predict_folder




# @app.route('/base')
# def base():
#     return render_template('base.html')
# @app.route('/about')
# def about():
#     return render_template('about.html')   
# @app.route('/service')



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        imgs = os.path.join(app.config['UPLOAD'], filename)
        calories=detection(imgs,filename)
        predict=os.path.join(app.config['PREDICT'], filename)
        content=''
        print(filename)
        return render_template('index.html', img=predict)
    return render_template('index.html')
 
def cal_calories(results):
    result=results[0]
    classes=model.names
    #kcal
    calorie_dict = { 'Bhatura':204, 'BhindiMasala':200,   'Biryani':350 , 'Chole':290 , 'ShahiPaneer': 280, 'chicken':335 , 'dal':198 ,'dhokla':152, 'gulab_jamun':175,'idli':58,'jalebi':150,'modak':126,'palak_paneer':374,'poha':273,'rice':206 ,'roti':120,'samosa':217}
    #print(result)
    calories=0
    for r in results:
        for i in (r.boxes.cls):
            print(classes[int(i)])
            calories+=calorie_dict[classes[int(i)]]
            print(calories)
    return calories

def detection(image_path,filename):
    model = YOLO('D:/sem 7/Majorproject/models/best (1).pt')
    results= model.predict(image_path)
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    #im.show()  # show image
    im.save(predict_folder+'/' +filename)    
    result=results[0]
    classes=model.names
    #kcal
    calorie_dict = { 'Bhatura':204, 'BhindiMasala':200,   'Biryani':350 , 'Chole':290 , 'ShahiPaneer': 280, 'chicken':335 , 'dal':198 ,'dhokla':152, 'gulab_jamun':175,'idli':58,'jalebi':150,'modak':126,'palak_paneer':374,'poha':273,'rice':206 ,'roti':120,'samosa':217}
    #print(result)
    calories=0
    for r in results:
        for i in (r.boxes.cls):
            print(classes[int(i)])
            calories+=calorie_dict[classes[int(i)]]
            print(calories)
    return calories
    
 
if __name__ == '__main__':
    app.run(debug=True, port=8001)