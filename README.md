# SolO_Data_Analysis_on_GitHubOrg

该仓库主要用于Solar Orbiter（SolO）卫星数据的分析与处理，包含了多个开发者针对不同数据类型的处理脚本，涉及数据下载、合并、可视化、频谱分析以及遗传算法（GA）拟合等功能。

## 目录结构

- **.gitignore**: 定义了仓库中需要忽略的文件类型，包括`*.xml`、`*.cdf`、`*.png`等。
- **Programs**: 包含各开发者的程序目录
  - **Xu.Xiangjing**: 包含`dwnload_eui_data.py`，用于获取EUI数据的下载链接。
  - **Wu.Ziqi**: 包含空文件`null.txt`。
  - **Zhu.Xingyu**: 
    - 包含`batch_download_files.py`（批量下载文件）和空文件`null.txt`。
    - `spectral_analysis`目录：包含`solo_mag_spectral_analysis.py`（磁场数据频谱分析）和`solo_pas_spectra_analysis.py`（粒子数据频谱分析）。
    - `ga_fitting`目录：包含`ga_fitting_of_3D_VDF.py`（3D速度分布函数的遗传算法拟合）和`statistical_analysis_ga_fitting_results.py`（GA拟合结果的统计分析）。
  - **Hou.Chuanpeng**: 包含空文件`null.txt`和`download_EUI_map_data.py`，用于获取EUI地图数据的文件链接。
  - **Duan.Die**: 包含多个MATLAB脚本，主要涉及数据处理、坐标转换、激波分析及GA拟合等，如`DataMerging.m`、`VDF_rtn2mfa.m`、`Shock_Fitting_Calculating.m`、`PAS_VDF_RTN_ga_fitting.m`、`PAS_VDF_RTN_ga_fitting_plot_alpha.m`、`ga_constraint.m`等。
  - **PJY/SolO_vdf/.idea**: 包含IDE相关的`.gitignore`文件，定义了IDE生成的需忽略的文件。
  - **PJY**: 包含`ga_fitting_of_3D_VDF.py`（遗传算法迭代过程监控）。


## 主要功能说明

1. **数据下载**
   - `dwnload_eui_data.py`: 根据指定的时间范围、分辨率和波长，生成EUI数据的下载链接。
   - `download_EUI_map_data.py`: 从指定的归档URL中提取后缀为`fits`或`jp2`的EUI地图数据文件链接。
   - `batch_download_files.py`: 用于批量下载文件（具体下载对象可根据实际配置调整）。

2. **数据合并与预处理**
   - `DataMerging.m`: 合并指定日期范围内的磁数据（`solo_l2_mag-rtn-normal_*`）和粒子数据（`solo_l2_swa-pas-grnd-mom_*`），并将结果保存为`.mat`文件。
   - 坐标转换相关：`VDF_rtn2mfa.m`（将速度分布函数数据从RTN坐标系转换到MFA坐标系）、`calc_wpara_wperp.m`（计算平行和垂直于磁场的速度分量）等。

3. **数据可视化与分析**
   - `plot_Summary_SolO.m`: 绘制SolO的快速查看数据和PAS vdf数据，包括磁场分量、粒子速度、密度、温度以及粒子通量等的时间序列和分布图。
   - 冲击与重联分析：
     - `Shock_Fitting_Calculating.m`、`Wind_Shock_Fitting_Calculating.m`: 针对冲击事件的拟合计算，包括磁场与速度分量对比、冲击位置识别、压力计算等。
     - `HT_Frame_Calculating.m`: 涉及磁场分量绘图、LMN坐标系转换与绘图、粒子能量峰值提取等冲击相关参数分析。
     - `Reconnection_Paper_Fig2.m`、`Reconnection_Paper_Fig3.m`: 重联事件相关论文图表生成脚本。

4. **频谱分析**
   - `solo_mag_spectral_analysis.py`: 对磁场数据（RTN分量）进行小波分析，计算功率谱密度（PSD）、结构函数等，研究磁场的频谱特性。
   - `solo_pas_spectra_analysis.py`: 对粒子数据（密度、速度RTN分量等）进行小波分析，计算功率谱密度、结构函数及相关误差，研究粒子参数的频谱特性。

5. **遗传算法（GA）拟合**
   - **Zhu.Xingyu/ga_fitting**:
     - `ga_fitting_of_3D_VDF.py`: 定义3D速度分布函数（VDF）的GA拟合目标函数，通过遗传算法优化核心和束流组分的参数（密度、温度、速度等），最小化拟合结果与观测数据的误差。
     - `statistical_analysis_ga_fitting_results.py`: 对GA拟合得到的参数（如密度、温度、速度分量等）进行统计分析，计算置信区间、偏差，并绘制时间序列分布图。
   - **Duan.Die**:
     - `PAS_VDF_RTN_ga_fitting.m`、`PAS_VDF_RTN_ga_fitting_plot_alpha.m`: 在RTN坐标系下对PAS仪器的VDF数据进行GA拟合，包含数据插值、磁场坐标系转换、拟合结果可视化等步骤，用于分析速度分布的核心和束流结构。
     - `ga_constraint.m`: 定义GA拟合中的约束条件（如参数间的不等式约束），用于优化拟合过程。
   - **PJY/ga_fitting_of_3D_VDF.py**: 实现GA迭代过程的监控函数，输出每一代的最优适应度及与上一代的变化，便于跟踪拟合收敛情况。


## 使用说明

1. **Python脚本依赖**
   - 数据下载脚本：需安装`requests`、`BeautifulSoup`，可通过`pip install requests beautifulsoup4`安装。
   - 频谱分析脚本：需安装`numpy`、`matplotlib`、`spacepy`、`pycwt`、`scipy`等，通过`pip install numpy matplotlib spacepy pycwt scipy`安装。
   - GA拟合脚本：需安装`numpy`、`matplotlib`、`scipy`、`deap`（或其他GA库），根据实际依赖配置安装。

2. **MATLAB脚本依赖**
   - 需在MATLAB环境中运行，部分脚本依赖`spdfcdfread`工具读取CDF格式数据，以及`Global Optimization Toolbox`用于GA拟合。

3. **数据路径配置**
   - 脚本中涉及的本地数据路径（如`D:\SolOData\`、`/Users/psr/data/`）需根据实际存储位置修改。


## 注意事项

- 处理大型数据文件（如VDF数据）时，需确保有足够的存储空间和计算资源。
- GA拟合参数（如迭代次数、种群规模）可根据拟合精度需求调整，平衡计算效率与结果准确性。
- 频谱分析和GA拟合的时间范围、数据筛选条件为示例参数，使用时需根据具体研究对象调整。
