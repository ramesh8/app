import io
import subprocess
from doc2pdf import convert, get_office_cli_path

libreoffice_path = get_office_cli_path()

print(libreoffice_path)

libreoffice_command = [
    libreoffice_path,
    "--headless",
    "--convert-to",
    "pdf",
    "/dev/stdin",  #'/dev/stdin',  # Read from  ( use /dev/stdin for linux & CON for windows)
    "--outdir",
    "/dev/stdout",  #'/dev/stdout',  # Write to stdout ( use /dev/stdout for linux & CON for windows)
]
try:
    with open("sample.pdf", "r") as fp:
        file_body = fp.read()

    input_stream = io.BytesIO(file_body)
    output_stream = io.BytesIO()
    # Run the LibreOffice command and capture stdout
    process = subprocess.run(
        libreoffice_command, input=input_stream.read(), check=True, capture_output=True
    )
    # Get the converted PDF content from the output stream
    # process = subprocess.run(libreoffice_command, input=file_body, stdout=subprocess.PIPE, check=True,capture_output=True)
    pdf_content = process.stdout
except subprocess.CalledProcessError as e:
    print(f"Error running LibreOffice command: {e}")
    pdf_content = b""
