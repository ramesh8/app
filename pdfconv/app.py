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
    with open("go.docx", "rb") as fp:
        file_body = fp.read()

    # input_stream = io.BytesIO(file_body)
    # output_stream = io.BytesIO()
    # Run the LibreOffice command and capture stdout
    # process = subprocess.run(
    #     libreoffice_command, input=input_stream.read(), check=True, capture_output=True
    # )
    process = subprocess.Popen(
        libreoffice_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False
    )
    # Get the converted PDF content from the output stream
    # process = subprocess.run(libreoffice_command, input=file_body, stdout=subprocess.PIPE, check=True,capture_output=True)
    # pdf_content = process.stdout
    output = b""
    process.stdin.write(file_body)
    while True:
        buff = process.stdout.read()
        if len(buff) > 0:
            output += buff
        else:
            errormsg = process.poll()
            if errormsg is not None:
                break

    with open("output.pdf", "wb") as fp:
        fp.write(output)
except subprocess.CalledProcessError as e:
    print(f"Error running LibreOffice command: {e}")
    pdf_content = b""
