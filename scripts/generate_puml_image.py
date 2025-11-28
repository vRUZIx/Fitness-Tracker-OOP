import os
import sys
import zlib
import urllib.request

# Ensure src is importable if run from repo root
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_PUML = os.path.join(BASE, 'docs', 'class_diagram.puml')
DEFAULT_OUT = os.path.join(BASE, 'docs', 'class_diagram.png')

# PlantUML server URL (public)
PLANTUML_SERVER = 'https://www.plantuml.com/plantuml/png/'

# Encoding per PlantUML: deflate (zlib) then encode to PlantUML base64 alphabet
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def encode_plantuml(text: bytes) -> str:
    # Use raw DEFLATE (no zlib header/footer) to match PlantUML expectation
    compressor = zlib.compressobj(level=9, wbits=-15)
    deflated = compressor.compress(text) + compressor.flush()

    def to_6bit(b):
        if b < 0:
            b += 256
        return b

    res = []
    data = deflated
    i = 0
    while i < len(data):
        # take 3 bytes (24 bits)
        b1 = to_6bit(data[i])
        b2 = to_6bit(data[i + 1]) if i + 1 < len(data) else 0
        b3 = to_6bit(data[i + 2]) if i + 2 < len(data) else 0
        i += 3
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        res.append(ALPHABET[c1])
        res.append(ALPHABET[c2])
        res.append(ALPHABET[c3])
        res.append(ALPHABET[c4])
    # If padding occurred, we must trim according to remainder
    # PlantUML encoding uses this direct conversion; above handles final block with zeros
    return ''.join(res)


def main():
    # Accept optional args: input PUML path and output PNG path
    pu_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PUML
    out_path = sys.argv[2] if len(sys.argv) > 2 else (os.path.splitext(pu_path)[0] + '.png')

    if not os.path.exists(pu_path):
        print('PUML file not found at', pu_path)
        sys.exit(1)
    with open(pu_path, 'rb') as f:
        text = f.read()
    encoded = encode_plantuml(text)
    url = PLANTUML_SERVER + encoded
    print('Requesting:', url)
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = resp.read()
    except Exception as e:
        print('Failed to fetch image:', e)
        sys.exit(2)
    with open(out_path, 'wb') as f:
        f.write(data)
    print('Wrote image to', out_path)


if __name__ == '__main__':
    main()
