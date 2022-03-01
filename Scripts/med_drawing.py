
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

fig, axes = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
extent = [-5.5, 37, 28, 46]
axes.add_feature(cfeature.LAND, color='white', zorder=50)
axes.add_feature(cfeature.COASTLINE, color='k', zorder=50)
axes.set_extent(extent)
rect_left = Rectangle((-8, 42), 8, 5, zorder=75, facecolor='white')
rect_right = Rectangle((27.5, 40), 10, 10, zorder=75, facecolor='white')
axes.add_patch(rect_left)
axes.add_patch(rect_right)
axes.outline_patch.set_visible(False)
plt.show()

