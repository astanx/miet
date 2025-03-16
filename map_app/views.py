from django.shortcuts import render, redirect
from .models import Tile, MissionData
from .utils import fetch_tiles, assemble_map, get_mission_data
import numpy as np
from io import BytesIO
import base64
from PIL import Image

def index(request):
    if request.method == 'POST':
        api_url = request.POST.get('api_url', '').strip()

        if not api_url:
            return render(request, 'index.html', {'error': 'Please enter API URL'})
        
        request.session['api_url'] = api_url
        
        try:
            tiles = fetch_tiles(api_url)
            for tile in tiles:
                Tile.create_from_data(tile)
            mission_data = get_mission_data(api_url)
            if mission_data:
                MissionData.objects.all().delete()
                MissionData.objects.create(
                    sender_x=mission_data['sender'][0],
                    sender_y=mission_data['sender'][1],
                    listener_x=mission_data['listener'][0],
                    listener_y=mission_data['listener'][1],
                    cuper_price=mission_data['price'][0],
                    engel_price=mission_data['price'][1]
                )
            return redirect('map_view')
        except Exception as e:
            return render(request, 'index.html', {'error': str(e)})
    
    return render(request, 'index.html')

def map_view(request):
    tiles = list(Tile.objects.all().values_list('data', flat=True))[:16]
    print(123)
    print(tiles)
    print(23323232)
    if len(tiles) != 16:
        return render(request, 'error.html')
    
    mission_data = MissionData.objects.first()
    map_array = assemble_map([np.array(t) for t in tiles])
    
    img = Image.fromarray(map_array.astype('uint8'))
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    context = {
        'map_image': img_str,
        'mission_data': mission_data,
    }
    return render(request, 'map.html', context)