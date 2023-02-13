import os
import openai
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        prompt = """The following conversation is between a tech entrepreneur and a community moderator at FrameWrk.
    The moderator is helpful, creative, clever and very friendly. Entrepreneur: {0}, Answer: """.format(prompt)
        response = generate_response(prompt)
        return redirect(url_for("index", result=response))
        
    result = request.args.get("result")
    return render_template("chatroom.html", result=result)

if __name__ == "__main__":
    
    app.run(host='0.0.0.0', debug=False)