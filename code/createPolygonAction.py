# encoding: utf-8

import gvsig
import sys

from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction
from org.gvsig.fmap.geom import GeometryLocator
from gvsig import geom

class CreatePolygonAction(AbstractTopologyRuleAction):
    
    def __init__(self):
        AbstractTopologyRuleAction.__init__(
            self,
            "MustCoverEachOtherPolygon",
            "CreatePolygonAction",
            "Create Polygon Action",
            "This action creates a new dataset 1 feature on not overlapping part."
        )
    
    def execute(self, rule, line, parameters):
      try:
        dataSet1 = rule.getDataSet1()
        dataSet2 = rule.getDataSet2()

        store1=dataSet1.getFeatureStore()
        store2=dataSet2.getFeatureStore()

        geomEr=line.getError()

        if line.getFeature1()!=None:
          newFeature=store2.createNewFeature()
          newFeature.setDefaultGeometry(geomEr)
          dataSet2.insert(newFeature)

        if line.getFeature2()!=None:
          newFeature=store1.createNewFeature()
          newFeature.setDefaultGeometry(geomEr)
          dataSet1.insert(newFeature)

      except:
        ex = sys.exc_info()[1]
        gvsig.logger("Can't execute action. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass