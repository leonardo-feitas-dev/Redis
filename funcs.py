import redis
from datetime import datetime, timedelta

# Configuração do cliente Redis
r = redis.Redis(
    host='oregon-redis.render.com', 
    port=6379, 
    password='zwSSy3QLI171V0cJO27hvUXRlOw4oziR', 
    username='red-csj60u68ii6s73d025f0'
)

def create_user_session(user_id, session_token, ip_address, device_info, browser_info):
    """Cria uma sessão de usuário com detalhes do dispositivo e expira após 2 horas."""
    session_key = f"session:{session_token}"
    r.hset(session_key, mapping={
        'user_id': user_id,
        'session_token': session_token,
        'ip_address': ip_address,
        'device_info': device_info,
        'browser_info': browser_info,
        'start_time': datetime.now().isoformat()
    })
    r.expire(session_key, timedelta(hours=2))

def set_user_cookie(session_token, cookie_value):
    """Armazena um cookie de sessão e define uma expiração de 30 dias."""
    cookie_key = f"cookie:session_token:{session_token}"
    r.set(cookie_key, cookie_value)
    r.expire(cookie_key, timedelta(days=30))

def set_user_preferences(user_id, language, theme, notifications):
    """Define preferências de usuário, como idioma, tema e notificações."""
    preferences_key = f"user:{user_id}:preferences"
    r.hset(preferences_key, mapping={
        'language': language,
        'theme': theme,
        'notifications': str(notifications).lower()
    })

def add_browsing_history(user_id, page_visited, duration_seconds):
    """Adiciona histórico de navegação do usuário com a página visitada e duração da visita."""
    history_key = f"user:{user_id}:history"
    visit_time = datetime.now().isoformat()
    r.lpush(history_key, f"page_visited:{page_visited}, visit_time:{visit_time}, duration:{duration_seconds}")
    
def get_user_preferences(user_id):
    """Recupera preferências do usuário."""
    preferences_key = f"user:{user_id}:preferences"
    return r.hgetall(preferences_key)

def get_browsing_history(user_id):
    """Recupera histórico de navegação do usuário."""
    history_key = f"user:{user_id}:history"
    return r.lrange(history_key, 0, -1)



