#!/usr/bin/env python3

import os
import re
import platform
import shutil
import git
import subprocess

# Configuration
icons_repo_url = 'https://github.com/iconoir-icons/iconoir'
clone_temp_dir = 'iconoir_icons_temp'
repo_subdir_with_icons = 'icons/regular'
additional_icons_dir = 'additional_icons'
bold_override_icons_dir = 'bold_override'
icons_dir = 'all_icons'
bold_icons_dir = 'all_icons_bold'
output_ttf_file = '../fonts/iconoir_icons_regular.ttf'
bold_output_ttf_file = '../fonts/iconoir_icons_bold.ttf'
output_dart_file = '../lib/iconoir_icons.dart'
unicode_start = 0xe900

# Cleanup previous build
def cleanup_previous_build():
  if os.path.isdir(icons_dir):
    shutil.rmtree(icons_dir)
  if os.path.isdir(bold_icons_dir):
    shutil.rmtree(bold_icons_dir)
  if os.path.isfile(output_ttf_file):
    os.remove(output_ttf_file)
  if os.path.isfile(bold_output_ttf_file):
    os.remove(bold_output_ttf_file)
  if os.path.isfile(output_dart_file):
    os.remove(output_dart_file)

# Clone the Iconoir Icons Repository
def clone_iconoir_icons():
  print("Cloning Icons repository...")
  if os.path.exists(clone_temp_dir):
    shutil.rmtree(clone_temp_dir)
  repo = git.Repo.clone_from(icons_repo_url, clone_temp_dir)
  icons_src = os.path.join(clone_temp_dir, repo_subdir_with_icons)
  if not os.path.exists(icons_dir):
    os.makedirs(icons_dir)
  shutil.copytree(icons_src, icons_dir, dirs_exist_ok=True)
  if not os.path.exists(bold_icons_dir):
    os.makedirs(bold_icons_dir)
  shutil.copytree(icons_src, bold_icons_dir, dirs_exist_ok=True)
  shutil.rmtree(clone_temp_dir)

# Copy additional SVG files from 'additional_icons' to 'all_icons' and 'all_icons_bold'
def copy_additional_icons():
  print("Copying additional icons...")
  if not os.path.exists(additional_icons_dir):
    print("No additional icons directory found.")
    return

  for file in os.listdir(additional_icons_dir):
    if file.endswith('.svg'):
      src_path = os.path.join(additional_icons_dir, file)
      dest_path = os.path.join(icons_dir, file)
      bold_dest_path = os.path.join(bold_icons_dir, file)
      shutil.copy2(src_path, dest_path)
      shutil.copy2(src_path, bold_dest_path)

def copy_bold_overrides():
  print("Copying bold override icons...")
  if not os.path.exists(bold_override_icons_dir):
    print("No bold_override_icons_dir found.")
    return

  for file in os.listdir(bold_override_icons_dir):
    if file.endswith('.svg'):
      src_path = os.path.join(bold_override_icons_dir, file)
      bold_dest_path = os.path.join(bold_icons_dir, file)
      shutil.copy2(src_path, bold_dest_path)

# Modify SVGs in 'all_icons_bold' to have a bolder stroke-width
def make_bold_icons(bold_icons_dir):
  print("Making bold SVGs...")
  svg_file_pattern = re.compile(r'stroke-width="(\d+(\.\d+)?)')

  for root, dirs, files in os.walk(bold_icons_dir):
    for file in files:
      if file.endswith('.svg'):
        file_path = os.path.join(root, file)
        with open(file_path, 'r') as f:
          content = f.read()

        content = svg_file_pattern.sub(lambda m: f'stroke-width="{float(m.group(1)) * 1.33}', content)
        with open(file_path, 'w') as f:
          f.write(content)

def convert_path_to_fill_for_bold():
  for root, dirs, files in os.walk(bold_icons_dir):
    for file in files:
      if file.endswith('.svg'):
        subprocess.call(['oslllo-svg-fixer', '-s', bold_icons_dir+'/'+file, '-d', bold_icons_dir])

# Create TTF file using FontForge
def create_ttf(icons_directory, ttf_output_file, is_bold=False):
  print(f"Creating {'bold' if is_bold else 'regular'} TTF file from {icons_directory}...")
  # Determine the operating system
  os_name = platform.system()
  
  # Define the FontForge command based on the OS
  if os_name == "Darwin":  # macOS
    fontforge_command = '/Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge'
  elif os_name == "Linux":
    fontforge_command = 'fontforge'
  else:
    raise ValueError(f"Unsupported operating system: {os_name}")

  # Run the FontForge script
  subprocess.call([fontforge_command, '-script', 'create_ttf.py', icons_directory, ttf_output_file, str(is_bold)])

def to_camel_case(snake_str):
  components = snake_str.split('-')
  return components[0] + ''.join(x.title() for x in components[1:])

# Generate Dart Class for Flutter
def generate_dart_class():
  print("Generating Dart class...")
  mapping = []

  with open(output_dart_file, 'w') as f:
    f.write('library flutter_iconoir_ttf;\n\n')
    f.write('import "package:flutter/widgets.dart";\n\n')
    f.write('class IconoirIconData extends IconData {\n')
    f.write('  const IconoirIconData(int codePoint) : super(codePoint, fontFamily: "IconoirIcons", fontPackage: "flutter_iconoir_ttf");\n')
    f.write('}\n')
    f.write('class IconoirIcons {\n')

    for index, file in enumerate(sorted(os.listdir(icons_dir))):
      if file.endswith('.svg'):
        icon_name = os.path.splitext(file)[0]
        camel_case_name = to_camel_case(icon_name)
        unicode = f"{unicode_start + index:04x}"
        f.write(f'  static const IconData {camel_case_name} = IconoirIconData(0x{unicode});\n')
        mapping.append({icon_name: unicode})

    f.write('}\n')

    f.write('class IconoirIconDataBold extends IconData {\n')
    f.write('  const IconoirIconDataBold(int codePoint) : super(codePoint, fontFamily: "IconoirIconsBold", fontPackage: "flutter_iconoir_ttf");\n')
    f.write('}\n')

    f.write('class IconoirIconsBold {\n')

    for index, file in enumerate(sorted(os.listdir(icons_dir))):
      if file.endswith('.svg'):
        icon_name = os.path.splitext(file)[0]
        camel_case_name = to_camel_case(icon_name)
        unicode = f"{unicode_start + index:04x}"
        f.write(f'  static const IconData {camel_case_name} = IconoirIconDataBold(0x{unicode});\n')
        mapping.append({icon_name: unicode})

    f.write('}\n')

if __name__ == "__main__":
  cleanup_previous_build()
  clone_iconoir_icons()
  copy_additional_icons()
  make_bold_icons(bold_icons_dir)
  copy_bold_overrides()
  #convert_path_to_fill_for_bold()
  create_ttf(icons_dir, output_ttf_file)
  create_ttf(bold_icons_dir, bold_output_ttf_file, is_bold=True)
  generate_dart_class()
  print("Process completed successfully.")
