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

## Actualizar los datos cada día

### Opción A: desde el mismo dashboard (sin instalar nada)

1. Abre el dashboard y despliega **⬆ ACTUALIZAR DATOS**.
2. Arrastra el Excel del día (hoja con columnas `temporada`, `especie`, `kilos_netos`, `fecha_recepcion`, etc.).
3. Revisa el resumen y pulsa **Descargar datos.js**.
4. En GitHub: **Add file → Upload files**, sube ese `datos.js` (reemplaza al anterior) y pulsa **Commit changes**.
5. En uno o dos minutos todos ven los datos nuevos.

El botón **Ver en este navegador** solo sirve para revisar el Excel antes de publicarlo: los datos quedan guardados únicamente en tu navegador. Para volver a los datos publicados usa **Volver a los datos publicados**.

### Opción B: con Python

```bash
pip install pandas openpyxl
python actualizar_datos.py "Resumen Materia Prima.xlsx"
git add datos.js && git commit -m "Actualiza datos" && git push
```

## Cómo se combinan los datos

Las temporadas que vienen en el Excel **reemplazan** a esas mismas temporadas en `datos.js`; las demás temporadas se mantienen. Así puedes subir cada día el Excel completo de la temporada actual sin perder las anteriores.

Si una fecha de recepción viene con un año de 2030 o más (por ejemplo 2055 por error de digitación), se corrige restándole 30 años.
