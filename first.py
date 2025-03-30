from flask import Flask, render_template, request, send_file
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

def add_centered_multiline_text(image_path, text, output_path, text_color=(0, 0, 0), max_font_size=70, position_offset=(0, 0), font_path=None):
    """
    Adds centered, multi-line text to an image. Automatically adjusts font size for best fit.

    Args:
        image_path (str): Path to the input image.
        text (str): The multi-line text to add (each line separated by '\n').
        output_path (str): Path to save the modified image.
        text_color (tuple): RGB color of the text (default is black).
        max_font_size (int): Maximum font size to use (the function will try to find the largest possible font size that fits).
        position_offset (tuple): A tuple (x, y) that offsets the center position.  This allows you to fine-tune the vertical placement of the text.
        font_path (str, optional): Path to a custom font file (e.g., .ttf). If None, a default font is used.
    """
    try:
        img = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        image_width, image_height = img.size

        print(image_width, image_height)

        # Choose a font
        if font_path:
            try:
                font = ImageFont.truetype(font_path, max_font_size)
            except IOError:
                print(f"Error: Could not load font at {font_path}. Using default font.")
                font = ImageFont.truetype("arial.ttf", max_font_size)
        else:
            try:
                font = ImageFont.truetype("Arial.ttf", max_font_size)  # Try Arial first
            except IOError:
                font = ImageFont.load_default()

        # Calculate the bounding box of the entire text block
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate the center position
        x = (image_width - text_width) / 2 + position_offset[0]
        y = (image_height - text_height) / 2 + position_offset[1]

        print(image_width, image_height, text_width, text_height, max_font_size)
        # Add the text
        draw.multiline_text((x, y- 100), text, fill=text_color, font=font, align="center")

        img.save(output_path)
        print(f"Text added to image and saved to {output_path}")
        return img

    except FileNotFoundError: 
        print(f"Error: Image not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/', methods=['GET', 'POST'])
def hello_world():
  if request.method == 'POST':
    day = request.form['day']
    text1 = request.form['text1']
    text2 = request.form['text2']
    text3 = request.form['text3']
    if os.path.exists("output.png"):
      os.remove("output.png")
    image_path = "test.jpeg"  # Replace with your image path
    text = """St. John Paul Mission Center
      Periyanaiken palayam
      SMYM
      Year of Bible 
      & 
      Evangelization"""
    text += "\n" + day
    if text1:
      text += "\n" + text1
    if text2:
      text += "\n" + text2
    if text3:
      text += "\n" + text3

    output_path = "output.png" 
    text_color = (233, 30, 99)  # White
    max_font_size = 30  # Adjust this to control the maximum font size.  The script will try to use the largest size that fits.
    position_offset = (0, 0)  # Adjust this to fine-tune the vertical position.  Positive values move the text down.
    font_path = "WinkySans-VariableFont_wght.ttf"  # Or "path/to/your/font.ttf"

    img = add_centered_multiline_text(image_path, text, output_path, text_color, max_font_size, position_offset, font_path)
    if img:
      # Save the image to a BytesIO object (in-memory)
      img_io = BytesIO()
      img.save(img_io, 'PNG')  # Save as PNG for best quality and transparency
      img_io.seek(0)

      # Send the file as a download
      return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='output.png')
    else:
        return "Error processing image."
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)