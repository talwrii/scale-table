import collections
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


MAJOR = (0, 2, 4, 5, 7, 9, 11)

def major_scale(x):
    return [(x + i) % 12 for i in MAJOR]

def list_transpose(n, xs):
    return tuple(transpose(n, x) for x in xs)

def transpose(n, x):
    return (x + n) % 12


def fifth(x):
    return transpose(7, x)

def list_fifth(xs):
    return list_transpose(7, xs)

def flat_name(x):
    return {
        0: 'C',
        1: 'Db',
        2: 'D',
        3: 'Eb',
        4: 'E',
        5: 'F',
        6: 'Gb',
        7: 'G',
        8: 'Ab',
        9: 'A',
        10: 'Bb',
        11: 'B'}[x]

def sharp_name(x):
    return {
        0: 'C',
        1: 'C#',
        2: 'D',
        3: 'D#',
        4: 'E',
        5: 'F',
        6: 'F#',
        7: 'G',
        8: 'G#',
        9: 'A',
        10: 'A#',
        11: 'B'
    }[x]

def sharp_name_list(xs):
    return list(map(sharp_name, xs))

def letter_collision(names):
    return max(collections.Counter(n[0] for n in names if n != '').values()) != 1

def draw_row(xs):
    pitches = [i if i in xs else None for i in range(12)]
    flats = [flat_name(p) if p is not None else '' for p in pitches]
    sharps = [sharp_name(p) if p is not None else '' for p in pitches]
    if not letter_collision(flats):
        return flats
    elif not letter_collision(sharps):
        return sharps
    else:
        raise Exception(f'Both sharps and flats have collisions: {flats} {sharps}')

def repeat(n, f, x):
    r = x
    for i in range(n):
        r = f(r)
    return r


style = TableStyle()
style.add('ALIGN', (0, 0), (-1, -1), 'CENTER')
for col in range(0, 24):
    for row in range(0, 24):
        if col % 2 == row % 2 == 0:
            style.add('BACKGROUND', (col, row), (col, row), colors.darkgrey)
        elif col % 2 == 0 or row % 2 == 0:
            style.add('BACKGROUND', (col, row), (col, row), colors.silver)



rows = []
circle_of_fifths = [repeat(i, fifth, 0) for i in range(12)]
for repeat in (0, 1):
    for i, x in enumerate(circle_of_fifths):
        row_num = i + 12 * repeat
        del i

        if x == 6:
            row = ['', 'C#', '', 'D#', '',  'E#', 'F#', '', 'G#', '', 'A#', 'B']
        else:
            row = draw_row(major_scale(x))


        minor = (x - 3) % 12

        row = [c or '*' for c in row]

        for k in (0, 1):
            style.add('BACKGROUND', (x + 12 * k, row_num), (x + 12 * k, row_num), colors.lightgreen)
            style.add('BACKGROUND', (minor + 12 * k, row_num), (minor + 12 * k, row_num), colors.violet)

        double_row = row + row

        for i, name in enumerate(double_row):
            if '#' in name:
                style.add('TEXTCOLOR', (i, row_num), (i, row_num), colors.red)

            if 'b' in name:
                style.add('TEXTCOLOR', (i, row_num), (i, row_num), colors.blue)

        rows.append(double_row)










doc = SimpleDocTemplate("scale.pdf", pagesize=landscape(A4))
table = Table(rows)
table.setStyle(style)
doc.build([table])
