import re
import zlib
from pathlib import Path
from statistics import mean

PDF_DIR = Path('.')


def parse_cmaps(pdf_bytes: bytes) -> dict[int, str]:
    """Return combined ToUnicode mapping for a PDF."""
    mappings = {}
    for m in re.finditer(rb'/ToUnicode\s+(\d+)\s+0\s+R', pdf_bytes):
        obj_num = int(m.group(1))
        obj_match = re.search(fr'{obj_num} 0 obj'.encode() + rb'(.*?)endobj', pdf_bytes, re.S)
        if not obj_match:
            continue
        block = obj_match.group(1)
        if b'stream' not in block:
            continue
        data = block.split(b'stream')[1].split(b'endstream')[0].strip(b'\r\n')
        try:
            decoded = zlib.decompress(data)
        except Exception:
            decoded = data
        cmap = {}
        for line in decoded.decode('latin1', errors='ignore').split('\n'):
            parts = line.strip().split()
            if len(parts) == 3 and parts[0].startswith('<') and parts[1].startswith('<'):
                start = int(parts[0][1:-1], 16)
                end = int(parts[1][1:-1], 16)
                base = int(parts[2][1:-1], 16)
                for i, code in enumerate(range(start, end + 1)):
                    target = base + i
                    if target <= 0x10FFFF:
                        cmap[code] = chr(target)
            elif len(parts) == 2 and parts[0].startswith('<') and parts[1].startswith('<'):
                key = int(parts[0][1:-1], 16)
                target = int(parts[1][1:-1], 16)
                if target <= 0x10FFFF:
                    cmap[key] = chr(target)
        mappings[obj_num] = cmap
    combined = {k: v for mp in mappings.values() for k, v in mp.items()}
    return combined


def extract_text(pdf_path: Path) -> str:
    pdf_bytes = pdf_path.read_bytes()
    cmap = parse_cmaps(pdf_bytes)

    def decode_hex(hexstr: bytes) -> str:
        text = ''
        bs = hexstr.decode()
        chunk = 2 if len(bs) % 4 == 2 else 4
        for i in range(0, len(bs), chunk):
            text += cmap.get(int(bs[i:i + chunk], 16), '')
        return text

    output: list[str] = []
    for m in re.finditer(rb'stream\r?\n', pdf_bytes):
        start = m.end()
        end = pdf_bytes.find(b'endstream', start)
        if end == -1:
            continue
        data = pdf_bytes[start:end].strip(b'\r\n')
        try:
            decoded = zlib.decompress(data)
        except Exception:
            continue
        for hexstr in re.findall(rb'<([0-9A-Fa-f]+)>\s*Tj', decoded):
            output.append(decode_hex(hexstr))
        for s in re.findall(rb'\(([^)]*)\)\s*Tj', decoded):
            try:
                output.append(s.decode())
            except Exception:
                pass
        for array in re.findall(rb'\[(.*?)\]\s*TJ', decoded, re.S):
            for part in re.findall(rb'<([0-9A-Fa-f]+)>|\(([^)]*)\)', array):
                hex_part, text_part = part
                if hex_part:
                    output.append(decode_hex(hex_part))
                elif text_part:
                    try:
                        output.append(text_part.decode())
                    except Exception:
                        pass
    return ''.join(output)


def extract_probability(text: str) -> float | None:
    match = re.search(r'Probability:\s*([0-9.]+)', text)
    return float(match.group(1)) if match else None


def main():
    rows = []
    for pdf in sorted(PDF_DIR.glob('*.pdf')):
        text = extract_text(pdf)
        prob = extract_probability(text)
        actual = 'success' if pdf.stem.endswith('a') else 'failure'
        rows.append((pdf.name, actual, prob))

    probs_success = [p for _, actual, p in rows if actual == 'success' and p is not None]
    probs_failure = [p for _, actual, p in rows if actual == 'failure' and p is not None]

    lines = [
        '# Probability 提取结果',
        '',
        f'总计处理 PDF：{len(rows)} 份。',
        f'成功样本（a）：{len([r for r in rows if r[1]=="success"])} 份，失败样本（c）：{len([r for r in rows if r[1]=="failure"])} 份。',
        '',
    ]

    if probs_success:
        lines.append(f'真实成功公司 Probability 平均值：{mean(probs_success):.4f}')
    if probs_failure:
        lines.append(f'真实失败公司 Probability 平均值：{mean(probs_failure):.4f}')
    lines.append('')

    lines.append('| 文件 | 实际结果 | Probability |')
    lines.append('| --- | --- | --- |')
    for name, actual, prob in rows:
        prob_str = f'{prob:.4f}' if prob is not None else 'N/A'
        lines.append(f'| {name} | {actual} | {prob_str} |')

    Path('probability_analysis.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
