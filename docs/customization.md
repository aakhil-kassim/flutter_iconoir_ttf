# Package Customization

If you want to generate the icons yourself, update them, and/or add more icons, you should fork the git repo and use that fork in your pubspec.yaml file. Then run the `build.sh` bash script file in the `_generator` directory

Remember to have bash, coreutils, oslllo-svg-fixer, and svgtofont. (FontForge has been replaced with svgtofont by the way.)

If you want to add icons to the pack, place SVG files in `_generator/additional_icons`
