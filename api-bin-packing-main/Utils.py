import ast
from collections import defaultdict
from models import GartmentTable

def _parse_rects(raw: str):
    if not raw:
        return []
    text = raw.replace('(', '[').replace(')', ']').replace("'", '"')
    text = f'[{text}]'
    return ast.literal_eval(text)

def _to_vertices(item):
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
            dims[(r[3], r[4])].append(r)

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
