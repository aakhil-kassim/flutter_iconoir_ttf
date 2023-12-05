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

def main(icons_dir, output_ttf, is_bold=False):
  font = fontforge.font()
  font.familyname = "IconoirIcons"
  font.fontname = "IconoirIcons" + ("Bold" if is_bold else "")
  font.fullname = "Iconoir Icons" + (" Bold" if is_bold else "")

  # Set bold attribute if necessary
  if is_bold:
    font.weight = "Bold"

  unicode_start = 0xe900
  for index, file in enumerate(sorted(os.listdir(icons_dir))):
    if file.endswith('.svg'):
      svg_file_path = os.path.join(icons_dir, file)
      unicode_value = unicode_start + index
      create_glyph_from_svg(font, svg_file_path, unicode_value)

  font.generate(output_ttf)

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print("Usage: fontforge -script this_script.py [icons directory] [output .ttf file] [is_bold]")
    sys.exit(1)

  icons_directory = sys.argv[1]
  output_font = sys.argv[2]
  is_bold = sys.argv[3].lower() == 'true'
  main(icons_directory, output_font, is_bold)
