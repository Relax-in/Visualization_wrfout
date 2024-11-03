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
                z = np.random.uniform(k - 0.3, k + 0.2)
                points.InsertNextPoint(x, y, z)

    # 将点数据添加到结构化网格
    structured_grid.SetPoints(points)
    return structured_grid

def add_scalar_data_to_grid(grid, data_array, scalar_name):
    """
    将标量数据添加到结构化网格的 PointData 中。

    参数：
    - grid: vtkStructuredGrid 对象，目标网格
    - data_array: 三维 numpy 数组，形状为 (nx, ny, nz)
    - scalar_name: str，标量数据的名称
    """
    nx, ny, nz = data_array.shape

    # 创建标量数据数组
    scalar_data = vtk.vtkDoubleArray()
    scalar_data.SetName(scalar_name)
    scalar_data.SetNumberOfComponents(1)
    scalar_data.SetNumberOfTuples(nx * ny * nz)

    # 将 numpy 数据写入 vtk 标量数据数组
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                idx = k * ny * nx + j * nx + i
                scalar_data.SetValue(idx, data_array[i, j, k])

    # 将标量数据添加到网格
    grid.GetPointData().AddArray(scalar_data)

    # 如果是第一个标量数组，将其设为默认标量数据
    if grid.GetPointData().GetScalars() is None:
        grid.GetPointData().SetScalars(scalar_data)

def save_structured_grid_vtk(grid, filename):
    writer = vtk.vtkStructuredGridWriter()
    writer.SetFileName(filename)
    writer.SetInputData(grid)
    writer.Write()

# 网格维度
nx, ny, nz = 30, 30, 30

# 创建结构化网格
grid = create_custom_structured_grid(nx, ny, nz)

# 生成两个示例标量数据数组
data1 = np.random.uniform(0, 5, (nx, ny, nz))
data2 = np.random.uniform(5, 10, (nx, ny, nz))

# 将标量数据添加到结构化网格
add_scalar_data_to_grid(grid, data1, "ScalarData1")
add_scalar_data_to_grid(grid, data2, "ScalarData2")

# 保存为 VTK 文件
save_structured_grid_vtk(grid, "custom_structured_grid.vtk")
