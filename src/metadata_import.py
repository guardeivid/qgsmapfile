# -*- coding: utf-8 -*-
"""docstring for metadata_import.py"""

from builtins import object

class MetadataImportVectorLayer(object):
    """docstring for MetadataImportVectorLayer"""
    def __init__(self, arg):
        super(MetadataImportVectorLayer, self).__init__()
        self.arg = arg






"""
 QIcon QgsFields::iconForField( int fieldIdx ) const
 {
   switch ( d->fields.at( fieldIdx ).field.type() )
   {
     case QVariant::Int:
     case QVariant::UInt:
     case QVariant::LongLong:
     case QVariant::ULongLong:
     {
       return QgsApplication::getThemeIcon( "/mIconFieldInteger.svg" );
     }
     case QVariant::Double:
     {
       return QgsApplication::getThemeIcon( "/mIconFieldFloat.svg" );
     }
     case QVariant::String:
     {
       return QgsApplication::getThemeIcon( "/mIconFieldText.svg" );
     }
     case QVariant::Date:
     {
       return QgsApplication::getThemeIcon( "/mIconFieldDate.svg" );
     }
     case QVariant::DateTime:
     {
       return QgsApplication::getThemeIcon( "/mIconFieldDateTime.svg" );
     }
     case QVariant::Time:
     {
       return QgsApplication::getThemeIcon( "/mIconFieldTime.svg" );
     }
     default:
       return QIcon();
   }
 }
 """