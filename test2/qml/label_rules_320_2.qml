<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingTol="1" readOnly="0" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" version="3.2.1-Bonn" labelsEnabled="1" simplifyDrawingHints="1" minScale="0" maxScale="0" simplifyMaxScale="1">
  <renderer-v2 type="singleSymbol" enableorderby="0" symbollevels="0" forceraster="0">
    <symbols>
      <symbol clip_to_extent="1" name="0" type="fill" alpha="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="128,90,255,255" k="color"/>
          <prop v="round" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="25,12,128,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.529167" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="" description="test1">
      <rule key="">
        <settings>
          <text-style fontCapitals="0" fieldName="COUNTRY" previewBkgrdColor="#ffffff" fontWordSpacing="0" fontSize="11.25" textColor="220,20,20,255" fontSizeMapUnitScale="3x:0,0,0,0,0,0" namedStyle="Normal" fontSizeUnit="Point" textOpacity="1" fontStrikeout="0" isExpression="0" useSubstitutions="0" multilineHeight="1" blendMode="0" fontItalic="0" fontWeight="50" fontUnderline="0" fontFamily="MS Shell Dlg 2" fontLetterSpacing="0">
            <text-buffer bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferNoFill="0" bufferSize="1" bufferSizeUnits="MM" bufferDraw="1" bufferColor="255,255,255,255" bufferJoinStyle="64"/>
            <background shapeRotation="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="MM" shapeBorderColor="128,128,128,255" shapeOpacity="1" shapeSizeY="0" shapeRadiiY="0" shapeJoinStyle="64" shapeOffsetY="0" shapeRotationType="0" shapeBorderWidth="0" shapeType="0" shapeSizeType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeRadiiX="0" shapeSizeUnit="MM" shapeBorderWidthUnit="MM" shapeFillColor="255,255,255,255" shapeDraw="1" shapeSizeX="0" shapeOffsetX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM"/>
            <shadow shadowOffsetGlobal="1" shadowDraw="1" shadowOffsetUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowBlendMode="6" shadowOffsetAngle="135" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0" shadowOffsetDist="1" shadowColor="0,0,0,255" shadowUnder="0" shadowRadius="1.5" shadowScale="100"/>
            <substitutions/>
          </text-style>
          <text-format wrapChar="" reverseDirectionSymbol="0" multilineAlign="1" addDirectionSymbol="0" placeDirectionSymbol="0" plussign="0" leftDirectionSymbol="&lt;" decimals="3" rightDirectionSymbol=">" formatNumbers="0"/>
          <placement quadOffset="3" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" maxCurvedCharAngleOut="-20" distMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" maxCurvedCharAngleIn="20" priority="5" offsetUnits="MM" preserveRotation="1" fitInPolygonOnly="1" dist="0" distUnits="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetType="0" centroidInside="0" repeatDistance="0" yOffset="0" centroidWhole="0" repeatDistanceUnits="MM" placement="1" placementFlags="10" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" xOffset="0"/>
          <rendering fontLimitPixelSize="1" scaleMin="1" mergeLines="0" obstacleFactor="1" upsidedownLabels="0" fontMinPixelSize="4" scaleVisibility="1" maxNumLabels="2000" obstacleType="0" limitNumLabels="0" zIndex="0" minFeatureSize="0" obstacle="1" labelPerPart="0" drawLabels="1" scaleMax="10000000" displayAll="0" fontMaxPixelSize="256"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="BufferColor" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="field" value="" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="BufferSize" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="COUNTRY" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="CentroidWhole" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="COUNTRY" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="Color" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="COUNTRY" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="Family" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="COUNTRY" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="FontOpacity" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="COUNTRY" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="MinimumScale" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="COUNTRY" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="Rotation" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="field" value="" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="ShadowOffsetAngle" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="COUNTRY" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="ShapeBorderColor" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="COUNTRY" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="ShapeBorderWidth" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="field" value="" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="ShapeFillColor" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="field" value="" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
                <Option name="Size" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="field" value="COUNTRY" type="QString"/>
                  <Option name="type" value="2" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="layer"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory rotationOffset="270" labelPlacementMethod="XHeight" backgroundAlpha="255" lineSizeType="MM" penColor="#000000" width="15" penWidth="0" scaleBasedVisibility="0" backgroundColor="#ffffff" barWidth="5" minimumSize="0" opacity="1" minScaleDenominator="0" diagramOrientation="Up" lineSizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="0" sizeScale="3x:0,0,0,0,0,0" enabled="0" scaleDependency="Area" penAlpha="255" height="15" sizeType="MM">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" showAll="1" placement="1" priority="0" zIndex="0" dist="0" obstacle="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="COUNTRY">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="COUNTRY"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="COUNTRY"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="COUNTRY" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="COUNTRY"/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column name="COUNTRY" type="field" width="-1" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
    </columns>
  </attributetableconfig>
  <editform></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- codificación: utf-8 -*-
"""
Los formularios de QGIS pueden tener una función de Python que
es llamada cuando se abre el formulario.

Use esta función para añadir lógica extra a sus formularios.

Introduzca el nombre de la función en el campo
"Python Init function".
Sigue un ejemplo:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="COUNTRY"/>
  </editable>
  <labelOnTop>
    <field name="COUNTRY" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>COUNTRY</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
