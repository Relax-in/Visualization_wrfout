import vtk

def save_rectilinear_grid_vtr(grid, filename):
    # 假设 `grid` 是一个 vtkRectilinearGrid 对象，而不是 vtkStructuredGrid
    writer = vtk.vtkXMLRectilinearGridWriter()  # 使用适当的 XML 写入器
    writer.SetFileName(filename)
    writer.SetInputData(grid)
    writer.SetDataModeToBinary()  # 使用二进制模式以减少文件大小
    writer.Write()

# 示例：创建一个简单的 RectilinearGrid 供测试
def create_rectilinear_grid():
    grid = vtk.vtkRectilinearGrid()
    grid.SetDimensions(10, 10, 10)

    # 设置 X、Y、Z 方向的坐标
    xCoords = vtk.vtkFloatArray()
    yCoords = vtk.vtkFloatArray()
    zCoords = vtk.vtkFloatArray()

    for i in range(10):
        xCoords.InsertNextValue(i)
        yCoords.InsertNextValue(i)
        zCoords.InsertNextValue(i)

    grid.SetXCoordinates(xCoords)
    grid.SetYCoordinates(yCoords)
    grid.SetZCoordinates(zCoords)

    return grid

# 使用示例创建的 RectilinearGrid 测试保存
grid = create_rectilinear_grid()
save_rectilinear_grid_vtr(grid, "output.vtr")
