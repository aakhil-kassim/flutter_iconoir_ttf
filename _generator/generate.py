#!/usr/bin/env python3

import os
import platform
import shutil
import git
import subprocess

# Configuration
icons_repo_url = 'https://github.com/iconoir-icons/iconoir'
clone_temp_dir = 'iconoir_icons_temp'
repo_subdir_with_icons = 'icons/regular'
additional_icons_dir = 'additional_icons'
icons_dir = 'all_icons'
output_ttf_file = '../fonts/iconoir_icons.ttf'
output_dart_file = '../lib/iconoir_icons.dart'
unicode_start = 0xe900

# Cleanup previous build
def cleanup_previous_build():
  if os.path.isdir(icons_dir):
    shutil.rmtree(icons_dir)
  if os.path.isfile(output_ttf_file):
    os.remove(output_ttf_file)
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
  shutil.rmtree(clone_temp_dir)

# Copy additional SVG files from 'additional_icons' to 'all_icons'
def copy_additional_icons():
  print("Copying additional icons...")
  if not os.path.exists(additional_icons_dir):
    print("No additional icons directory found.")
    return

  for file in os.listdir(additional_icons_dir):
    if file.endswith('.svg'):
      src_path = os.path.join(additional_icons_dir, file)
      dest_path = os.path.join(icons_dir, file)
      shutil.copy2(src_path, dest_path)

# Create TTF file using FontForge
def create_ttf():
  print("Creating TTF file...")
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
  subprocess.call([fontforge_command, '-script', 'create_ttf.py', icons_dir, output_ttf_file])


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

if __name__ == "__main__":
  cleanup_previous_build()
  clone_iconoir_icons()
  copy_additional_icons()
  create_ttf()
  generate_dart_class()
  print("Process completed successfully.")