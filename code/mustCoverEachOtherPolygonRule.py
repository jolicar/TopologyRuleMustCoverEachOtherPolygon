# encoding: utf-8

import gvsig
import sys

from gvsig import geom
from gvsig import uselib #para cargar plugins, scripting no tiene cargados todos los plugins
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.expressionevaluator import GeometryExpressionEvaluatorLocator, ExpressionEvaluatorLocator
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.spi import AbstractTopologyRule
from org.gvsig.fmap.geom import GeometryLocator

from org.gvsig.tools.task import SimpleTaskStatus

from deletePolygonAction import DeletePolygonAction
from createPolygonAction import CreatePolygonAction


class MustCoverEachOtherPolygonRule(AbstractTopologyRule):


  def __init__(self, plan, factory, tolerance, dataSet1, dataSet2):
      AbstractTopologyRule.__init__(self, plan, factory, tolerance, dataSet1, dataSet2)
      self.addAction(DeletePolygonAction())
      self.addAction(CreatePolygonAction())

      self.expression = ExpressionEvaluatorLocator.getManager().createExpression()
      self.expressionBuilder = GeometryExpressionEvaluatorLocator.getManager().createExpressionBuilder()
      self.geomName=None

  def getSteps(self):
      return self.getDataSet1().getSize()+self.getDataSet2().getSize()

  def execute(self, taskStatus, report):
    try:
      dataSet1 = self.getDataSet1()
      dataSet2 = self.getDataSet2()
      
      store1=dataSet1.getFeatureStore()
      store2=dataSet2.getFeatureStore()

      if store1.getSRSDefaultGeometry()==store2.getSRSDefaultGeometry():
        AbstractTopologyRule.execute(self, taskStatus, report)
      else:
        report.addLine(self,
          self.getDataSet1(),
          self.getDataSet2(),
          None,
          None,
          None,
          None,
          -1,
          -1,
          False,
          "Can't execute rule. The two datasets cant have a different projection.",
          ""
        )

      features1=store1.getFeatures()
      features2=store2.getFeatures()

      candidateEr1List=[]
      candidateEr2List=[]
      er1ListAux=[]
      er2ListAux=[]

      for feature1 in features1:
        taskStatus.incrementCurrentValue()
        feature1M=convert2D(self, feature1, report)
        checkIntersects=False

        for feature2 in features2:
          feature2M=convert2D(self, feature2, report)
          if feature1M.intersects(feature2M):
            candidateEr1=feature2M.difference(feature1M)
            checkIntersects=True
            if candidateEr1!=None:
              candidateEr1Dic={}
              candidateEr1Dic["geom"]=candidateEr1
              candidateEr1Dic["ref"]=feature2.getReference()
              candidateEr1List.append(candidateEr1Dic)
        if checkIntersects==False:
          candidateEr1Dic={}
          candidateEr1Dic["geom"]=feature1.getDefaultGeometry()
          candidateEr1Dic["ref"]=feature1.getReference()
          er1ListAux.append(candidateEr1Dic)

      for dic in candidateEr1List:
        for feature1 in features1:
          feature1M=convert2D(self, feature1, report)
          if dic["geom"] == None:
            continue
          if dic["geom"].intersects(feature1M):
            dic["geom"]=dic["geom"].difference(feature1M)

      er1List=[]
      for dic in candidateEr1List:
        if dic not in er1List:
          er1List.append(dic)

      er1List+=er2ListAux

      for dic in er1List: 
        if dic["geom"] == None:
          continue
        report.addLine(self,
          self.getDataSet1(),
          self.getDataSet2(),
          dic["ref"].getFeature().getDefaultGeometry(),
          dic["geom"],
          None,
          dic["ref"],
          -1,
          -1,
          False,
          "The dataset 1 polygons dont cover dataset 2 polygons",
          ""
        )
        

      for feature2 in features2:
        taskStatus.incrementCurrentValue()
        feature2M=convert2D(self, feature2, report)
        checkIntersects=False

        for feature1 in features1:
          feature1M=convert2D(self, feature1, report)
          if feature2M.intersects(feature1M):
            candidateEr2=feature1M.difference(feature2M)
            checkIntersects=True
            if candidateEr2!= None:
              candidateEr2Dic={}
              candidateEr2Dic["geom"]=candidateEr2
              candidateEr2Dic["ref"]=feature1.getReference()
              candidateEr2List.append(candidateEr2Dic)
        if checkIntersects==False:
          candidateEr2Dic={}
          candidateEr2Dic["geom"]=feature2.getDefaultGeometry()
          candidateEr2Dic["ref"]=feature2.getReference()
          er2ListAux.append(candidateEr2Dic)
              

      for dic in candidateEr2List:
        for feature2 in features2:
          feature2M=convert2D(self, feature2, report)
          if dic["geom"] == None:
            continue
          if dic["geom"].intersects(feature2M):
            dic["geom"]=dic["geom"].difference(feature2M)

      er2List=[]
      for dic in candidateEr2List:
        if dic not in er2List:
          er2List.append(dic)

      er2List+=er1ListAux

      for dic in er2List:
        if dic["geom"] == None:
          continue
        report.addLine(self,
          self.getDataSet1(),
          self.getDataSet2(),
          dic["ref"].getFeature().getDefaultGeometry(),
          dic["geom"],
          dic["ref"],
          None,
          -1,
          -1,
          False,
          "The dataset 2 polygons dont cover dataset 1 polygons",
          ""
        )

    except:
      ex = sys.exc_info()[1]
      gvsig.logger("Can't execute rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def convert2D(self, feature, report):
    polygon= feature.getDefaultGeometry()
    geometryType = polygon.getGeometryType()

    mustConvert2D=(not geometryType.getSubType() == geom.D2)

    proj=polygon.getProjection()
    geomManager = GeometryLocator.getGeometryManager()
    if geomManager.isSubtype(geom.POLYGON,geometryType.getType()):
      if mustConvert2D:
        polygon=polygon.force2D()
        polygon.setProjection(proj)
        return polygon
      return polygon
    elif geomManager.isSubtype(geom.MULTIPOLYGON,geometryType.getType()):
      if mustConvert2D:
        polygon=polygon.force2D()
        polygon.setProjection(proj)
        return polygon
      return polygon
    else:
      report.addLine(self,
        self.getDataSet1(),
        self.getDataSet2(),
        polygon,
        polygon,
        feature.getReference(),
        None,
        -1,
        -1,
        False,
        "Unsupported geometry type.",
        ""
    )

def main(*args):
    pass