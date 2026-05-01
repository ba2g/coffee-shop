from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
return " DevOps coffe shop'a Hoş geldiniz siparişiniz hazırlanır,yor."

if __nme__ =="__main__':
app.run(host="0.0.0.0'. port=5000)
