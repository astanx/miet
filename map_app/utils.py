import requests
import numpy as np

def fetch_tiles(api_url):
    tiles = []
    while len(tiles) < 16:
        try:
            if not api_url.startswith(('http://', 'https://')):
                api_url = f'https://{api_url}'
            response = requests.get(f"{api_url.rstrip('')}")
            if response.status_code == 200:
                tile_data = response.json()['message']['data']
                int_data = [[int(num) for num in row] for row in tile_data]
                tiles.append(int_data)

        except Exception as e:
            print(f"Error fetching tile: {e}")
    return tiles

def assemble_map(tiles):
    return np.vstack([np.hstack(tiles[i*4:(i+1)*4]) for i in range(4)])

def get_mission_data(api_url):
    response = requests.get(f"{api_url}/coords")
    if response.status_code == 200:
        data = response.json()['message']
        return data
    return None