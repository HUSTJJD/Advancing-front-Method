# Pointwise V18.4R4 Journal file - Fri Oct 15 09:24:28 2021

package require PWI_Glyph 4.18.4

pw::Application setUndoMaximumLevels 5
pw::Application reset
pw::Application markUndoLevel {Journal Reset}

pw::Application clearModified

pw::Application setCAESolver CGNS 2
pw::Application markUndoLevel {Set Dimension 2D}

pw::Application setCAESolver {ANSYS Fluent} 2
pw::Application markUndoLevel {Select Solver}

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic C:/Users/JJD/Desktop/project_data/dat/goe450.dat
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Import Database}

set _DB(1) [pw::DatabaseEntity getByName curve-1]
set _TMP(PW_1) [pw::Collection create]
$_TMP(PW_1) set [list $_DB(1)]
$_TMP(PW_1) do setRenderAttribute PointMode All
$_TMP(PW_1) delete
unset _TMP(PW_1)
pw::Application markUndoLevel {Modify Entity Display}

set _TMP(split_params) [list]
lappend _TMP(split_params) [lindex [$_DB(1) closestControlPoint [list 0.5 0 $_DB(1)]] 0]
lappend _TMP(split_params) [lindex [$_DB(1) closestControlPoint [list 0 0 $_DB(1)]] 0]
set _TMP(PW_1) [$_DB(1) split $_TMP(split_params)]
unset _TMP(PW_1)
unset _TMP(split_params)
pw::Application markUndoLevel Split

set _DB(2) [pw::DatabaseEntity getByName curve-1-split-1]
set _DB(3) [pw::DatabaseEntity getByName curve-1-split-2]
set _TMP(PW_1) [pw::Connector createOnDatabase -parametricConnectors Aligned -merge 0 -reject _TMP(unused) [list $_DB(2) $_DB(3)]]
unset _TMP(unused)
unset _TMP(PW_1)
pw::Application markUndoLevel {Connectors On DB Entities}

pw::Display setShowDatabase 0
set _CN(1) [pw::GridEntity getByName con-1]
set _CN(2) [pw::GridEntity getByName con-2]
set _TMP(PW_1) [pw::Collection create]
$_TMP(PW_1) set [list $_CN(1) $_CN(2)]
$_TMP(PW_1) do setDimension 100
$_TMP(PW_1) delete
unset _TMP(PW_1)
pw::CutPlane refresh
pw::Application markUndoLevel Dimension

set _TMP(PW_1) [pw::Collection create]
$_TMP(PW_1) set [list $_CN(1) $_CN(2)]
$_TMP(PW_1) do setRenderAttribute PointMode All
$_TMP(PW_1) delete
unset _TMP(PW_1)
pw::Application markUndoLevel {Modify Entity Display}

pw::Display resetView -Z
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(2) $_CN(1)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.0030000000000000001
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.0030000000000000001
  unset _TMP(PW_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Change Spacings}

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(2) $_CN(1)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.0030000000000000001
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.0030000000000000001
  unset _TMP(PW_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Change Spacings}

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(2) $_CN(1)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0
  unset _TMP(PW_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Change Spacings}

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(2) $_CN(1)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.002
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.002
  unset _TMP(PW_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Change Spacings}

pw::Display resetView -Z
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(2) $_CN(1)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.0050000000000000001
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.0050000000000000001
  unset _TMP(PW_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Change Spacings}

pw::Display resetView -Z
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]
  pw::Connector swapDistribution MRQS [list [list $_CN(1) 1] [list $_CN(2) 1]]
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel Distribute

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel Distribute

pw::Display resetView -Z
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentCircle create]
  pw::Display resetView -Z
  pw::Display resetView -Z
  $_TMP(PW_1) addPoint {-5 0 0}
  $_TMP(PW_1) addPoint {6 0 0}
  $_TMP(PW_1) setAngle 360 {0 0 1}
  set _CN(3) [pw::Connector create]
  $_CN(3) addSegment $_TMP(PW_1)
  $_CN(3) calculateDimension
  unset _TMP(PW_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Create Connector}

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentCircle create]
  $_TMP(PW_1) delete
  unset _TMP(PW_1)
$_TMP(mode_1) abort
unset _TMP(mode_1)
$_CN(3) setDimension 30
pw::CutPlane refresh
pw::Application markUndoLevel Dimension

pw::Display resetView -Z
set _TMP(PW_1) [pw::Collection create]
$_TMP(PW_1) set [list $_CN(3)]
$_TMP(PW_1) do setRenderAttribute PointMode All
$_TMP(PW_1) delete
unset _TMP(PW_1)
pw::Application markUndoLevel {Modify Entity Display}

$_CN(3) setDimension 50
pw::CutPlane refresh
pw::Application markUndoLevel Dimension

pw::Application setGridPreference Unstructured
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(edge_1) [pw::Edge create]
  $_TMP(edge_1) addConnector $_CN(3)
  $_TMP(edge_1) addConnector $_CN(3)
  $_TMP(edge_1) addConnector $_CN(3)
  $_TMP(edge_1) addConnector $_CN(3)
  $_TMP(edge_1) addConnector $_CN(3)
$_TMP(mode_1) abort
unset _TMP(mode_1)
unset _TMP(edge_1)
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(edge_1) [pw::Edge create]
  $_TMP(edge_1) addConnector $_CN(3)
  set _TMP(edge_2) [pw::Edge create]
  $_TMP(edge_2) addConnector $_CN(1)
  $_TMP(edge_2) addConnector $_CN(2)
  $_TMP(edge_2) addConnector $_CN(2)
  $_TMP(edge_2) addConnector $_CN(1)
  $_TMP(edge_2) addConnector $_CN(2)
  $_TMP(edge_2) addConnector $_CN(1)
  $_TMP(edge_2) removeLastConnector
  $_TMP(edge_2) removeLastConnector
  $_TMP(edge_2) removeLastConnector
  $_TMP(edge_2) removeLastConnector
  $_TMP(edge_2) removeLastConnector
  $_TMP(edge_2) removeLastConnector
  $_TMP(edge_2) delete
  unset _TMP(edge_2)
  set _TMP(edge_2) [pw::Edge create]
  $_TMP(edge_2) addConnector $_CN(1)
  $_TMP(edge_2) addConnector $_CN(2)
  $_TMP(edge_2) removeLastConnector
  $_TMP(edge_2) removeLastConnector
  $_TMP(edge_2) delete
  unset _TMP(edge_2)
  set _TMP(edge_2) [pw::Edge create]
  $_TMP(edge_2) addConnector $_CN(2)
  $_TMP(edge_2) addConnector $_CN(1)
  $_TMP(edge_2) reverse
  set _DM(1) [pw::DomainUnstructured create]
  $_DM(1) addEdge $_TMP(edge_1)
  $_DM(1) addEdge $_TMP(edge_2)
  unset _TMP(edge_2)
  unset _TMP(edge_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Assemble Domain}

set _TMP(mode_1) [pw::Application begin Create]
$_TMP(mode_1) abort
unset _TMP(mode_1)
pw::Display resetView -Z
pw::Display resetView -Z
pw::Display resetView -Z
set _TMP(mode_1) [pw::Application begin UnstructuredSolver [list $_DM(1)]]
  $_DM(1) setUnstructuredSolverAttribute Algorithm AdvancingFrontOrtho
  $_DM(1) setUnstructuredSolverAttribute Algorithm AdvancingFront
  $_DM(1) setUnstructuredSolverAttribute Algorithm Delaunay
  $_DM(1) setUnstructuredSolverAttribute Algorithm AdvancingFront
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel Solve

set _TMP(mode_1) [pw::Application begin UnstructuredSolver [list $_DM(1)]]
  $_TMP(mode_1) run Initialize
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Refine
  $_TMP(mode_1) run Refine
  $_TMP(mode_1) run Refine
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Refine
  $_TMP(mode_1) run Refine
  $_TMP(mode_1) run Refine
  $_TMP(mode_1) run Refine
  $_TMP(mode_1) run Refine
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Smooth
  pw::Display resetView -Z
  pw::Display resetView -Z
  $_TMP(mode_1) run Smooth
  $_TMP(mode_1) run Smooth
  set _TMP(exam_1) [pw::Examine create DomainArea]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  set _TMP(exam_1) [pw::Examine create DomainCellType]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  set _TMP(exam_1) [pw::Examine create DomainAreaRatio]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  set _TMP(exam_1) [pw::Examine create DomainAspectRatio]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  set _TMP(exam_1) [pw::Examine create DomainCellIntersection]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  set _TMP(exam_1) [pw::Examine create DomainOnDatabase]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine -excludeCellTypes [list Tet Pyramid Prism Hex]
  pw::CutPlane applyMetric {}
  pw::Display resetView -Z
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  set _TMP(exam_1) [pw::Examine create DomainAreaRatio]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  set _TMP(exam_1) [pw::Examine create DomainMinimumAngle]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  pw::CutPlane applyMetric {}
  $_TMP(mode_1) run Initialize
  set _TMP(exam_1) [pw::Examine create DomainArea]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  set _TMP(exam_1) [pw::Examine create DomainAreaRatio]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  pw::CutPlane applyMetric {}
  $_TMP(mode_1) run Refine
  set _TMP(exam_1) [pw::Examine create DomainArea]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  set _TMP(exam_1) [pw::Examine create DomainAreaRatio]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  pw::Display resetView -Z
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  pw::CutPlane applyMetric {}
  set _TMP(exam_1) [pw::Examine create DomainArea]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  pw::CutPlane applyMetric {}
  set _TMP(exam_1) [pw::Examine create DomainAspectRatio]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  pw::CutPlane applyMetric {}
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Smooth
  set _TMP(exam_1) [pw::Examine create DomainAspectRatio]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  pw::CutPlane applyMetric {}
  set _TMP(exam_1) [pw::Examine create DomainAspectRatio]
  $_TMP(exam_1) addEntity [list $_DM(1)]
  $_TMP(exam_1) examine
  pw::CutPlane applyMetric {}
  $_TMP(exam_1) delete
  unset _TMP(exam_1)
  pw::CutPlane applyMetric {}
  $_TMP(mode_1) run Smooth
  pw::Display resetView -Z
  pw::Display resetView -Z
$_TMP(mode_1) abort
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin UnstructuredSolver [list $_DM(1)]]
  $_TMP(mode_1) run Initialize
  $_TMP(mode_1) run Refine
  $_TMP(mode_1) run Decimate
  $_TMP(mode_1) run Smooth
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel Solve

set ents [list $_DM(1)]
set _TMP(mode_1) [pw::Application begin Modify $ents]
  pw::Display resetView -Z
$_TMP(mode_1) abort
unset _TMP(mode_1)

set ents [list $_DM(1)]
set _TMP(mode_1) [pw::Application begin Modify $ents]
$_TMP(mode_1) abort
unset _TMP(mode_1)

pw::Display resetView -Z
set _TMP(mode_1) [pw::Application begin GridExport [pw::Entity sort [list $_DM(1)]]]
$_TMP(mode_1) abort
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_DM(1)]]]
  $_TMP(mode_1) initialize -strict -type CAE C:/Users/JJD/Desktop/project_data/cas/in-100-out-50-front/goe450/goe450.cas
  $_TMP(mode_1) verify
  $_TMP(mode_1) write
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application save C:/Users/JJD/Desktop/project_data/cas/in-100-out-50-front/goe450/goe450.pw
pw::Application exit