"""Use the database provider to connect to PostgreSQL.
This script is set up to run under the Script Runner plugin, but
can be also be run from the Python console.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from qgis.core import *


def run_script(iface):
    # get the active layer
    layer = iface.activeLayer()
    # get the underlying data provider
    provider = layer.dataProvider()
    if provider.name() == 'postgres':
        # get the URI containing the connection parameters
        uri = QgsDataSourceURI(provider.dataSourceUri())
        print uri.uri()
        # create a PostgreSQL connection using QSqlDatabase
        db = QSqlDatabase.addDatabase('QPSQL')
        # check to see if it is valid
        if db.isValid():
            print "QPSQL db is valid"
            # set the parameters needed for the connection
            db.setHostName(uri.host())
            db.setDatabaseName(uri.database())
            db.setPort(int(uri.port()))
            db.setUserName(uri.username())
            db.setPassword(uri.password())
            # open (create) the connection
            if db.open():
                print "Opened %s" % uri.uri()
                # execute a simple query 
                query = db.exec_("""select * from qgis_sample.airports
                    order by name""")
                # loop through the result set and print the name
                while query.next():
                    record = query.record()
                    print record.field('name').value().toString()
            else:
                err = db.lastError()
                print err.driverText()