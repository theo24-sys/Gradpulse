import time
import os
from agora_token_builder import RtcTokenBuilder

def generate_agora_token(channel_name, uid=0):
    """
    Generates an Agora RTC token for a given channel name.
    """
    app_id = os.environ.get('AGORA_APP_ID')
    app_certificate = os.environ.get('AGORA_APP_CERTIFICATE')
    
    if not app_id or not app_certificate:
        return None
        
    # Expiration time in seconds (e.g., 1 hour)
    expiration_time_in_seconds = 3600
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds
    
    # Role: 1 for Publisher, 2 for Subscriber
    role = 1 
    
    token = RtcTokenBuilder.buildTokenWithUid(
        app_id, 
        app_certificate, 
        channel_name, 
        uid, 
        role, 
        privilege_expired_ts
    )
    
    return token
