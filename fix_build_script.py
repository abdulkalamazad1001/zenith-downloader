import os

file_path = 'render-build.sh'
if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Replace CRLF with LF
    content = content.replace(b'\r\n', b'\n')
    
    with open(file_path, 'wb') as f:
        f.write(content)
    print("Fixed line endings for render-build.sh")
else:
    print("File not found")
