# Must Cover Each Other Polygon Topology Rule
![TopologyRule](https://github.com/jolicar/TopologyRuleMustCoverEachOtherPolygon/blob/master/img/TP00RU04_img1.png)
* **Rule type:** *Polygon rule*
* **Primary dataset:** Polygon dataset (2D, 2DM, 3D and 3DM) (*Multygeometry allowed*)
* **Secundary dataset:** Polygon dataset (2D, 2DM, 3D and 3DM) (*Multygeometry allowed*)


* **Brief description:** The rule evaluates all the polygons. All dataset 2 polygon areas  must cover the dataset 1 polygon area and all dataset 1 polygon areas  must cover the dataset 2 polygon area too. The rule returns *False* when a part of the dataset 1 polygon area or dataset 2 polygon area is not covered or not completely covered. In 2DM, 3D and 3DM formats, the Z coordinate or M coordinate are ignored.
* **Limitations:** The two datasets cant have a different projection.
* **Rule behavior:** 
  - The Tolerance parameter is useless for this rule.
  
* **Potential fixes actions:** 
  - **Delete** The delete action removes polygon features for cases when *Must Cover Each Other Polygon* Topology Rule is false.
  - **Create feature** This action creates a new feature on not overlapping part.
* **Actions behavior:**
  - All the dataset 1 polygons must be covered by the dataset 2 polygons perfectly and all the dataset 2 polygons must be covered by the dataset 1 polygons perfectly too.

#### [*Back to GSoC2020 Project Wiki*](https://github.com/jolicar/GSoC2020/wiki/GSoC2020-New-rules-for-the-Topology-Framework-in-gvSIG-Desktop)