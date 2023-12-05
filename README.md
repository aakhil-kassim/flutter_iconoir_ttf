# Flutter Iconoir TTF


## Intro:
The free open source Iconoir icons for Flutter without dependency on flutter_svg like the regular Iconoir package has.

You can just use the Icon widget and be on your way. ✨

There are well over a thousand nice icons to choose from!

It works as a regular TTF font file that can be generated with a FontForge script from the original SVGs and uses Python script to generate the corresponding Dart code.

You don't need Python or FontForge to use this package. That is only to customize it.

## Usage:

Add:

`import 'package:flutter_iconoir_ttf/iconoir_icons.dart';`

and use an `Icon` widget where the expected IconData is coming from the `IconoirIcons` class.

Example:

`Icon(IconoirIcons.bluetooth, color: Color(0xFF0000FF), weight: 700)`

## Package Customization
If you want to generate the icons yourself, update them, and/or add more icons, you should fork the git repo and use that fork in your pubspec.yaml file. Then run the generate.py file in the `_generator` directory

Also remember to make a Python virtual env that has the requirement packages from requirements.txt, FontForge is installed, and oslllo-svg-fixer to convert the stokes to paths (optional but useful for simplifying the SVGs too complex for FontForge).

If you want to add icons to the pack, place them in `_generator/additional_icons`

### Note:

Some icons from the upstream Iconoir pack fail to convert or throw off the font because they are sometimes a little too complex and are incompatible with FontForge due to the complex SVG syntax so they have been replaced with fixed versions. Making them bold with thicker stroke-width was also a challenge so there is a bold_override directory to deal with that before FontForge tries to read the SVG files.

Don't delete the fixed ones from `_generator/additional_icons` unless you know what you're doing :)