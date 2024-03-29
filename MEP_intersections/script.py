# -*- coding: UTF-8 -*-

import os, sys
import Autodesk
from Autodesk.Revit.DB import *
import sys
from System.Collections.Generic import List
import Autodesk.Revit.DB.Transaction
import clr
clr.AddReference("RevitAPI")
clr.AddReference("ProtoGeometry")
pg = clr.AddReference("ProtoGeometry")
# Import ToProtoType, ToRevitType geometry conversion extension methods
from Autodesk.DesignScript.Geometry import *
from Autodesk.Revit.DB.HostObjectUtils import *
from Autodesk.Revit.DB.ExtensibleStorage import *
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc =  DocumentManager.Instance.CurrentDBDocument
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

import math
#print((pg))
#doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
curview = uidoc.ActiveGraphicalView
__doc__ = 'hole'
__author__ = 'Herashchanka Max'
distanceByJoin = 200
UNIT_CONVERT = 304.8005
from Autodesk.Revit.Creation import *

# project data
all_ducts = list(FilteredElementCollector(doc). \
    OfClass(Autodesk.Revit.DB.Mechanical.Duct). \
    ToElements())



all_flex_ducts = list(FilteredElementCollector(doc). \
    OfClass(Autodesk.Revit.DB.Mechanical.FlexDuct). \
    ToElements())

all_pipes = list(FilteredElementCollector(doc). \
    OfClass(Autodesk.Revit.DB.Plumbing.Pipe). \
    ToElements())

all_roofs = list(FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Roofs). \
    WhereElementIsNotElementType().ToElements())

all_walls =list(FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Walls). \
    WhereElementIsNotElementType().ToElements())

all_floors = list(FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Floors). \
    WhereElementIsNotElementType().ToElements())

all_curtain_panel = list(FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_CurtainWallPanels). \
    WhereElementIsNotElementType().ToElements())

all_ducts_terminals = list(FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_DuctTerminal). \
    WhereElementIsNotElementType().ToElements())



all_family_sybols= list(FilteredElementCollector(doc). \
    OfClass(FamilySymbol). \
    ToElements())

all_levels = list(FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Levels). \
    WhereElementIsNotElementType().ToElements())


#all_engineering_elements = all_ducts + all_flex_ducts +all_ducts_terminals+ all_pipes
all_bases =  all_curtain_panel + all_walls + all_floors + all_roofs

options = Options()
options.ComputeReferences=True
options2 = Options()
options2.ComputeReferences=False

import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')


import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *


class MainForm(Form):
    def __init__(self):
        self.InitializeComponent()

    def InitializeComponent(self):
        self._checkBox1 = System.Windows.Forms.CheckBox()
        self._checkBox2 = System.Windows.Forms.CheckBox()
        self._Cancelbutton = System.Windows.Forms.Button()
        self._Applybutton = System.Windows.Forms.Button()
        self._groupBox1 = System.Windows.Forms.GroupBox()
        self._groupBox1.SuspendLayout()
        self.SuspendLayout()
        #
        # checkBox1
        #
        #self._checkBox1.Checked = True
        self._checkBox1.CheckState = System.Windows.Forms.CheckState.Checked
        self._checkBox1.Location = System.Drawing.Point(6, 27)
        self._checkBox1.Name = "checkBox1"
        self._checkBox1.Size = System.Drawing.Size(150, 24)
        self._checkBox1.TabIndex = 2
        self._checkBox1.Text = "Воздуховоды"
        self._checkBox1.UseVisualStyleBackColor = True
        self._checkBox1.CheckedChanged += self.CheckBox1CheckedChanged
        #
        # checkBox2
        #
        self._checkBox2.Location = System.Drawing.Point(6, 70)
        self._checkBox2.Name = "checkBox2"
        self._checkBox2.Size = System.Drawing.Size(104, 24)
        self._checkBox2.TabIndex = 3
        self._checkBox2.Text = "Трубы"
        self._checkBox2.UseVisualStyleBackColor = True
        self._checkBox2.CheckedChanged += self.CheckBox2CheckedChanged
        #
        # Cancelbutton
        #
        self._Cancelbutton.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center
        self._Cancelbutton.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._Cancelbutton.Font = System.Drawing.Font("ISOCPEUR", 8, System.Drawing.FontStyle.Italic,
                                                      System.Drawing.GraphicsUnit.Point, 204)
        self._Cancelbutton.Location = System.Drawing.Point(203, 218)
        self._Cancelbutton.Name = "Cancelbutton"
        self._Cancelbutton.Size = System.Drawing.Size(75, 25)
        self._Cancelbutton.TabIndex = 4
        self._Cancelbutton.Text = "Cancel"
        self._Cancelbutton.UseVisualStyleBackColor = True
        self._Cancelbutton.MouseClick += self.CancelbuttonClick
        #
        # Applybutton
        #
        self._Applybutton.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center
        self._Applybutton.DialogResult = System.Windows.Forms.DialogResult.OK
        self._Applybutton.Font = System.Drawing.Font("ISOCPEUR", 8, System.Drawing.FontStyle.Italic,
                                                     System.Drawing.GraphicsUnit.Point, 204)
        self._Applybutton.Location = System.Drawing.Point(122, 218)
        self._Applybutton.Name = "Applybutton"
        self._Applybutton.Size = System.Drawing.Size(75, 25)
        self._Applybutton.TabIndex = 5
        self._Applybutton.Text = "Ok"
        self._Applybutton.UseVisualStyleBackColor = True
        self._Applybutton.Click += self.ApplybuttonClick
        #
        # groupBox1
        #
        self._groupBox1.Controls.Add(self._checkBox1)
        self._groupBox1.Controls.Add(self._checkBox2)
        self._groupBox1.Location = System.Drawing.Point(13, 37)
        self._groupBox1.Name = "groupBox1"
        self._groupBox1.Size = System.Drawing.Size(200, 100)
        self._groupBox1.TabIndex = 6
        self._groupBox1.TabStop = False
        self._groupBox1.Text = "Категории"
        #
        # MainForm
        #
        self.AcceptButton = self._Applybutton
        self.CancelButton = self._Cancelbutton
        self.ClientSize = System.Drawing.Size(282, 253)
        self.Controls.Add(self._groupBox1)
        self.Controls.Add(self._Applybutton)
        self.Controls.Add(self._Cancelbutton)
        self.Font = System.Drawing.Font("ISOCPEUR", 10.2, System.Drawing.FontStyle.Italic,
                                        System.Drawing.GraphicsUnit.Point, 204)
        self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
        self.KeyPreview = True
        self.Name = "MainForm"
        self.Text = "intersectsForm"
        self.Load += self.MainFormLoad
        self._groupBox1.ResumeLayout(False)
        self.ResumeLayout(False)

    def CheckBox1CheckedChanged(self, sender, e):
        pass

    def CheckBox2CheckedChanged(self, sender, e):
        pass

    def MainFormLoad(self, sender, e):

        pass

    def CancelbuttonClick(self, sender, e):
        self.value1 = '00'
        self.Close()

    def ApplybuttonClick(self, sender, e):
        self.value1 = '00'
        if self._checkBox1.Checked and self._checkBox2.Checked:
            self.value1 = '11'
        elif self._checkBox1.Checked:
            self.value1 = '10'
        elif self._checkBox2.Checked:
            self.value1 = '01'
        else:
            self.value1 = '00'
        self.Close()

form = MainForm()
Application.Run(form)
Application.EnableVisualStyles()



try:
    form_return = form.value1
    if form_return == '11':
        all_engineering_elements = all_ducts + all_flex_ducts + all_pipes
    elif form_return == '10':
        all_engineering_elements = all_ducts + all_flex_ducts
    elif form_return == '01':
        all_engineering_elements =  all_pipes
    else:
        all_engineering_elements = []
except:
    form_return = '00'
    all_engineering_elements = []
all_bases = all_curtain_panel + all_walls + all_floors + all_roofs



#Get Family symbol for hole
for familySymbol in all_family_sybols:
    if familySymbol.FamilyName == 'The hole':
        familyName = familySymbol

    elif familySymbol.FamilyName == 'The hole2':
        familyName2 = familySymbol



#print(familyName)
av = doc.ActiveView

def GetBoundingBoxCenterPoint(solid, vec):
    """ this function get center point of bounding box
    build line between min and max point and get
    his center point
    """
    #print(dir(solid.BoundingBox))
    boundinBoxMinPoint = solid.BoundingBox.MinPoint
    boundinBoxMaxPoint = solid.BoundingBox.MaxPoint

    x1 = boundinBoxMinPoint.X
    y1 = boundinBoxMinPoint.Y
    z1 = boundinBoxMinPoint.Z

    x2 = boundinBoxMaxPoint.X
    y2 = boundinBoxMaxPoint.Y
    z2 = boundinBoxMaxPoint.Z
    #print(boundinBoxMinPoint, boundinBoxMaxPoint )
    if vec.ToVector().IsParallel(XYZ(0, 1, 0).ToVector()):

        a = (x2-x1+100)/UNIT_CONVERT
        b = (z2-z1+100)/UNIT_CONVERT
        t = (y2-y1)/UNIT_CONVERT
    elif vec.ToVector().IsParallel(XYZ(1, 0, 0).ToVector()):
        a = (y2 - y1 + 100) / UNIT_CONVERT
        b = (z2 - z1 + 100) / UNIT_CONVERT
        t = (x2 - x1) / UNIT_CONVERT
    else:
        a = (x2 - x1 + 100) / UNIT_CONVERT
        b = (y2 - y1 + 100) / UNIT_CONVERT
        t = (z2 - z1) / UNIT_CONVERT

    line = Autodesk.DesignScript.Geometry.Line.ByStartPointEndPoint(boundinBoxMinPoint, boundinBoxMaxPoint)

    centerPoint = line.PointAtParameter(0.5)
    return centerPoint, a, b, t

def UnionTwoBoundingBoxes(firstBoundingBox, secondBoundingBox):
    """
    this function unions two bounding box.
    it find min and max point. they are the corner points

             __________max1    ____________ max2
            |          |      |            |
            |          |      |            |
       min1|__________|  min2|____________|
    :param firstBoundingBox:
    :param secondBoundingBox:
    :return: boundingBox
    """

    firstMinPoint = firstBoundingBox.MinPoint
    firstMaxPoint =  firstBoundingBox.MaxPoint
    secondMinPoint = secondBoundingBox.MinPoint
    secondMaxPoint = secondBoundingBox.MaxPoint
    if firstMinPoint.DistanceTo(secondMaxPoint) > secondMinPoint.DistanceTo(firstMaxPoint):
        boundingMaxPoint = secondMaxPoint
        boundingMinPoint = firstMinPoint
    else:
        boundingMaxPoint = firstMaxPoint
        boundingMinPoint = secondMinPoint

    return Autodesk.DesignScript.Geometry.BoundingBox.ByCorners(boundingMinPoint, boundingMaxPoint)

def JoinIntersectionSolid(boundingBoxes):
    distance = 0
    i=0
    while i < len(boundingBoxes):
        counter = len(boundingBoxes)
        j = i + 1
        while j<len(boundingBoxes) or j < counter:
                if boundingBoxes[i].DistanceTo(boundingBoxes[j])<=200:
                    boundingBoxes[i] = boundingBoxes[i].Union(boundingBoxes[j])
                    #distance = boundingBoxes[i].DistanceTo(boundingBoxes[j])
                    boundingBoxes.pop(boundingBoxes.index(boundingBoxes[j]))
                    j += 1
                    counter -=1
                else:
                    j += 1
        i+=1
    return boundingBoxes
def InsertFamilyInstance(familySymbols, baseInformation):

    for familyName in familySymbols:
        if familyName.IsActive == False:
            familyName.Activate()
        else:
            pass

    if baseInformation[3].ToString() != 'Autodesk.Revit.DB.Panel' and baseInformation[3].ToString() != 'Autodesk.Revit.DB.FootPrintRoof':
        instance = doc.Create.NewFamilyInstance(face=baseInformation[2], \
                                                location=BoxCenterPoint.ToRevitType(), \
                                                referenceDirection=baseInformation[1].GetPerpendicular(), \
                                                symbol=familySymbols[0])
        ref = 'face'
    else:
        st = Autodesk.Revit.DB.Structure.StructuralType()
        instance = doc.Create.NewFamilyInstance(location=BoxCenterPoint.ToRevitType(), \
                                                symbol=familySymbols[1], \
                                                level=all_levels[0], \
                                                structuralType=st.NonStructural)
        ref = 'point'
    return instance, ref
##Getting reference geo

panels_dict = {}

#Поулчение геометрии стен. Для витражей отбрасывается сама стена-витраж, т.к. для нее нет геометрии, обрабатываются панели. Все панели одного виража объединяются в один солид

if len(all_engineering_elements)>0:
    new_X = []
    new_Y = []
    new_Z = []
    for base in all_bases:
        print(" ")
        #print(dir(base))
        try:#Отбрасывает витражи, оставляет панели и обычные стены
            if base.CurtainGrid.ToString() == 'Autodesk.Revit.DB.CurtainGrid':
                #all_bases.remove(base)
                if base == all_bases[-1]:
                    for panel in panels_dict.values():
                        if panel[1].ToVector().IsParallel(XYZ(1, 0, 0).ToVector()):
                            new_X.append(panel)
                        elif panel[1].ToVector().IsParallel(XYZ(0, 1, 0).ToVector()):
                            new_Y.append(panel)
                        elif panel[1].ToVector().IsParallel(XYZ(0, 0, 1).ToVector()):
                            new_Z.append(panel)
                # Если последний элемент из списка, то добавить в общий список
                continue
        except:
            print(" ")
            pass
        try:
            Volume_base = list(base.GetGeometryObjectFromReference(Reference(base)).GetEnumerator())[0].Volume
        except:
            try:
                Volume_base =list(list(base.GetGeometryObjectFromReference(Reference(base)).GetEnumerator())[0].GetInstanceGeometry().GetEnumerator())[0].Volume
            except:
                print("Somthing went wrong..212", base.Id)
                #continue
                pass
        print(" ")
        if Volume_base>0:#Для исключения элементов с нулевыи объемом
            try:
                reference_vector = base.Orientation.ToVector().ToRevitType()
                ref_geo = list(base.get_Geometry(options).GetEnumerator())[0]
            except:
                try:
                    reference_vector = base.FacingOrientation.ToVector().ToRevitType()
                    ref_geo = list(list(base.get_Geometry(options).GetEnumerator())[0].GetInstanceGeometry().GetEnumerator())[0]
                except:
                    reference_vector = XYZ(0, 0, 1)
                    ref_geo = list(base.get_Geometry(options).GetEnumerator())[0]

            if reference_vector.X == -1:
                reference_vector= reference_vector.Negate()
            if reference_vector.Y == -1:
                reference_vector= reference_vector.Negate()

            print(" ")
            try:# Получает геометрию и вектор для панелей и добавлет в список
                host_id = base.Host.Id.ToString()
                if host_id not in panels_dict.keys():

                    panels_dict[host_id] = [ref_geo.ToProtoType(),reference_vector,0, base]
                else:
                    panels_dict[host_id][0] = panels_dict[host_id][0].Union(ref_geo.ToProtoType())
            except:
                print(" ")
                # Поулчает геометрию для стен и длобавляет в список
                try:
                    area = 0
                    for face in ref_geo.Faces:
                        #print(1234)
                        if face.Area > area:
                            area = face.Area
                            reference_face = face
                except:
                    print(" ")
                    #print('Somthing went wrong..244:', base.Id.ToString())
                    continue

                if reference_vector.ToVector().IsParallel(XYZ(1, 0, 0).ToVector()):
                    new_X.append([ref_geo.Convert(), reference_vector, reference_face, base])
                elif reference_vector.ToVector().IsParallel(XYZ(0, 1, 0).ToVector()):
                    new_Y.append([ref_geo.Convert(), reference_vector, reference_face, base])
                else:
                    new_Z.append([ref_geo.Convert(), reference_vector, reference_face, base])
                #elif reference_vector.ToVector().IsParallel(XYZ(0, 0, 1).ToVector()):
                #    new_Z.append([ref_geo.Convert(), reference_vector, reference_face, base])
            # Если последний элемент из списка, то добавить в общий список
            if base == all_bases[-1]:
                for panel in panels_dict.values():
                    if panel[1].ToVector().IsParallel(XYZ(1, 0, 0).ToVector()):
                        new_X.append(panel)
                    elif panel[1].ToVector().IsParallel(XYZ(0, 1, 0).ToVector()):
                        new_Y.append(panel)
                    elif panel[1].ToVector().IsParallel(XYZ(0, 0, 1).ToVector()):
                        new_Z.append(panel)

    new ={XYZ(1, 0, 0).ToVector() : new_X, XYZ(0, 1, 0).ToVector():new_Y,  XYZ(0, 0, 1).ToVector():new_Z}


    intersection_solids = []
    t = Transaction(doc, 'search intersetions')
    t.Start()
    for engineering_element in all_engineering_elements:
        print(" ")

        try:
            curve = engineering_element.Location.Curve.Direction.ToVector()
            eng_geo = list(engineering_element.get_Geometry(options2).GetEnumerator())[0]
        except:
            try:
                enga = list(list(engineering_element.get_Geometry(options2))[0].GetSymbolGeometry())[0]
                eng_geo = enga.ToProtoType()
                curve = 0
            except:
                print('somthing went wrong with element id:', engineering_element.Id)
                continue
        if curve != 0:
            if curve.IsParallel(new.keys()[0]):
                for base in new[XYZ(0,1,0).ToVector()]:
                    print(" ")
                    base_DS = base[0]
                    try:
                        if base_DS.Intersect(eng_geo.ToProtoType()):
                            solid = base_DS.Intersect(eng_geo.ToProtoType())[0]
                            if len(base)==4:
                                base.append([solid])
                            else:
                                base[4].append(solid)
                    except:
                        pass
            elif curve.IsParallel(new.keys()[1]):
                for base in new[XYZ(1, 0, 0).ToVector()]:
                    print(" ")
                    base_DS = base[0]
                    try:
                        if base_DS.Intersect(eng_geo.ToProtoType()):
                            solid = base_DS.Intersect(eng_geo.ToProtoType())[0]
                            if len(base) == 4:
                                base.append([solid])
                            else:
                                base[4].append(solid)

                    except:
                        pass
            #elif curve.IsParallel(new.keys()[2]):
            else:
                for base in new[XYZ(0, 0, 1).ToVector()]:
                    print(" ")
                    base_DS = base[0]
                    try:
                        if base_DS.Intersect(eng_geo.ToProtoType()):
                            solid = base_DS.Intersect(eng_geo.ToProtoType())[0]
                            if len(base) == 4:
                                base.append([solid])
                            else:
                                base[4].append(solid)
                    except:
                        pass

    #### Проверка есть л, рядом боксы, если есть т, их объединение
    for base in new.values():
        try:
            for solids in base:
                print(" ")
                #print(solids[4])
                solids[4] = JoinIntersectionSolid(solids[4])
        except:
            pass
    #### объдениненные солиды пересечения в словарь к основе

    #### structure for new [solid, vector, face, base, curve  [intersectioos solids]]
    angle = 90
    counter = 0

    for direction in new.values():
        for inf in direction:
            #print(inf)
            try:
                for box in inf[-1]:
                    print(" ")
                    intersection_points = []
                    BoxCenterPoint,a, b, thinknes = GetBoundingBoxCenterPoint(box, inf[1])
                    instance, ref = InsertFamilyInstance([familyName, familyName2],inf)
                    if inf[1][0]==1 and ref =='point':
                        p2 = XYZ(BoxCenterPoint.X / UNIT_CONVERT, BoxCenterPoint.Y / UNIT_CONVERT, (BoxCenterPoint.Z + 100) /UNIT_CONVERT)
                        axis = Line.ByStartPointEndPoint(p2.ToPoint(), BoxCenterPoint).ToRevitType()
                        #axis = Line.ByStartPointEndPoint(p2.ToPoint(), BoxCenterPoint).ToRevitType()
                        instance.Location.Rotate(axis, 1.570796)
                    instance.LookupParameter('a').Set(a)
                    instance.LookupParameter('b').Set(b)
                    instance.LookupParameter('t').Set(thinknes)
                    counter+=1
            except:
                pass
    t.Commit()

    print('Успешно создано {0} проем'.format(counter))
