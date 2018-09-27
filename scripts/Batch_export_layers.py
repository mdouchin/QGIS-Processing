##Vector=group
##Batch export layers=name
##Vector_layers=multiple vector
##Format=selection ESRI Shapefile;GeoJSON;CSV;ODS
##Use_table_name_instead_of_layer_name_for_database_layers=boolean True
##Output_folder=folder

from processing.tools.vector import VectorWriter
from qgis.core import QgsDataSourceURI, QgsCoordinateReferenceSystem

ogr_extensions = {
    0: 'shp',
    1: 'geojson',
    2: 'csv',
    3: 'ods'
}

layers = Vector_layers.split(';')
for l in layers:
    layer = processing.getObject(l)
    lname = layer.name()
    progress.setInfo('%s' % lname)

    # Create filename for this layer
    output_name = layer.name()
    if layer.providerType() == 'postgres' and Use_table_name_instead_of_layer_name_for_database_layers:
        output_name = QgsDataSourceURI(layer.dataProvider().dataSourceUri()).table()
    output_filename = Output_folder + '/' + output_name + '.' + ogr_extensions[Format]
    progress.setInfo(output_filename)

    # CRS
    lcrs = layer.crs()
    progress.setInfo('Layer CRS = %s' % lcrs.authid())

    # Create writer
    writer = VectorWriter(
        output_filename,
        None,
        layer.dataProvider().fields(),
        layer.dataProvider().geometryType(),
        lcrs
    )

    # Export features
    features = layer.getFeatures()
    for feat in features:
        writer.addFeature(feat)

    del writer
    progress.setInfo('  -> OK')
    progress.setInfo('----------')
