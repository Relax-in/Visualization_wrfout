import numpy as np
import vtk

def create_custom_structured_grid(nx, ny, nz):
    # 创建一个结构化网格
    structured_grid = vtk.vtkStructuredGrid()
    structured_grid.SetDimensions(nx, ny, nz)

    # 创建点数据
    points = vtk.vtkPoints()
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                x = i * 1.0  # x 坐标均匀分布
                y = j * 1.0  # y 坐标均匀分布

                z = np.random.uniform(k-0.3, k+0.2)



                points.InsertNextPoint(x, y, z)

    # 将点数据添加到结构化网格
    structured_grid.SetPoints(points)

    # 创建一个示例标量数据数组
    scalar_data = vtk.vtkDoubleArray()
    scalar_data.SetName("ScalarData")
    scalar_data.SetNumberOfComponents(1)
    scalar_data.SetNumberOfTuples(nx * ny * nz)

    # 生成一些示例数据
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                idx = k * ny * nx + j * nx + i
                scalar_data.SetValue(idx, np.random.uniform(0, 5))

    # 将标量数据添加到结构化网格
    structured_grid.GetPointData().SetScalars(scalar_data)

    return structured_grid

def save_structured_grid_vtk(grid, filename):
    writer = vtk.vtkStructuredGridWriter()
    writer.SetFileName(filename)
    writer.SetInputData(grid)
    writer.Write()

# 网格维度
nx, ny, nz = 30, 30, 30

# 创建结构化网格
grid = create_custom_structured_grid(nx, ny, nz)

# 保存为VTK文件
save_structured_grid_vtk(grid, "custom_structured_grid.vtk")