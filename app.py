from flask import Flask, request, render_template
from handler import handler
import json
import base64

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def generate_image():
    image_data = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        print(f"Prompt received: {prompt}")
        test_event = {
            "body": json.dumps({"prompt": prompt})
        }

        response = handler(test_event, context={})
        print("Handler Response:", response)

        if response.get("statusCode") == 200:
            try:
                image_base64 = json.loads(response["body"]).get("image_base64", "")
                if image_base64:
                    image_data = f"data:image/png;base64,{image_base64}"
                else:
                    print("No image_base64 found.")
            except Exception as e:
                print("Error decoding image:", str(e))
        else:
            print("Handler failed with status:", response.get("statusCode"))
            print("Error body:", response.get("body"))
    return render_template("index.html", image=image_data)


if __name__ == "__main__":
    app.run(debug=True)