import json
import html
from pathlib import Path

SOURCE = Path('/Users/mirandagrein/Downloads/Final_Test_Study_Guide.ipynb')
TARGET = Path('/Users/mirandagrein/Downloads/Final_Test_Study_Guide_single_page.html')


def as_text(value):
    if isinstance(value, list):
        return ''.join(value)
    return value or ''


def build_page(notebook):
    cells = notebook.get('cells', [])
    page = []
    page.append('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">')
    page.append('<title>Final Test Study Guide - Single Page</title>')
    page.append('''<style>
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial,sans-serif;margin:14px;font-size:11px;line-height:1.35;color:#1f2937}
h1{font-size:16px;margin:0 0 8px}.meta{color:#4b5563;margin-bottom:12px}
.cell{border:1px solid #e5e7eb;border-radius:6px;margin:8px 0;overflow:hidden}
.cell-head{background:#f9fafb;border-bottom:1px solid #e5e7eb;padding:4px 8px;font-size:10px;color:#374151}
.cell-body{padding:8px}pre{margin:0;white-space:pre-wrap;word-wrap:break-word;font-size:10px;line-height:1.3;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace}
.code pre{background:#f8fafc;padding:6px;border-radius:4px}.output{margin-top:6px;border-top:1px dashed #d1d5db;padding-top:6px}
.output-label{font-size:10px;color:#6b7280;margin-bottom:4px}.output-html{overflow-x:auto}img{max-width:100%;height:auto}
</style></head><body>''')
    page.append('<h1>Final Test Study Guide - Single Page Export</h1>')
    page.append('<div class="meta">Source: Final_Test_Study_Guide.ipynb | Includes all cells and saved outputs</div>')

    for idx, cell in enumerate(cells, start=1):
        cell_type = cell.get('cell_type', 'unknown')
        source = as_text(cell.get('source', ''))
        page.append('<section class="cell {0}">'.format(html.escape(cell_type)))
        page.append('<div class="cell-head">Cell {0} - {1}</div>'.format(idx, html.escape(cell_type)))
        page.append('<div class="cell-body">')

        if cell_type == 'code':
            page.append('<div class="code"><pre>{0}</pre></div>'.format(html.escape(source)))
            for out_idx, out in enumerate(cell.get('outputs', []), start=1):
                page.append('<div class="output">')
                output_type = out.get('output_type', 'output')
                page.append('<div class="output-label">Output {0} - {1}</div>'.format(out_idx, html.escape(output_type)))

                if output_type == 'stream':
                    page.append('<pre>{0}</pre>'.format(html.escape(as_text(out.get('text', '')))))
                elif output_type == 'error':
                    traceback = out.get('traceback') or []
                    error_text = '\n'.join(traceback) if traceback else '{0}: {1}'.format(out.get('ename', ''), out.get('evalue', ''))
                    page.append('<pre>{0}</pre>'.format(html.escape(error_text)))
                else:
                    data = out.get('data', {}) or {}
                    if 'text/html' in data:
                        page.append('<div class="output-html">{0}</div>'.format(as_text(data.get('text/html'))))
                    if 'image/png' in data:
                        page.append('<img src="data:image/png;base64,{0}" alt="output-image">'.format(as_text(data.get('image/png'))))
                    if 'text/plain' in data:
                        page.append('<pre>{0}</pre>'.format(html.escape(as_text(data.get('text/plain')))))
                    if 'text/markdown' in data:
                        page.append('<pre>{0}</pre>'.format(html.escape(as_text(data.get('text/markdown')))))
                    if 'application/json' in data:
                        page.append('<pre>{0}</pre>'.format(html.escape(json.dumps(data.get('application/json'), indent=2, ensure_ascii=False))))

                page.append('</div>')
        else:
            page.append('<div class="markdown"><pre>{0}</pre></div>'.format(html.escape(source)))

        page.append('</div></section>')

    page.append('</body></html>')
    return ''.join(page)


def main():
    notebook = json.loads(SOURCE.read_text(encoding='utf-8'))
    TARGET.write_text(build_page(notebook), encoding='utf-8')
    print(str(TARGET))


if __name__ == '__main__':
    main()
