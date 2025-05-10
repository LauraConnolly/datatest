transform = slicer.mrmlScene.GetFirstNodeByName('TumorTransform')
ros = slicer.util.getModuleLogic('ROS2')
node = ros.GetDefaultRos2Node()
publisher = node.CreateAndAddPublisher('vtkMRMLROS2PoseNode', 'tumor_transform')

def updatetransform():
  matrix = vtk.vtkMatrix4x4()
  transform.GetMatrixTransformToParent(matrix)
  publisher.Publish(matrix)