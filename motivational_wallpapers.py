from PIL import Image, ImageDraw, ImageFont
import random
import os
import json

def create_wallpaper(quote, author, output_path="wallpaper.png", size=(1920, 1080), text_color=(255, 255, 255), hpad=40, vpad=40):
    # Generate a random dark gradient background
    img = generate_dark_gradient_background(size)
    
    # Create a drawing context
    draw = ImageDraw.Draw(img)
    
    # Choose a motivational font and larger size
    try:
        font_quote = ImageFont.truetype("fonts/RobotoCondensed-VariableFont_wght.ttf", 100)  # Adjust the font size
        font_author = ImageFont.truetype("fonts/RobotoCondensed-Italic-VariableFont_wght.ttf", 50)  # Adjust the font size
    except IOError:
        print("Font not found, falling back to default font.")
        font_quote = ImageFont.load_default()  # If the font is not found, fall back to default
        font_author = ImageFont.load_default()  # If the font is not found, fall back to default

    # Text wrapping
    quote_lines = wrap_text(quote, font_quote, size[0] - hpad)

    # Calculate the vertical position to center the quote text
    total_height = sum(font_quote.getbbox(line)[3] - font_quote.getbbox(line)[1] for line in quote_lines) + vpad * len(quote_lines)
    y_position = (size[1] - total_height) // 2

    # Draw each line of the quote on the image
    for line in quote_lines:
        bbox = font_quote.getbbox(line)  # getbbox returns (left, top, right, bottom)
        width = bbox[2] - bbox[0]  # Width is the difference between right and left
        x_position = (size[0] - width) // 2  # Center the quote horizontally
        draw.text((x_position, y_position), line, font=font_quote, fill=text_color)
        y_position += bbox[3] - bbox[1] + vpad # Move down based on the height of the text

    # Add the author text below the quote, aligned to the right
    author_bbox = font_author.getbbox(author)
    author_width = author_bbox[2] - author_bbox[0]  # Width of the author text
    author_x_position = 0.8 * (size[0] - author_width - hpad)  # Right-align with some padding
    author_y_position = y_position + 100  # Leave some space below the quote
    draw.text((author_x_position, author_y_position), author, font=font_author, fill=text_color)    

    # Save the wallpaper to the specified path
    img.save(output_path)


def wrap_text(text, font, max_width):
    """Wrap text to fit within the given width."""
    lines = []
    words = text.split()
    line = ""
    
    for word in words:
        # Try adding the word to the current line
        test_line = f"{line} {word}".strip()
        bbox = font.getbbox(test_line)  # getbbox returns (left, top, right, bottom)
        width = bbox[2] - bbox[0]  # Width is the difference between right and left

        # If it fits, add the word to the line
        if width <= 0.8*max_width and word != '||':
            line = test_line
        else:
            # Otherwise, start a new line
            if word == '||':
                word = ''
            lines.append(line)
            line = word
    
    # Add the last line
    if line:
        lines.append(line)
    
    return lines


def get_random_quote(file_path):
    """Read quotes from the file and return a random one."""
    with open(file_path, 'r') as file:
        quotes = json.load(file)
    return random.choice(quotes)


def generate_dark_gradient_background(size, color1=None, color2=None):
    """Generate a dark gradient background with fading colors."""
    # Use random dark colors if not provided
    if not color1:
        color1 = tuple(random.randint(0, 60) for _ in range(3))  # Dark color
    if not color2:
        color2 = tuple(random.randint(0, 60) for _ in range(3))  # Dark color
    
    # Create an image
    img = Image.new("RGB", size)
    width, height = size
    
    # Gradient generation: fade from color1 to color2
    for y in range(height):
        # Interpolate between color1 and color2
        r = int(color1[0] * (1 - y / height) + color2[0] * (y / height))
        g = int(color1[1] * (1 - y / height) + color2[1] * (y / height))
        b = int(color1[2] * (1 - y / height) + color2[2] * (y / height))
        
        for x in range(width):
            img.putpixel((x, y), (r, g, b))

    return img


def main():
    # Path to the quotes text file:
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to your target file relative to the script's directory
    file_path = os.path.join(script_dir, 'quotes.json')

    # Get a random quote
    random_quote = get_random_quote(file_path)

    quote = random_quote["quote"]
    try:
        author = "~ " + random_quote["author"]
    except KeyError:
        author = ""

    # Path to save the wallpaper
    output_path = "wallpaper.png"

    # Create the wallpaper
    create_wallpaper(quote, author, output_path)

    print(f"Wallpaper created with quote: {quote}")

if __name__ == "__main__":
    main()
