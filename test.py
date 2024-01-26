from openai import OpenAI


import json
import os
from distutils.log import debug 
from fileinput import filename 
from flask import *  
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


client = OpenAI(api_key="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")

items = {}

items["random chat"] = "randchat()"
items["asking nda"] = "asknda()"


@app.route('/')   
def main():   
    return render_template("index.html")   


bvb = ""
currfunc = ""

@app.route('/success', methods = ['POST'])   
def success():   

    global bvb
    global currfunc


    if currfunc=="":
        answersreceived = []
    
    if request.method == 'POST':   

        transcript = ""
        f = request.files['file'] 
        f.save("a.mp3")

       
       # f.save(f.filename)   

        audio_file = open("a.mp3", "rb")
        transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
        )

        bvb = transcript
        if currfunc=="":
            messages = [ {"role": "system", "content":  
                    "You are a real estate."} ]

            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a real estate agent"},
                {"role": "user", "content": "categories = [\"asking nda\",\"contract\",\"random chat\"] User: "+transcript+" Pick an item from categories array which is most likely the User is asking about Give exact one line only in this format: Item:\n"}
            ]
            )

            try:
                currfunc = items[completion.choices[0].message.content.split(":")[1].strip().lower()]
                print(currfunc)
        
                eval(items[completion.choices[0].message.content.split(":")[1].strip().lower()])
            except:
                currfunc = ""
        else:
            ff = ""
            eval(currfunc)

      
        
        
        return  bvb



def randchat():
    global bvb
    global currfunc
    print(bvb)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a assistant"},
        {"role": "user", "content": bvb+" give one sentence only."}
    ]
    )
    currfunc = ""
    bvb = completion.choices[0].message.content
    genaudio()


def genaudio():
    global bvb
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=bvb,
)

    response.stream_to_file("./static/a.mp3")



answersreceived = []

def asknda():
    global bvb
    global answersreceived


    print((len(answersreceived)))

  
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a assistant"},
        {"role": "user", "content": "Execute this PHP Code <?php $questions = ['What is your name','What is your age','Where do you live?']; $thequestion =$questions["+str(len
        (answersreceived))+"]; echo $thequestion;?> Give exact answer only  in this format output:\n"}
    ]
    )
    if len(answersreceived)>=3:
        currfunc = ""
        answersreceived = []

    print(completion.choices[0].message.content)
    answersreceived.append(bvb)
    
    if "Notice:" not in completion.choices[0].message.content:
        bvb = completion.choices[0].message.content

        if ":" in bvb:
            arr = bvb.split("\n")
            for str1 in arr:
                if ":" not in str1 and len(str1)>2:
                    bvb = str1
                    print(">>>>>>"+bvb)
                    break


        genaudio()



def ggg():
    print("asdawe sdfgsfg")

        #return render_template("Acknowledgement.html", name = f.filename)   




def revoicer():
        import requests

        cookies = {
        '_ga': 'GA1.1.413694345.1706058031',
        'ci_session': 'd95fc919c90ded630625be3896e8af1d7cc4f1a9',
        '_ga_WLEQM9ZEZN': 'GS1.1.1706058030.1.1.1706058447.0.0.0',
        }

        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://revoicer.app',
            'Referer': 'http://revoicer.app/speak',
            'Accept-Language': 'en-US,en;q=0.9',
            # 'Cookie': '_ga=GA1.1.413694345.1706058031; ci_session=d95fc919c90ded630625be3896e8af1d7cc4f1a9; _ga_WLEQM9ZEZN=GS1.1.1706058030.1.1.1706058447.0.0.0',
        }

        reply = completion.choices[0].message.content
        data = 'data=%7B%22languageSelected%22%3A%22en-US%22%2C%22voiceSelected%22%3A%22en-US-TonyNeural%22%2C%22toneSelected%22%3A%22Cheerful%22%2C%22text%22%3A%22%3Cp%3E'+reply+'%3F%3C%2Fp%3E**********Cheerful%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%22%2C%22simpletext%22%3A%22'+reply+'%3F%5Cn%22%7D'

        response = requests.post('http://revoicer.app/speak/preview_voice', cookies=cookies, headers=headers, data=data, verify=False)

if __name__ == '__main__':
     
    app.run(debug=True)