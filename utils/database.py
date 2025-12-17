import json
from upstash_redis import Redis
from datetime import datetime, timezone

# 从环境变量中初始化 Upstash Redis 客户端
# SDK 会自动读取 UPSTASH_REDIS_REST_URL 和 UPSTASH_REDIS_REST_TOKEN
redis = Redis.from_env()

def save_scores(scores: list, ttl_seconds: int = None):
    """
    将一份完整的成绩列表保存到 Upstash Redis。
    我们使用带时间戳的 key 来保存历史记录。

    Args:
        scores (list): 从 ScoreFetcher 获取的 combined_scores 列表。
        ttl_seconds (int): 数据过期时间（秒），默认 永不过期。
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    key = f"scores:{timestamp}"
    
    print(f"--- 准备保存成绩到 Upstash Redis，Key: {key}，TTL: {ttl_seconds}秒 ---")
    
    # 使用 redis.set() 方法，设置过期时间
    redis.set(key, scores, ex=ttl_seconds)
    
    print(f"--- 成功保存 {len(scores)} 条成绩记录到 Upstash Redis ---")
    return key

def get_latest_scores():
    """
    从 Upstash Redis 中获取最新的一份成绩单。
    """
    score_keys = redis.keys("scores:*")
    if not score_keys:
        return None # 或者返回一个空列表 [] 会更友好
    
    latest_key = sorted(score_keys, reverse=True)[0]
    
    print(f"--- 正在从 Key '{latest_key}' 读取最新成绩 ---")
    
    json_data_string = redis.get(latest_key) # 获取到的是JSON字符串
    
    if not json_data_string:
        return None # 或者 []

    # 在返回前，将 JSON 字符串解析成 Python 对象 (列表)
    return json.loads(json_data_string) # <--- 添加这一步！