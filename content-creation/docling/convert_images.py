import os
import glob
from docling.document_converter import DocumentConverter

def main():
    # Find all png files in the current directory
    png_files = sorted(glob.glob("*.png"))
    if not png_files:
        print("No PNG files found in the current directory.")
        return

    print(f"Found {len(png_files)} PNG files to convert.")
    converter = DocumentConverter()

    for png_file in png_files:
        md_file = os.path.splitext(png_file)[0] + ".md"
        print(f"Converting '{png_file}' to '{md_file}'...")
        try:
            result = converter.convert(png_file)
            markdown_content = result.document.export_to_markdown()
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"Successfully converted and saved '{md_file}'.")
        except Exception as e:
            print(f"Error converting '{png_file}': {e}")

if __name__ == "__main__":
    main()
