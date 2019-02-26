# -*- coding: utf-8 -*-
"""docstring for import_.py"""

from builtins import object
import re

REGEX_STRING = re.compile(r"^(\w*)$")
REGEX_REGEX = re.compile(r"^/(.*)/$")
REGEX_LIST = re.compile(r"^{(.*)}$")
REGEX_LOGICAL = re.compile(r"(\(.*\))$")
REGEX_BETWEEN = re.compile(r"\[(?P<attr1>\w*)\] >=? (?P<min>\d*\.?\d*) AND \[(?P<attr2>\w*)\] <=? (?P<max>\d*\.?\d*)", re.I)
REGEX_CONCAT_ATTR = re.compile(r"((\[\w*\])(?:\s*)){2,}")
REGEX_CONCAT_STR = re.compile(r"^['|\"]+.*['|\"]+$|tostring\(.*")
REGEX_FX_TOSTRING = re.compile(r"tostring(\(\[\w*\]),\s?[\'|\"]{1}\%\.(\d)f[\'|\"]{1}\)")
#REGEX_FX_UPPER = re.compile(r"upper\('?\"?\[\w*\]'?\"?\)")
#REGEX_FX_LOWER = re.compile(r"lower\('?\"?\[\w*\]'?\"?\)")
REGEX_FX_INITCAP = re.compile(r"(initcap|firscap)(\('?\"?\[\w*\]'?\"?\))") #solo fx([atribute])?
REGEX_LOGICAL_IN = re.compile(r"'?\"?(\[\w*\])'?\"?\s+in\s+\"([\w*,?]*)\"")

class Expression(object):
    TYPE_STRING = 'string'
    TYPE_REGEX = 'regexp'
    TYPE_LIST = 'list'
    TYPE_BETWEEN = 'between'
    TYPE_LOGICAL = 'logical'
    TYPE_UNKNOWN = 'unknown'

    """docstring for Expression"""
    def __init__(self, expression, has_item, text=False):
        super(Expression, self).__init__()
        self.expression = expression
        self.has_item = has_item
        self.text = text

        #self.num_decimals = 0
        #self.capitalize = []

    def type(self):
        """docstring for __getExpressionType"""
        match = REGEX_STRING.match(self.expression)
        #String comparisons
        if match:
            return (self.TYPE_STRING, match.group(1))
        #Regular expressions
        match = REGEX_REGEX.match(self.expression)
        if match:
            if self.has_item:
                return (TYPE_REGEX, self.__fixExpressionRegexp(match.group(1), self.has_item))
            return (self.TYPE_UNKNOWN, '')
        #List expressions
        match = REGEX_LIST.match(self.expression)
        if match:
            if self.has_item:
                return (self.TYPE_LIST, self.__fixExpressionList(match.group(1), self.has_item))
            return (self.TYPE_UNKNOWN, '')
        #Logical MapServer expressions
        match = REGEX_LOGICAL.search(self.expression)
        if match:
            match2 = REGEX_BETWEEN.search(self.expression)
            if match2:
                if match2["attr1"] == match2["attr2"]:
                    return (self.TYPE_BETWEEN, self.__fixExpressionLogical(self.expression, 'between'), match2["attr1"], float(match2["min"]), float(match2["max"]))
            return (self.TYPE_LOGICAL, self.__fixExpressionLogical(self.expression))
        else:
            return (self.TYPE_UNKNOWN, self.__fixExpressionLogical(self.expression, 'unknown'))

    #def decimals(self):
    #    return self.num_decimals

    #def capitalizes(self):
    #    return self.capitalize[0] if self.capitalize else False

    #--Correccion de expresiones-------------------------------------------
    def __fixExpressionRegexp(self, expression, item):
        """docstring for __fixExpressionRegexp """
        return "\"{}\" ~ '{}'".format(item, expression)

    def __fixExpressionList(self, expression, item):
        """docstring for __fixExpressionList"""
        #join( map(str.strip, expression.split(',')))
        #no seria necesario porque mapserver no soporta espacios en blanco entre los valores
        return "\"{}\" IN ('{}')".format(item, "', '".join(expression.split(',')))

    def __fixAttributes(self, expression):
        """docstring for __fixAttributes"""
        return expression.replace("'[", '"').replace('"[', '"').replace("`[", '"').replace("]'", '"').replace(']"', '"').replace("]`", '"').replace("[", '"').replace("]", '"')

    def __fixOperators(self, exp):
        exp = re.sub(r"\seq\s", " = ", exp, 0, re.IGNORECASE)
        exp = re.sub(r"\s==\s", " = ", exp, 0, re.IGNORECASE)
        exp = re.sub(r"\s=\*\s", " ILIKE ", exp, 0, re.IGNORECASE)
        exp = re.sub(r"\sne\s", " != ", exp, 0, re.IGNORECASE)
        exp = re.sub(r"\slt\s", " < ", exp, 0, re.IGNORECASE)
        exp = re.sub(r"\sgt\s", " > ", exp, 0, re.IGNORECASE)
        exp = re.sub(r"\sle\s", " <= ", exp, 0, re.IGNORECASE)
        exp = re.sub(r"\sge\s", " >= ", exp, 0, re.IGNORECASE)
        #exp = re.sub(r"\s~\*\s", " ~ ", exp, 0, re.IGNORECASE)
        return exp

    def __fixExpressionTemporal(self, expression):
        """docstring for __fixExpressionTemporal"""
        return expression.replace("`", "'")

    def __fixOperationsString(self, expression):
        #String operations that return a string
        strings = expression.split(' + ')
        concat = []

        if strings:
            for st in strings:
                # concatenar [atributes]
                match = REGEX_CONCAT_ATTR.search(st)
                if match:
                    concat.extend((match.group).split(' '))
                else:
                    # solo concatenar string, no una suma
                    match = REGEX_CONCAT_STR.search(st)
                    if match:
                        concat.append(st)
        else:
            match = REGEX_CONCAT_ATTR.search(st)
            if match:
                concat.extend((match.group).split(' '))

        if concat:
            expression = "concat({})".format(",".join(concat))

        return expression

    def __fixFunctionString(self, expression):
        #Functions that return a string
        #tostring(n1, 'Format1'), upper('String1'), lower('String1'), initcap('String1'), firstcap('String1')
        match = REGEX_FX_TOSTRING.search(expression)
        if match:
            expression = expression.replace(match.group(), "format_number{}, {})".format(match.group(1), match.group(2)))
            #self.num_decimals = int(match.group(2))

        #match = REGEX_FX_UPPER.search(expression)
        #if match:
        #    self.capitalize.append('upper')

        #match = REGEX_FX_LOWER.search(expression)
        #if match:
        #    self.capitalize.append('lower')

        match = REGEX_FX_INITCAP.search(expression)
        if match:
            expression = expression.replace(match.group(), "title" + match.group(2))
            #self.capitalize.append('initcap')

        return expression

    #TODO
    def __fixExpressionLogical(self, expression, typexp='logical'):
        """docstring for __fixExpressionLogical
        Corregir para todos los tipos posibles de expresiones en mapserver a qgis"""

        if typexp == self.TYPE_BETWEEN:
            return self.__fixAttributes(expression)

        #Expresiones regexp
        #TODO Atencion: string que contenga "/" pueden ser reemplazados de manera no deseada
        expression.replace("/", "")

        #Expressions that return a logical value
        expression = self.__fixOperators(expression)

        #Expresiones -> [item] in "val1,val2,..."
        matches = REGEX_LOGICAL_IN.finditer(expression, re.IGNORECASE)
        for match in enumerate(matches):
            expression.replace(match.group(), self.__fixExpressionList(match.group(2), match.group(1)))

        #TODO Spatial expressions
        #String operations that return a string
        expression = self.__fixOperationsString(expression)
        #Functions that return a string
        expression = self.__fixFunctionString(expression)
        #TODO String functions that return a number -> length('String1')
        #TODO Arithmetic operations and functions that return a number
        #TODO Spatial functions that return a number
        #TODO Spatial functions that return a shape
        #Temporal expressions
        expression = self.__fixExpressionTemporal(expression)

        if typexp == self.TYPE_LOGICAL:
            pass

        if typexp == self.TYPE_UNKNOWN:
            pass

        return self.__fixAttributes(expression)

