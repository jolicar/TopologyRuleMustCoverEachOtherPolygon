# encoding: utf-8

import gvsig
import sys

from gvsig import uselib
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.fmap.geom import Geometry
from org.gvsig.tools.util import ListBuilder
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.spi import AbstractTopologyRuleFactory, RuleResourceLoaderUtils

from java.io import File

from mustCoverEachOtherPolygonRule import MustCoverEachOtherPolygonRule

class MustCoverEachOtherPolygonRuleFactory(AbstractTopologyRuleFactory):
      
    def __init__(self):
        AbstractTopologyRuleFactory.__init__(
            self,
            "MustCoverEachOtherPolygon",
            "Must Cover Each Other Polygon Rule GSoC2020",
            "The rule evaluates all the polygons. All dataset 2 polygon areas must cover the dataset 1 polygon area. The rule returns False when a part of the dataset 1 polygon area is not covered or not completely covered. In 2DM, 3D and 3DM formats, the Z coordinate or M coordinate are ignored.\n \n NOTE 1: The Tolerance parameter is useless for this rule.",
            ListBuilder().add(Geometry.TYPES.POLYGON).add(Geometry.TYPES.MULTIPOLYGON).asList(),
            ListBuilder().add(Geometry.TYPES.POLYGON).add(Geometry.TYPES.MULTIPOLYGON).asList()
        )

        pathName = gvsig.getResource(__file__,'MustCoverEachOtherPolygon.json')
        url = File(pathName).toURL()
        gvsig.logger(str(url))
        json = RuleResourceLoaderUtils.getRule(url)
        self.load_from_resource(url, json)
    
    def createRule(self, plan, dataSet1, dataSet2, tolerance):
        rule = MustCoverEachOtherPolygonRule(plan, self, tolerance, dataSet1, dataSet2)
        return rule

def selfRegister():
    try:
        manager = TopologyLocator.getTopologyManager()
        manager.addRuleFactories(MustCoverEachOtherPolygonRuleFactory())
    except:
        ex = sys.exc_info()[1]
        gvsig.logger("Can't register rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass