from datetime import datetime
import requests

def reset_daily_payments():
    try:
        response = requests.post('http://127.0.0.1:8014/sitters/reset_daily_payments')
        response.raise_for_status()
        print(f"Sitters' daily payments reset successfully at {datetime.now()}.")
    except requests.RequestException as e:
        print(f"Failed to reset sitters' daily payments: {e}")

def reset_sitter_status():
    try:
        response = requests.get('http://127.0.0.1:8014/sitters/get_all_sitters')
        sitters = response.json()['data']

        for sitter in sitters:
            sitter_id = sitter['id']
            requests.put(f'http://127.0.0.1:8014/sitters/new_day_sitter/?sitter_id={sitter_id}')
        print(f"Sitters' status reset successfully at {datetime.now()}.")
    except requests.RequestException as e:
        print(f"Failed to reset sitters' status: {e}")


