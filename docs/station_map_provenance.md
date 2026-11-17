# Station map provenance

The station map is an editorial geographic display of the 12 period-median coordinates and station roles already reported in Supplementary Table S1. It adds no observation, station reassignment, satellite footprint, or coverage result.

## Rebuild

```bash
python scripts/render_station_map.py
```

The script depends only on Matplotlib and the Python standard library. It reads `data/station_locations.csv` and the bundled offline land subset. The PDF is a vector figure, 7.16 by 4.2 inches, with embedded TrueType fonts and a minimum text size of 8 points. It should be used at full two-column width rather than reduced to a single column.

## Station input

`data/station_locations.csv` contains eight evaluation stations and four development stations. All numerical coordinates and original selection labels are unchanged from the supplied manuscript. The labels are study-protocol assignments, not independently validated geographic or product-coverage classes. The special note for 42056 reflects the unresolved distinction between its original Gulf selection label and the NDBC Yucatan Basin station metadata already discussed in the supplement.

## Land input

- Dataset: Natural Earth 1:50m physical land polygons.
- Actual retrieved dataset version: 4.0.0, as recorded in the repository's `50m_physical/ne_50m_land.VERSION.txt`.
- Immutable source commit: `693f11422f4e08d2da4566b854dda53eb7c39fb3`.
- Original source Git blob SHA: `c412c52b5286ba727dcb7047ecd6080bcbeb8298`.
- [Source GeoJSON](https://github.com/nvkelso/natural-earth-vector/blob/693f11422f4e08d2da4566b854dda53eb7c39fb3/geojson/ne_50m_land.geojson).
- [Version record](https://github.com/nvkelso/natural-earth-vector/blob/693f11422f4e08d2da4566b854dda53eb7c39fb3/50m_physical/ne_50m_land.VERSION.txt).
- [Official terms of use](https://www.naturalearthdata.com/about/terms-of-use/): public domain; no separate permission is required.

The bundled GeoJSON retains all 92 complete source features whose bounding boxes intersect the region from 99 W to 63 W and 16 N to 47 N. Source coordinates and geometries are unchanged; only feature selection and JSON serialization were performed. The plotting axes clip the rendered view. The subset is about 267 KB, and its SHA-256 is recorded in `data/basemaps/natural_earth_provenance.json`.

## Rendering and interpretation

Both panels use an equidistant cylindrical projection with standard parallel 32 N. Longitude is transformed to `longitude * cos(32 degrees)` and latitude is retained; map axes use equal projected-unit aspect ratios. Coordinates are labeled in geographic degrees. The northeast inset separates the closely spaced 44008, 44020, and 44027 labels. Evaluation and development roles use both different symbols and different colors.

Land outlines are generalized context at 1:50m scale. They cannot establish a station's precise near-shore placement or a satellite file's observation support. The dashed box denotes only the inset extent. No product-sector borders are drawn.

Suggested caption attribution: “Land outlines: Natural Earth, 1:50m.” A full citation is optional under the data provider's public-domain terms; the source version and immutable retrieval record are retained here regardless.

## Assistance scope

ChatGPT assisted with the new display's design and plotting code. Station coordinates and roles were transcribed from the source manuscript; the land coordinates came from Natural Earth. No generative-image model was used, and this display does not represent a new scientific acquisition or coverage experiment.
