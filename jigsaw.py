from PIL import Image
import argparse
import os


def make_pieces(src_filename, cut_filename):
    filename = os.path.splitext(os.path.basename(src_filename))[0]
    src_image = Image.open(src_filename).convert('RGB')
    cut_image = Image.open(cut_filename).convert('RGB')

    width, height = cut_image.size
    threshold = width * height * 0.01
    colors = [rgb for c, rgb in cut_image.getcolors()
              if c >= threshold and rgb != (255, 255, 255) and rgb != (0, 0, 0)]

    colors_dict = \
        dict((val[0], {
            'img': Image.new('RGBA', (width, height), (0, 0, 0, 0)),
            'min_x': width,
            'min_y': height,
            'max_x': 0,
            'max_y': 0,
        }) for val in colors)

    src_pix = src_image.load()
    cut_pix = cut_image.load()

    for x in xrange(width):
        for y in xrange(height):
            c = cut_pix[x, y]
            if c in colors:
                d = colors_dict[c[0]]
                d['img'].putpixel((x, y), src_pix[x, y])
                d['min_x'] = min(d['min_x'], x)
                d['min_y'] = min(d['min_y'], y)
                d['max_x'] = max(d['max_x'], x)
                d['max_y'] = max(d['max_y'], y)

    for c, d in colors_dict.iteritems():
        img = d['img'].crop((d['min_x'], d['min_y'], d['max_x'], d['max_y']))
        img.save('%s-%02d.png' % (filename, c))


def main():
    parser = argparse.ArgumentParser(
        description='Cut an image into jigsaw pieces by color cells')
    parser.add_argument('src', help='filename for source image')
    parser.add_argument('cut', help='filename for cut image')

    args = parser.parse_args()
    make_pieces(args.src, args.cut)

if __name__ == "__main__":
    main()
