# Flutter Iconoir TTF

## Intro:
The free open source Iconoir icons for Flutter without dependency on `flutter_svg` because they use a standard font file.

That means you can just use the Icon widget and be on your way. ✨

There are well over a thousand nice icons to choose from!

(even more if you include the additional **bold** variant!)

This would not be possible without the Iconoir Project Community and their efforts. 💙

## Rationale:
Using a font is more lightweight on resources than parsing and rendering SVGs because the vector graphics in fonts are precompiled. Since the icons are monochrome glyphs, this works out pretty well.

## Usage:

**Add the following to your imports**:

`import 'package:flutter_iconoir_ttf/flutter_iconoir_ttf.dart';`

After importing, you can utilize an Icon widget, with `IconData` sourced from either the `IconoirIcons` or `IconoirIconsBold` class.

**Examples**:

`Icon(IconoirIcons.bluetooth, color: Color(0xFF0000FF))`

`Icon(IconoirIconsBold.bluetooth, color: Color(0xFF0000FF))`

## Package Customization

See the customization document in the git repo:
[customization.md](https://github.com/aakhil-kassim/flutter_iconoir_ttf/blob/main/extra/customization.md)


## Example Picture

<img src="https://github.com/aakhil-kassim/flutter_iconoir_ttf/raw/main/extra/example.png" alt="Example main.dart screen" />