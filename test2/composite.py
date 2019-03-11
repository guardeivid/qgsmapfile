from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict
from mappyfile.ordereddict import DefaultOrderedDict, CaseInsensitiveOrderedDict

def get_dict(s):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict()
    ast = p.parse(s)
    d = m.transform(ast)
    return d

s = """
    LAYER
        NAME "Layer1"
        COMPOSITE
            OPACITY 50
        END
        CLASS
            NAME "Class1"
        END
    END
    """
    
d = get_dict(s)

#print(d)
c = d.get('composites')
print(c[0].get('opacity'))