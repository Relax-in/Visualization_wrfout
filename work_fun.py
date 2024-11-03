import netCDF4 as nc
import numpy as np
import vtk

def create_custom_structured_grid(nx, ny, nz, height, dx, dy):
    # 创建一个结构化网格
    structured_grid = vtk.vtkStructuredGrid()
    structured_grid.SetDimensions(nx, ny, nz)

    # 创建点数据
    points = vtk.vtkPoints()
    
    print("zyx",nz,ny,nx)
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                x = i * dx  # x 坐标均匀分布
                y = j * dy  # y 坐标均匀分布
                z = height[k, j, i]
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
    nz, ny, nx = data_array.shape

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
                scalar_data.SetValue(idx, data_array[k, j, i])

    # 将标量数据添加到网格
    grid.GetPointData().AddArray(scalar_data)

    # 如果是第一个标量数组，将其设为默认标量数据
    if grid.GetPointData().GetScalars() is None:
        grid.GetPointData().SetScalars(scalar_data)


# 写出可视化文件
def save_structured_grid_vts(grid, filename):
    writer = vtk.vtkXMLStructuredGridWriter()  # 使用 XML 格式的 Structured Grid 写入器
    writer.SetFileName(filename)
    writer.SetInputData(grid)
    writer.SetDataModeToBinary()  # 二进制模式减少文件体积
    writer.Write()


# 判断要插值的维度
def if_dimension(data, x_cell_number, y_cell_number, z_cell_number):
    if data.shape[3] != x_cell_number:
        
        data = np.array(data)
        output_data = (data[:, :, :, :-1] + data[:, :, :, 1:]) / 2
        return output_data
    elif data.shape[2] != y_cell_number:
        data = np.array(data)
        output_data = (data[:, :, :-1, :] + data[:, :, 1:, :]) / 2
        return output_data
    elif data.shape[1] != z_cell_number:
        data = np.array(data)
        output_data = (data[:, :-1, :, :] + data[:, 1:, :, :]) / 2
        return output_data
    else:
        data = np.array(data)
        return data
        

# 核心函数
def run_work_1(file_name, output_variables, dx, dy, file_number, directory):


    # 打开wrfout文件
    wrfout_data = nc.Dataset(file_name, 'r')
    print(wrfout_data.variables['P'].shape[0])
    time_step = wrfout_data.variables['P'].shape[0]
    x_cell_number = wrfout_data.variables['P'].shape[3]
    y_cell_number = wrfout_data.variables['P'].shape[2]
    z_cell_number = wrfout_data.variables['P'].shape[1]
    PH = wrfout_data.variables['PH']
    PHB = wrfout_data.variables['PHB']
    height = (PH[0,:,:,:] + PHB[0,:,:,:]) / 9.81    # 网格对应的真实高度
    
    print("height", height.shape)
    
    print("ph",PH.shape)
    print("phb",PHB.shape)
    # 创建结构化网格
    grid = create_custom_structured_grid(x_cell_number, y_cell_number, z_cell_number, height, dx, dy)
    for i in range(time_step):
        for variables in output_variables:
            data = wrfout_data.variables[variables][:]
            # print(data.shape)
            data_same_length = if_dimension(data, x_cell_number, y_cell_number, z_cell_number)   # 维度处理后的数据
            
            # 将标量数据添加到结构化网格
            add_scalar_data_to_grid(grid, data_same_length[i,:,:,:], variables)

        # 保存为 VTK 文件
        save_structured_grid_vts(grid, directory + "/" + f"wrfout_{str(file_number * time_step + i + 1).zfill(6)}.vts")

        # print(data_same_length.shape)
        
    # 关闭文件
    wrfout_data.close()
    return 1
    

# 核心函数
def run_work_2(file_name_1, file_name_2, output_variables, dx, dy, file_number, directory):

    # 打开wrfout文件
    wrfout_data = nc.Dataset(file_name_1, 'r')
    print(wrfout_data.variables['P'].shape[0])
    time_step = wrfout_data.variables['P'].shape[0]
    x_cell_number = wrfout_data.variables['P'].shape[3]
    y_cell_number = wrfout_data.variables['P'].shape[2]
    z_cell_number = wrfout_data.variables['P'].shape[1]
    
    wrfout_data_2 = nc.Dataset(file_name_2, 'r')
    print(wrfout_data_2.variables['P'].shape[0])
    time_step_2 = wrfout_data_2.variables['P'].shape[0]
    x_cell_number_2 = wrfout_data_2.variables['P'].shape[3]
    y_cell_number_2 = wrfout_data_2.variables['P'].shape[2]
    z_cell_number_2 = wrfout_data_2.variables['P'].shape[1]
    
    if time_step != time_step_2 or x_cell_number != x_cell_number_2 or y_cell_number != y_cell_number_2 or z_cell_number != z_cell_number_2:
        return 0
    
    PH = wrfout_data.variables['PH']
    PHB = wrfout_data.variables['PHB']
    height = (PH[0,:,:,:] + PHB[0,:,:,:]) / 9.81    # 网格对应的真实高度
    
    print("height", height.shape)
    
    print("ph",PH.shape)
    print("phb",PHB.shape)
    # 创建结构化网格
    grid = create_custom_structured_grid(x_cell_number, y_cell_number, z_cell_number, height, dx, dy)
    for i in range(time_step):
        for variables in output_variables:
            data_1 = wrfout_data.variables[variables][:]
            data_2 = wrfout_data_2.variables[variables][:]
            
            # print(data.shape)
            data_same_length_1 = if_dimension(data_1, x_cell_number, y_cell_number, z_cell_number)   # 维度处理后的数据
            data_same_length_2 = if_dimension(data_2, x_cell_number, y_cell_number, z_cell_number)   # 维度处理后的数据
            
            # 将标量数据添加到结构化网格
            add_scalar_data_to_grid(grid, data_same_length_1[i,:,:,:] - data_same_length_2[i,:,:,:], variables)

        # 保存为 VTK 文件
        save_structured_grid_vts(grid,  directory + "/" + f"wrfout_{str(file_number * time_step + i + 1).zfill(6)}.vts")

        # print(data_same_length.shape)
        
    # 关闭文件
    wrfout_data.close()
    return 1


