from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.jplhorizons import Horizons
epoch = Time('1977-09-06 00:00')
q = Horizons('399', location='@0', epochs=epoch.tdb.jd)
tab = q.vectors(refplane='earth')
c = SkyCoord(tab['x'].quantity, tab['y'].quantity, tab['z'].quantity, representation_type='cartesian', frame='icrs', obstime=epoch, unit="meter")
print(c)
d = SkyCoord(tab['vx'].quantity, tab['vy'].quantity, tab['vz'].quantity, representation_type='cartesian', frame='icrs', obstime=epoch, unit="meter/second")
print(d)