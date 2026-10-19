#!/usr/bin/env python3
"""Адресные письма Кирилла пользователям через POST /admin/custdev/outreach.

    python3 -I send_custdev_outreach.py <ники.txt> <письмо.txt> <.kubyshka-admin.env> [--send]

Без --send только печатает, кому и что уйдёт. Ники — по одному в строке. Тема всегда
online_talk: письмо от Кирилла, а не ИИ-интервьюер. Пауза 2 с между запросами.
Логин и пароль из env-файла не печатаются.
"""
import base64
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def load_env(path: str) -> dict:
    env = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip().strip("\"'")
    return env


def main() -> None:
    nick_path, message_path, env_path = sys.argv[1:4]
    send = "--send" in sys.argv[4:]
    nicknames = [n.strip() for n in open(nick_path, encoding="utf-8") if n.strip()]
    message = open(message_path, encoding="utf-8").read().strip()
    assert 0 < len(message) <= 1500, "Письмо должно быть 1–1500 символов"
    env = load_env(env_path)
    base_url = (env.get("BASE_URL") or "https://api.kubysh.com").rstrip("/")
    auth = base64.b64encode(f"{env['ADMIN_USERNAME']}:{env['ADMIN_PASSWORD']}".encode()).decode()
    opener = urllib.request.build_opener(NoRedirect)

    print(f"{len(nicknames)} адресатов, письмо {len(message)} символов, {'ОТПРАВКА' if send else 'проверка'}")
    for nickname in nicknames:
        if not send:
            print(f"  {nickname}")
            continue
        body = urllib.parse.urlencode({"nickname": nickname, "topic": "online_talk", "message": message}).encode()
        request = urllib.request.Request(
            f"{base_url}/admin/custdev/outreach",
            data=body,
            headers={"Authorization": f"Basic {auth}", "User-Agent": "curl/8.4.0"},
        )
        status, location = 0, ""
        for attempt in range(4):
            try:
                response = opener.open(request, timeout=30)
                status, location = response.status, response.headers.get("Location", "")
                break
            except urllib.error.HTTPError as error:
                status, location = error.code, error.headers.get("Location", "")
                break
            except urllib.error.URLError:
                # Сбой сети до сервера: письмо не создано, пробуем ещё раз.
                time.sleep(5 * (attempt + 1))
        notice = urllib.parse.parse_qs(urllib.parse.urlparse(location).query).get("notice", [""])[0]
        print(f"  {nickname}: {status} {notice}")
        time.sleep(2)


if __name__ == "__main__":
    main()
