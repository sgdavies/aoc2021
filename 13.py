#!/usr/bin/python
with open("13.dat", "r") as f:
    lines = f.readlines()

dots = set()
folds = []

while (line := lines.pop()) != "\n":
    plane, val = line.strip().split(" ")[2].split("=")
    folds = [(plane, int(val))] + folds

for line in lines:
    x,y = line.strip().split(",")
    dots.add((int(x),int(y)))

first = True
for fold in folds:
    if fold[0] == "x":
        x = fold[1]
        folded = set(filter(lambda dot: dot[0] > x, dots))
        dots -= folded
        folded = set(map(lambda dot: (2*x - dot[0], dot[1]), folded))
        dots.update(folded)
    elif fold[0] == "y":
        y = fold[1]
        folded = set(filter(lambda dot: dot[1] > y, dots))
        dots -= folded
        folded = set(map(lambda dot: (dot[0], 2*y - dot[1]), folded))
        dots.update(folded)
    else:
        print("Bad val", fold[0], fold[1])
        exit()

    if first:
        print(len(dots))
        first = False

try:
    from PIL import Image
    import pytesseract
    # A few hacks needed to help OCR:
    # - scale up
    # - ensure there's a top and left border
    # - smooth pixel-pixel boundaries on diagonal lines:
    #      ***       ***
    #      ***  =>  ****
    #   ***       ****
    #   ***       ***
    scale = 5
    sizex = scale*(x+2) # x,y still at max values from folding process above; +2 for borders
    sizey = scale*(y+2)
    black = (0,0,0)
    white = (255,255,255)
    img = Image.new('RGB', (sizex, sizey), white)
    pixels = img.load()
    for (x,y) in dots:
        for dx in range(scale):
            for dy in range(scale):
                pixels[scale*(x+1) + dx, scale*(y+1) +dy] = black  # +1 leaving space for top/left border
    # smooth diagonals
    for x in range(sizex-1):
        for y in range(sizey-1):
            if pixels[x,y] == white and pixels[x+1,y] == black and pixels[x,y+1] == black and pixels[x+1,y+1] == white:
                # corner rising right
                pixels[x,y] = black
                pixels[x+1,y+1] = black
            elif pixels[x,y] == black and pixels[x+1,y] == white and pixels[x,y+1] == white and pixels[x+1,y+1] == black:
                # corner sinking right
                pixels[x+1,y] = black
                pixels[x,y+1] = black
    #print(pytesseract.image_to_string(img))
    # should be able to go direct from image as above, but the format must be wrong - go via file instead to work around this
    img.save("13.bmp", "BMP")
    print(pytesseract.image_to_string("13.bmp"))
    
except ModuleNotFoundError as mnfe:
    img = [ ["."]*(x+1) for _ in range(y+1) ]
    for dot in dots:
        img[dot[1]][dot[0]] = '#'

    print("\n".join(["".join(row) for row in img]))
    print("\nPlease install PIL.Image and pytesseract to print the answer directly!")
