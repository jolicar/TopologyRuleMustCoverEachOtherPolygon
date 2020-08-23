# encoding: utf-8

import gvsig
import sys

from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction

class DeletePolygonAction(AbstractTopologyRuleAction):
    
    def __init__(self):
        AbstractTopologyRuleAction.__init__(
            self,
            "mustCoverEachOtherPolygon",
            "DeletePolygonAction",
            "Delete Polygon Action",
            "The delete action removes polygon features for cases when Must Cover Each Other Polygon Topology Rule is false. The rule evaluates all the polygons. All dataset 2 polygon areas must cover the dataset 1 polygon area. The rule returns False when a part of the dataset 1 polygon area is not covered or not completely covered."
        )
    
    def execute(self, rule, line, parameters):
        try:
            dataSet1 = rule.getDataSet1()
            dataSet2 = rule.getDataSet2()
            if line.getFeature1()!=None:
              dataSet1.delete(line.getFeature1())
            if line.getFeature2()!=None:
              dataSet2.delete(line.getFeature2())
        except:
            ex = sys.exc_info()[1]
            gvsig.logger("Can't execute action. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass