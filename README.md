# Flutter Iconoir TTF


## Intro:
The free open source Iconoir icons for Flutter without dependency on flutter_svg like the regular Iconoir package has.

You can just use the Icon widget and be on your way. ✨

There are well over a thousand nice icons to choose from!

It works as a regular TTF font file that can be generated with a FontForge script from the original SVGs and uses Python script to generate the corresponding Dart code.

You don't need Python or FontForge to use this package. That is only to customize it.

## Usage:

**Add the following to your imports**:

`import 'package:flutter_iconoir_ttf/iconoir_icons.dart';`

...then you can use an `Icon` widget where the expected IconData is coming from the `IconoirIcons` or `IconoirIconsBold` class.

**Example**:

`Icon(IconoirIcons.bluetooth, color: Color(0xFF0000FF))`


`Icon(IconoirIconsBold.bluetooth, color: Color(0xFF0000FF))`

## Package Customization

See the customization document in the git repo:
[docs/customization.md](https://github.com/aakhil-kassim/flutter_iconoir_ttf/docs/customization.md)

