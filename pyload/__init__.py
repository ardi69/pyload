# -*- coding: utf-8 -*-

__status_code__ = 4
__status__ = {1: "Planning",
              2: "Pre-Alpha",
              3: "Alpha",
              4: "Beta",
              5: "Production/Stable",
              6: "Mature",
              7: "Inactive"}[__status_code__]  #: PyPI Development Status classifiers

__version_info__ = (0, 4, 10)
__version__ = '.'.join(map(str(v), __version_info__))

__license__ = "GNU Affero General Public License v3"
