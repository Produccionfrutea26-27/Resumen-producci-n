# Dashboard Recepción de Fruta · FRUTEA

Dashboard interactivo de recepción de fruta, con filtros por temporada, tipo de recepción, especie, variedad, bodega, semana y razón social.

## Archivos

| Archivo | Qué es |
|---|---|
| `index.html` | El dashboard. |
| `datos.js` | Los datos que muestra el dashboard. **Es el único archivo que cambia al actualizar.** |
| `actualizar_datos.py` | Opcional: convierte el Excel en `datos.js` desde tu computador. |

## Publicarlo con GitHub Pages (una sola vez)

1. Crea un repositorio nuevo en GitHub y sube estos archivos (**Add file → Upload files**).
2. Entra a **Settings → Pages**.
3. En *Build and deployment* elige **Deploy from a branch**, rama `main`, carpeta `/ (root)` y guarda.
4. En uno o dos minutos GitHub te muestra el enlace del dashboard.

> **Ojo con la privacidad:** el dashboard tiene nombres de productores, CSG y kilos. En un repositorio **público**, cualquiera que tenga el enlace puede verlo. Para un repositorio privado con Pages se necesita un plan pagado de GitHub (Pro, Team o Enterprise).

## Conectar el dashboard con GitHub (una sola vez)

Así, al subir el Excel en el dashboard, los datos se guardan solos en el repositorio y todos ven la actualización.

1. En GitHub, haz clic en tu foto (arriba a la derecha) → **Settings** → **Developer settings** (al final del menú izquierdo) → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**.
2. Ponle un nombre (por ejemplo `dashboard-frutea`) y una fecha de vencimiento (por ejemplo 1 año).
3. En **Repository access** elige **Only select repositories** y selecciona este repositorio.
4. En **Permissions → Repository permissions → Contents** elige **Read and write**.
5. Pulsa **Generate token** y copia el token (empieza con `github_pat_`). GitHub lo muestra una sola vez.
6. Abre el dashboard → **⬆ ACTUALIZAR DATOS** → **⚙ Conexión con GitHub**, pega el token y pulsa **Guardar**.

El token queda guardado solo en tu navegador; no se sube al repositorio. No lo compartas: quien lo tenga puede modificar el repositorio. Si lo pierdes o vence, crea uno nuevo y vuelve a guardarlo.

## Actualizar los datos cada día

1. Abre el dashboard y despliega **⬆ ACTUALIZAR DATOS**.
2. Arrastra el Excel del día (hoja con columnas `temporada`, `especie`, `kilos_netos`, `fecha_recepcion`, etc.).
3. Revisa el resumen y pulsa **Publicar para todos**.
4. Listo: en 1 a 2 minutos todos ven los datos nuevos (si alguien no los ve, que recargue la página).

Otros botones:

- **Solo ver en mi navegador**: para revisar el Excel antes de publicarlo; nadie más lo ve.
- **Descargar datos.js**: por si quieres subir el archivo a mano (GitHub → **Add file → Upload files**).

### Alternativa con Python

```bash
pip install pandas openpyxl
python actualizar_datos.py "Resumen Materia Prima.xlsx"
git add datos.js && git commit -m "Actualiza datos" && git push
```

## Cómo se combinan los datos

Las temporadas que vienen en el Excel **reemplazan** a esas mismas temporadas en `datos.js`; las demás temporadas se mantienen. Así puedes subir cada día el Excel completo de la temporada actual sin perder las anteriores.

Si una fecha de recepción viene con un año de 2030 o más (por ejemplo 2055 por error de digitación), se corrige restándole 30 años.
