#!/bin/bash

cd $(dirname ${0})

SVG_DIR="$1"
OUTPUT_HTML="quality_control_$2.html"

# Start of HTML and CSS for the grid layout
cat > $OUTPUT_HTML <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SVG Quality Control</title>
<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    padding: 10px;
  }
  .svg-container {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: center;
  }
  svg {
    max-width: 100%;
    height: auto;
  }
</style>
</head>
<body>
<div class="grid">
EOF


for svg_file in "$SVG_DIR"/*.svg; do
    filename=$(basename "$svg_file")

    # Add SVG content and filename to HTML
    echo "<div class='svg-container'>" >> $OUTPUT_HTML
    cat "$svg_file" >> $OUTPUT_HTML
    echo "<p>$filename</p>" >> $OUTPUT_HTML
    echo "</div>" >> $OUTPUT_HTML
done

# End of HTML file
cat >> $OUTPUT_HTML <<EOF
</div>
</body>
</html>
EOF

echo "HTML file created: $OUTPUT_HTML"
