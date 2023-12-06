# Package Customization

If you want to generate the icons yourself, update them, and/or add more icons, you should fork the git repo and use that fork in your pubspec.yaml file. Then run the generate.py file in the `_generator` directory

Also remember to make a Python virtual env that has the requirement packages from requirements.txt, FontForge is installed, and oslllo-svg-fixer is present to convert the stokes to paths (optional but useful for simplifying the SVGs too complex for FontForge).

If you want to add icons to the pack, place them in `_generator/additional_icons`

### Note:

Some icons from the upstream Iconoir pack fail to convert or throw off the font even after enrichment with the svg-fixer because they are sometimes a little too complex and incompatible with FontForge due to the SVG syntax so they have been replaced with fixed versions. Making them bold with thicker stroke-width was also a challenge so there is a bold_override directory to deal with that before FontForge tries to read the SVG files.

Don't delete the fixed ones from `_generator/additional_icons` unless you know what you're doing :)