import json

import requests

with open('auth.json', 'r') as fp:
    TOKEN = json.load(fp)["llm_platform_token"]


def generate_script_from_playlist(playlist_name: str, limit: int = 10):
    agent_api = "https://platform.abstergo.ai/v1"
    bearer_token = TOKEN
    try:
        res = requests.post(f"{agent_api}/chat-messages", headers={"Authorization": f"Bearer {bearer_token}"},
                            json={"query": playlist_name, "inputs": {"prompt_count": limit},
                                  "response_mode": "blocking",
                                  "user": "m.shaheen", "conversation_id": ""})
    except Exception as e:
        print(e)
        return None

    answer = res.json()["answer"]
    prompts = json.loads(answer)
    return prompts
