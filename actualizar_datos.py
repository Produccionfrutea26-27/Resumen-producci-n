"""Convierte el Excel de recepciones en datos.js para el dashboard.

Uso:
    python actualizar_datos.py "Resumen Materia Prima.xlsx"

Requiere: pip install pandas openpyxl
Las temporadas que vienen en el Excel reemplazan a esas mismas temporadas
en datos.js; las demás temporadas se mantienen.
"""
import json, re, sys, datetime, pathlib
import pandas as pd

REQ = ['temporada', 'tipo_recepcion', 'especie', 'descripcion_bodega', 'variedad',
       'razon_social_entidad', 'semana_recepcion', 'kilos_netos', 'fecha_recepcion', 'codigo_csg']
AQUI = pathlib.Path(__file__).parent
DATOS = AQUI / 'datos.js'


def leer_excel(ruta):
    for hoja, df in pd.read_excel(ruta, sheet_name=None).items():
        df.columns = [str(c).strip().lower() for c in df.columns]
        if all(c in df.columns for c in REQ):
            return hoja, df
    sys.exit('No encontré una hoja con las columnas: ' + ', '.join(REQ))


def agregar(df):
    df = df.copy()
    s = lambda c: df[c].fillna('').astype(str).str.strip()
    df['kilos_netos'] = pd.to_numeric(df['kilos_netos'], errors='coerce')
    fr = pd.to_datetime(df['fecha_recepcion'], errors='coerce', dayfirst=True)
    fr = fr.where(fr.dt.year < 2030, fr - pd.DateOffset(years=30))  # años mal digitados (ej. 2055)
    fc = pd.to_datetime(df.get('fecha_cosecha'), errors='coerce', dayfirst=True) if 'fecha_cosecha' in df else pd.Series(pd.NaT, index=df.index)
    ok = df['kilos_netos'].notna() & fr.notna() & (s('especie') != '')
    df, fr, fc = df[ok], fr[ok], fc[ok]
    out = pd.DataFrame({
        't': s('temporada')[ok], 'ti': s('tipo_recepcion')[ok], 'e': s('especie')[ok],
        'b': s('descripcion_bodega')[ok].str.replace(r'-+$', '', regex=True).str.strip(),
        'v': s('variedad')[ok], 'p': s('razon_social_entidad')[ok],
        'sem': pd.to_numeric(df['semana_recepcion'], errors='coerce').fillna(0).astype(int),
        'f': fr.dt.strftime('%Y-%m-%d'),
        'fc': fc.dt.strftime('%Y-%m-%d').where(fc.notna() & (fc <= fr.dt.normalize()), '9999'),
        'csg': s('codigo_csg')[ok],
        'k': df['kilos_netos'],
        'c': pd.to_numeric(df['cant_envases_primarios'], errors='coerce').fillna(0) if 'cant_envases_primarios' in df else 1,
    })
    g = out.groupby(['t', 'ti', 'e', 'b', 'v', 'p', 'sem', 'f', 'fc', 'csg'], as_index=False).agg(k=('k', 'sum'), c=('c', 'sum'))
    rows = [[r.t, r.ti, r.e, r.b, r.v, r.p, int(r.sem), round(float(r.k), 1), int(round(r.c)), r.f, r.fc, r.csg] for r in g.itertuples()]
    return rows, int(ok.sum()), int((~ok).sum())


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ruta = pathlib.Path(sys.argv[1])
    hoja, df = leer_excel(ruta)
    nuevas, n, omitidas = agregar(df)
    temps = sorted({r[0] for r in nuevas})
    previas = []
    if DATOS.exists():
        txt = DATOS.read_text(encoding='utf-8')
        previas = json.loads(re.sub(r'^\s*window\.DATOS\s*=\s*|;\s*$', '', txt.strip()))['rows']
    filas = [r for r in previas if r[0] not in temps] + nuevas
    ds = {'rows': filas, 'meta': {'archivo': ruta.name, 'actualizado': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'hoja': hoja, 'filas': n}}
    DATOS.write_text('window.DATOS=' + json.dumps(ds, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
    print(f'Listo: {n} líneas leídas ({omitidas} omitidas) · temporadas {", ".join(temps)} · {sum(r[7] for r in nuevas):,.0f} kg')


if __name__ == '__main__':
    main()
