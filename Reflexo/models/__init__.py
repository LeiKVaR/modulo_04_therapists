# Importar todos los modelos
from .country import Country, CountryUser, CountryPatient, CountryTherapist
from .region import Region, RegionUser, RegionPatient, RegionTherapist
from .province import Province, ProvinceUser, ProvincePatient, ProvinceTherapist
from .district import District, DistrictUser, DistrictPatient, DistrictTherapist

__all__ = [
    'Country', 'CountryUser', 'CountryPatient', 'CountryTherapist',
    'Region', 'RegionUser', 'RegionPatient', 'RegionTherapist',
    'Province', 'ProvinceUser', 'ProvincePatient', 'ProvinceTherapist',
    'District', 'DistrictUser', 'DistrictPatient', 'DistrictTherapist',
]
