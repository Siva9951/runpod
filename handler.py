import json
import base64
import torch
from diffusers import DiffusionPipeline
from PIL import Image
import io


# Load the model (once)
pipe = DiffusionPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
).to("cuda")  # Use "cpu" if you don't have a GPU

def handler(event, context=None):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)

        prompt = body.get("prompt")
        if not prompt:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'prompt' in request body."})
            }

        # Generate image
        image = pipe(prompt).images[0]

        # Convert to base64
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"image_base64": img_str})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }











