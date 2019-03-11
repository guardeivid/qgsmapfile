# -*- coding: utf-8 -*-
"""docstring for svg_painter.py"""
from PyQt4.QtCore import QPointF, QPoint,  QRect, QRectF, QSize
from PyQt4.QtGui import QPainter, QPolygon, QPolygonF, QPainterPath
from PyQt4.QtSvg import QSvgGenerator

def vector2svg(mssymbol):
    if mssymbol["type"] != 'vector':
        return False
    
    pf = []
    points = mssymbol.get("points", [])
    min_ = min(points)
    max_ = max(points)
    print(min_)
    for p in points:
        x = float(p[0])
        y = float(p[1])
        
        if x == -99:
            pass
        
        pf.append(QPointF(x, y))
        
    
    polygon = QPolygonF(pf)
        
    painter = QPainter()
    painter.drawPolygon(polygon)
    
    painter.save()
    
    name = mssymbol.get("name", 'tmp')
    path = "C:\\Users\\User\\.qgis2\\python\\plugins\\QgsMapfile\\test\\" + name + ".svg"
    generator = QSvgGenerator()
    generator.setFileName(path);
    generator.setSize(QSize(max_[0],max_[1]));
    generator.setViewBox(QRectF(min_[0], min_[1], max_[0],max_[1]))
    
    painter.begin(generator)
    painter.drawPolygon(polygon)
    painter.end() 
            
    print(painter)
    """if mssymbol["filled"]:
        points = QPolygonF([
            QPointF(float(10), float(80)),
            QPointF(float(20), float(10)),
            QPointF(float(80), float(30))
        ])
        print(points)
  
    print(mssymbol)
    """
#print(float(10))
        
sym = {
    "type": "vector",
    "name": "rectangle",
    "filled": True,
    "points": [
    (0, 0),
    (1, 0),
    (1, 0.8),
    (-99, -99),
    (0, 0.8),
    (0, 0),
    ]
}

#p = QPointF(float(0), float(1))
#print(p)

vector2svg(sym)
painter = QPainter()
path = QPainterPath()

#polygon = QPolygonF()
#polygon.add
#polygon << QPointF(10.4, 20.5) << QPointF(20.2, 30.2)