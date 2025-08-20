from django.shortcuts import render
from django.http import JsonResponse
from Reflexo.models import Country, Region, Province, District

def home_view(request):
    """Vista para la página principal"""
    return render(request, 'home.html')

def debug_view(request):
    """Vista de depuración para verificar el estado de la base de datos"""
    context = {
        'countries_count': Country.objects.count(),
        'regions_count': Region.objects.count(),
        'provinces_count': Province.objects.count(),
        'districts_count': District.objects.count(),
        'regions_with_ubigeo': Region.objects.filter(ubigeo_code__isnull=False).count(),
        'provinces_with_ubigeo': Province.objects.filter(ubigeo_code__isnull=False).count(),
        'districts_with_ubigeo': District.objects.filter(ubigeo_code__isnull=False).count(),
        'sample_regions': list(Region.objects.all()[:5].values('id', 'name', 'ubigeo_code')),
        'sample_provinces': list(Province.objects.all()[:5].values('id', 'name', 'ubigeo_code', 'region__name')),
        'sample_districts': list(District.objects.all()[:5].values('id', 'name', 'ubigeo_code', 'province__name')),
    }
    return JsonResponse(context)

def countries_view(request):
    """Vista para mostrar países"""
    countries = Country.objects.all()
    return render(request, 'countries.html', {'countries': countries})

def regions_view(request):
    """Vista para mostrar regiones"""
    regions = Region.objects.all()
    return render(request, 'regions.html', {'regions': regions})

def provinces_view(request):
    """Vista para mostrar provincias"""
    provinces = Province.objects.all()
    return render(request, 'provinces.html', {'provinces': provinces})

def districts_view(request):
    """Vista para mostrar distritos"""
    districts = District.objects.all()
    return render(request, 'districts.html', {'districts': districts})

# API endpoints v1
def api_countries(request):
    """API endpoint para países"""
    countries = Country.objects.all().values('id', 'name', 'ubigeo_code')
    return JsonResponse({'countries': list(countries)})

def api_regions(request):
    """API endpoint para regiones"""
    regions = Region.objects.all().values('id', 'name', 'ubigeo_code')
    return JsonResponse({'regions': list(regions)})

def api_provinces(request):
    """API endpoint para provincias"""
    provinces = Province.objects.all().values('id', 'name', 'ubigeo_code', 'region__name')
    return JsonResponse({'provinces': list(provinces)})

def api_districts(request):
    """API endpoint para distritos"""
    districts = District.objects.all().values('id', 'name', 'ubigeo_code', 'province__name')
    return JsonResponse({'districts': list(districts)})