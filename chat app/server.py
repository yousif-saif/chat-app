from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send
import json
import waitress

# install flask, flask_socketio, waitress by typing in the CMD
# pip install waitress
# pip install flask
# pip install flask_socketio


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config["SECRET_KEY"] = "dsklj93l493403lnfd-34mdw0k3j40r" # create a secret key to the app



def load_json():
    with open("./data.json", "r+") as f: 
        return json.load(f)


def write_json(data):
    with open("./data.json", "r+") as f:
        json.dump(data, f, indent=4)

def connect_socket():
    @socketio.on("message")
    def sendMessage(message):
        name = session["name"] # store the name of the user
        complet_message = name + ": " + message

        if message != "":
            with open("./data.json", "r+") as f:
                data = json.load(f)
                temp = data["messages"]
                temp.append(complet_message)
            
            write_json(data)

            send(complet_message, broadcast=True) # sending the message to all clients


# @app.route("/chat")
def send_message():

    connect_socket()
        
    with open("./data.json", "r+") as f:
        load = json.load(f)
        messages = load["messages"] # load the stored messages from the json file
    
    return render_template("message.html", messages = messages)


@app.route("/sign_in", methods=["POST"])
def sign_in():
    name = request.form["name"]
    email = request.form["email"]
    password = str(request.form["password"])
    
    correct = []
    all_correct = []

    if name == "" or email == "" or password == "":
        correct.append("False")

    with open("./data.json", "r+") as f:
        data = json.load(f)
        temp = data["accounts"]
        for i in temp: 
            for item, value in i.items(): # get all accounts
                if item == "name":
                    if value == name:
                        correct.append("True")
                    else:
                        correct.append("False")
                
                if item == "email":
                    if value == email:
                        correct.append("True")
                    else:
                        correct.append("False")
                

                if item == "password":
                    if value == password:
                        correct.append("True")
                    
                    else:
                        correct.append("False")
            
            all_correct.append(correct)
            correct = []
                        
        
    if ["True", "True", "True"] in all_correct: # if an account in the json file matching the enterd data
        correct = []
        all_correct = []
        # return redirect("/chat")
        session["name"] = name
        return send_message()

    else:
        correct = []
        all_correct = []
        return render_template("sign_in.html", error="Account not found")


@app.route("/")
def get_user_name():
    return render_template("sign_in.html")


@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


@app.route("/real_sign_up", methods=["POST"])
def real_sign_up():
    name = request.form["name2"]
    email = request.form["email2"]
    password = request.form["password2"]
    
    session["name"] = name

    with open("./data.json", "r+") as f:
        data = json.load(f)
        temp = data["accounts"]
        account = {"name":name, "email":email, "password":password}
        names = []
        for i in temp:
            names.append(i["name"])

        if name in names:
            return render_template("sign_up.html", error_msg="This name is alrady taken")
            
        else:
            temp.append(account)
    
    write_json(data)

    return send_message()

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error="Page not found")

@app.errorhandler(500)
def not_found(e):
    return render_template("error.html", error="Error from the server reload the page or restart the browser")


@app.errorhandler(429)
def not_found(e):
    return render_template("error.html", error="Too many messages")




if __name__ == "__main__":
    app.debug = True
    waitress.serve(app, host="you'r IP address", port = "80") # host the website on you'r computer (you can get the IP address form typing in the CMD 'ipconfig')
    # IMPORTANT: remember to change the IP address from the 'sign_in.html and sign_up.html'

    # go to chrome and type "you'r IP address:port number"
