#!/usr/bin/env bash

# Ensure you are in the _generator dir
cd "$(dirname "${0}")"

# Check dependencies
which git > /dev/null || { echo "Missing git... exiting."; exit 1; }
os_name=$(uname -s)
##### No longer using fontforge
# fontforge_binary='fontforge'

# if [ "$os_name" = "Darwin" ]; then
#   fontforge_binary='/Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge'
# elif [ "$os_name" = "Linux" ]; then
#   fontforge_binary='fontforge'
# else
#   echo "Unsupported operating system: $os_name"
#   exit 1
# fi

# which "$fontforge_binary" > /dev/null || { echo "Missing fontforge... exiting."; exit 1; }
#####
npx svgtofont --version > /dev/null || { echo "Missing svgtofont... exiting."; exit 1; }
npx oslllo-svg-fixer --version > /dev/null || { echo "Missing oslllo-svg-fixer... exiting."; exit 1; }

# Extract repo
icons_repo_url='https://github.com/iconoir-icons/iconoir'
clone_temp_dir='iconoir_icons_temp'
repo_subdir_with_icons='icons/regular'
all_icons_dir='all_icons'

echo "Cloning Icons repository..."
mkdir -p "$all_icons_dir"
rm $all_icons_dir/*.svg
rm -rf "$clone_temp_dir"
git clone "$icons_repo_url" "$clone_temp_dir"
cp -r "${clone_temp_dir}/${repo_subdir_with_icons}/." "$all_icons_dir"
rm -rf "$clone_temp_dir"

# Copy additional icons
additional_icons_dir='additional_icons'
cp "$additional_icons_dir"/*.svg "$all_icons_dir/"

# Enrich Icons
enriched_icons_dir='enriched'
mkdir -p "$enriched_icons_dir"

echo -e "\nThe following must be done at least once (and it takes a long time for the first time)!"
read -p "Would you like to start icon enrichment for REGULAR icons (convert SVG path to fills)? [y/n] " yn
case $yn in
  [Yy]* )
    echo "Enriching icons..."
    for svg in $all_icons_dir/*.svg; do
      base_svg=$(basename "$svg")
      if [ ! -f "$enriched_icons_dir/$base_svg" ]; then
        npx oslllo-svg-fixer -s "$svg" -d "$enriched_icons_dir/"
      fi
    done
    ;;
  [Nn]* )
    echo "Skipping icon enrichment."
    ;;
  * )
    echo "Please answer yes or no."
    ;;
esac
# Make bold versions of the icons
enriched_icons_bold_dir='enriched_bold'
temp_enriched_bold_dir='temp_enriched_bold'
mkdir -p "$enriched_icons_bold_dir"
mkdir -p "$temp_enriched_bold_dir"
stroke_pattern='stroke-width="([0-9]+(\.[0-9]+)?)"'

echo "Making bold SVGs..."
for svg in $all_icons_dir/*.svg; do
  base_svg=$(basename "$svg")
  if [ ! -f "$enriched_icons_bold_dir/$base_svg" ]; then
    sed -E "s/${stroke_pattern}/stroke-width=\"2.0\"/g" "$svg" > "$temp_enriched_bold_dir/$base_svg"
  fi
done

# Enrich Bold Icons
echo -e "\nThe following must be done at least once (and it takes a long time for the first time)!"
read -p "Would you like to start icon enrichment for BOLD icons? [y/n] " yn
case $yn in
  [Yy]* )
    echo "Enriching bold icons..."
    for svg in $temp_enriched_bold_dir/*.svg; do
      if [ ! -n "$(find "$temp_enriched_bold_dir" -maxdepth 1 -type f)" ]; then
        echo "No new icons to enrich, leaving loop."
        break
      fi
      base_svg=$(basename "$svg")
      if [ ! -f "$enriched_icons_bold_dir/$base_svg" ]; then
        npx oslllo-svg-fixer -s "$svg" -d "$enriched_icons_bold_dir/"
      fi
    done
    ;;
  [Nn]* )
    echo "Skipping bold icon enrichment."
    ;;
  * )
    echo "Please answer yes or no."
    ;;
esac

# Clean up temporary directory
rm -rf "$temp_enriched_bold_dir"


# Quality control
echo "Generating quality control HTML files"
./quality_control.sh $enriched_icons_dir regular
./quality_control.sh $enriched_icons_bold_dir bold


# Create TTFs
temp_fonts_dir="temp_fonts"
mkdir -p $temp_fonts_dir
fonts_dir="../fonts"
font_name="iconoir_icons"
#####
# echo "Generating TTF files with FontForge"
# "$fontforge_binary" -script create_ttf.py "$enriched_icons_dir" "$fonts_dir/${font_name}_regular.ttf" false
# "$fontforge_binary" -script create_ttf.py "$enriched_icons_bold_dir" "$fonts_dir/${font_name}_bold.ttf" true
#####
npx svgtofont -s $enriched_icons_dir -o $temp_fonts_dir -f IconoirIconsRegular
cp $temp_fonts_dir/IconoirIconsRegular.ttf ../fonts/
rm -rf $temp_fonts_dir
mkdir -p $temp_fonts_dir
npx svgtofont -s $enriched_icons_bold_dir -o $temp_fonts_dir -f IconoirIconsBold
cp $temp_fonts_dir/IconoirIconsBold.ttf ../fonts/
rm -rf $temp_fonts_dir

# Generate Dart Class for Flutter
output_dart_file="../lib/flutter_iconoir_ttf.dart"
unicode_start=0xEA01

generate_dart_class() {
  echo "Generating Dart class..."
  {
    echo '/// Flutter Iconoir Icon Pack - TrueType Font Version.'
    echo 'library flutter_iconoir_ttf;'
    echo ''
    echo 'import "package:flutter/widgets.dart";'
    echo ''
    echo '/// An icon data class for regular stroke-width Iconoir icons.'
    echo 'class IconoirIconData extends IconData {'
    echo '  /// Creates an icon data for Iconoir icons regular stroke-width set.'
    echo '  const IconoirIconData(int codePoint) : super(codePoint, fontFamily: "IconoirIconsRegular", fontPackage: "flutter_iconoir_ttf");'
    echo '}'
    echo '/// A collection of Flutter icons from the Iconoir regular stroke-width set.'
    echo 'class IconoirIcons {'

    local index=0
    for file in "$all_icons_dir"/*.svg; do
      local icon_name
      icon_name=$(basename "$file" .svg)
      local camel_case_name
      camel_case_name=$(echo "$icon_name" | awk -F'-' '{ printf "%s", $1; for(i=2; i<=NF; i++) printf toupper(substr($i,1,1)) substr($i,2); }')
      local unicode
      unicode=$((unicode_start + index))
      echo "  /// Iconoir icon for '$icon_name'."
      echo "  static const IconData $camel_case_name = IconoirIconData(0x$(printf '%x' "$unicode"));"
      ((index++))
    done

    echo '}'
    echo ''
    echo '/// An icon data class for bold stroke-width Iconoir icons.'
    echo 'class IconoirIconDataBold extends IconData {'
    echo '  /// Creates an icon data for Iconoir icons bold stroke-width set.'
    echo '  const IconoirIconDataBold(int codePoint) : super(codePoint, fontFamily: "IconoirIconsBold", fontPackage: "flutter_iconoir_ttf");'
    echo '}'
    echo ''
    echo '/// A collection of Flutter icons from the Iconoir bold stroke-width set.'
    echo 'class IconoirIconsBold {'

    index=0
    for file in "$all_icons_dir"/*.svg; do
      local icon_name
      icon_name=$(basename "$file" .svg)
      local camel_case_name
      camel_case_name=$(echo "$icon_name" | awk -F'-' '{ printf "%s", $1; for(i=2; i<=NF; i++) printf toupper(substr($i,1,1)) substr($i,2); }')
      local unicode
      unicode=$((unicode_start + index))
      echo "  /// Iconoir icon for '$icon_name' in bold stroke-width."
      echo "  static const IconData $camel_case_name = IconoirIconDataBold(0x$(printf '%x' "$unicode"));"
      ((index++))
    done

    echo '}'
  } > "$output_dart_file"
}

generate_dart_class

dart format -o write "$output_dart_file"