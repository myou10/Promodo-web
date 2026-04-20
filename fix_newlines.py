import sys

def main():
    file_path = r'c:\Users\ACER\Downloads\Promodo-web-main\Promodo-web-main\index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for literal newline occurrences inside the bad strings
    content = content.replace("label: 'Mạng\nxã hội'", "label: 'Mạng\\nxã hội'")
    content = content.replace("label: 'Tin\nnhắn'", "label: 'Tin\\nnhắn'")
    content = content.replace("label: 'Ăn\nuống'", "label: 'Ăn\\nuống'")
    
    # Also handle Windows newlines just in case
    content = content.replace("label: 'Mạng\r\nxã hội'", "label: 'Mạng\\nxã hội'")
    content = content.replace("label: 'Tin\r\nnhắn'", "label: 'Tin\\nnhắn'")
    content = content.replace("label: 'Ăn\r\nuống'", "label: 'Ăn\\nuống'")
    
    # Also fix the weird replace function
    content = content.replace("d.label.replace('\n', '\n')", "d.label")
    content = content.replace("d.label.replace('\r\n', '\r\n')", "d.label")
    
    # Wait, in the view result it looked like:
    '''d.label.replace('
', '
')'''
    # We will just replace it simply
    content = content.replace("d.label.replace('\\n', '\\n')", "d.label")
    # Actually just a regex to wipe out the whole replace part for certainty
    import re
    content = re.sub(r"d\.label\.replace\(\s*['\"\n\r]+.*?\)", "d.label", content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
