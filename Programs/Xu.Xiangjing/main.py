import sunpy.map
import matplotlib.pyplot as plt
from sunpy.map.header_helper import make_heliographic_header

file = "E:/python/EUImap/data/solo_L1_eui-fsi174-image-short_20230328T000050186_V01.fits"
shape = (720, 1440)

eui_map = sunpy.map.Map(file)
carr_header = make_heliographic_header(eui_map.date,
                                       eui_map.observer_coordinate,
                                       shape,
                                       frame='carrington')
eui_carr = eui_map.reproject_to(carr_header)

fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(projection=eui_map)
ax.set_title(f"Time: {eui_map.date.strftime('%Y-%m-%d %H:%M:%S')}")
eui_map.plot(axes=ax, autoalign=True)
plt.show()
