import ast
from collections import defaultdict
from models import GartmentTable

def _parse_rects(raw: str):
    if not raw:
        return []

    try:
        text = raw.replace('(', '[').replace(')', ']').replace("'", '"')
        text = f'[{text}]'
        parsed = ast.literal_eval(text)
        return [r for r in parsed if isinstance(r, list) and len(r) == 6 and all(not isinstance(e, list) for e in r[3:5])]
    except Exception as e:
        print(f"Erro ao processar retângulos: {e}")
        return []

def _to_vertices(item):
    if not isinstance(item, list) or len(item) != 6:
        raise ValueError(f"Retângulo inválido: {item}")
    _, x, y, w, h, rid = item
    return {
        "clothingId": str(rid),
        "vertices": [
            [x,     y],
            [x + w, y],
            [x + w, y + h],
            [x,     y + h],
        ]
    }

class Utils:

    @staticmethod
    def mount_table_return(table: GartmentTable):
        maxr = _parse_rects(table.bin_maxrects)
        sky  = _parse_rects(table.bin_skyline)
        gui  = _parse_rects(table.bin_guillotine)

        dims = defaultdict(list)
        for r in maxr:
            if len(r) >= 5:
                dims[(int(r[3]), int(r[4]))].append(r)
            else:
                print(f"Retângulo Inválido: {r}")

        for (w, h), group in list(dims.items()):
            if len(group) == 2:
                r1, r2 = group
                maxr.remove(r1)
                maxr.remove(r2)
                x0 = min(r1[1], r2[1])
                y0 = min(r1[2], r2[2])
                new = [r1[0], x0, y0, w, h * 2, f"sleeve_{r1[5]}"]
                maxr.append(new)

        return {
            "width":      table.width,
            "height":     table.height,
            "maxRects":   [_to_vertices(r) for r in maxr],
            "skyline":    [_to_vertices(r) for r in sky ],
            "guillotine": [_to_vertices(r) for r in gui ],
        }
