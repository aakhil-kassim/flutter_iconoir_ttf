import fontforge
import os
import sys

def create_glyph_from_svg(font, svg_file, unicode_value):
  try:
    print(f'processing {svg_file}')
    glyph = font.createChar(unicode_value)
    glyph.importOutlines(svg_file)
    glyph.left_side_bearing = glyph.right_side_bearing = 15
  except Exception as e:
    print(f"Error processing {svg_file}: {e}")

def main(icons_dir, output_ttf):
  font = fontforge.font()
  font.familyname = "IconoirIcons"
  font.fontname = "IconoirIcons"
  font.fullname = "Iconoir Icons"

  unicode_start = 0xe900
  for index, file in enumerate(sorted(os.listdir(icons_dir))):
    if file.endswith('.svg'):
      svg_file_path = os.path.join(icons_dir, file)
      unicode_value = unicode_start + index
      create_glyph_from_svg(font, svg_file_path, unicode_value)

  font.generate(output_ttf)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("Usage: fontforge -script this_script.py [icons directory] [output .ttf file]")
    sys.exit(1)

  icons_directory = sys.argv[1]
  output_font = sys.argv[2]
  main(icons_directory, output_font)
