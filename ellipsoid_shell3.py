import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Circle, Ellipse, Patch, PathPatch, Wedge
from matplotlib.transforms import Affine2D, IdentityTransform
import numpy as np

class EllipticalShell(Patch):
    """
    Elliptical shell patch.
    """

    def __str__(self):
        return f"EllipticalShell(center={self.center}, width={self.width}, height={self.height}, thick={self.thick}, angle={self.angle})"

    def __init__(self, center, width, height, thick, angle=0.0, **kwargs):
        """
        Draw an elliptical ring centered at *x*, *y* center with outer width (horizontal diameter)
        *width* and outer height (vertical diameter) *height* with a fractional ring thickness of *thick*
        ( [r_outer - r_inner]/r_outer where r is the major radius).
        Valid kwargs are:
        %(Patch)s
        """
        super().__init__(**kwargs)
        self.center = center
        self.height, self.width = height, width
        self.thick = thick
        self.angle = angle
        self._recompute_path()
        # Note: This cannot be calculated until this is added to an Axes
        self._patch_transform = IdentityTransform()

    def _recompute_path(self):
        # Form the outer ring
        arc = Path.arc(theta1=0.0, theta2=360.0)
        print(f'{arc=}')
        # Draw the outer unit circle followed by a reversed and scaled inner circle
        v1 = arc.vertices
        v2 = np.zeros_like(v1)
        v2[:, 0] = v1[::-1, 0] * float(1.0 - self.thick[0])
        v2[:, 1] = v1[::-1, 1] * float(1.0 - self.thick[1])
        print(f'{v1=} {v2=}')
        v = np.vstack([v1, v2, v1[0, :], (0, 0)])
        print(f'{v=}')
        c = np.hstack([arc.codes, arc.codes, Path.MOVETO, Path.CLOSEPOLY])
        print(f'{c=}')
        c[len(arc.codes)] = Path.MOVETO
        # Final shape acheieved through axis transformation. See _recompute_transform
        self._path = Path(v, c)

    def _recompute_transform(self):
        """NOTE: This cannot be called until after this has been added
                 to an Axes, otherwise unit conversion will fail. This
                 makes it very important to call the accessor method and
                 not directly access the transformation member variable.
        """
        center = (self.convert_xunits(self.center[0]), self.convert_yunits(self.center[1]))
        width = self.convert_xunits(self.width)
        height = self.convert_yunits(self.height)
        self._patch_transform = Affine2D() \
            .scale(width * 0.5, height * 0.5) \
            .rotate_deg(self.angle) \
            .translate(*center)

    def get_patch_transform(self):
        self._recompute_transform()
        return self._patch_transform

    def get_path(self):
        if self._path is None:
            self._recompute_path()
        return self._path



fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})

e3 = EllipticalShell(center=(0, 0),
                     width=1,
                     height=1,
                     thick=(0.5, 0.0),
                     angle=0)
ax.add_patch(e3)
e3.set_facecolor((1, 0, 0))


e1 = Ellipse(xy=(0, 0),
             width=0.1,
             height=1,
             angle=0)
ax.add_patch(e1)
e1.set_facecolor((0, 0, 1))

e2 = Ellipse(xy=(0, 0),
             width=0.1,
             height=1,
             angle=90)
ax.add_patch(e2)
e2.set_facecolor((0, 1, 0))


ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

arc = Path.arc(theta1=0.0, theta2=360.0)
v1 = arc.vertices
v2 = arc.vertices[::-1] * float(1.0 - 0.5)  # self.thick is fractional thickness


ax.scatter(v1[:,0], v1[:,1])
ax.scatter(v2[:,0], v2[:,1])

plt.show()
