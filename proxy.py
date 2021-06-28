from httpx import AsyncClient

proxyHost = "forward.apeyun.com"
proxyPort = "9082"

# 代理隧道验证信息
proxyUser = "2021042800845441043"
proxyPass = "RrIenLnwFmaajEmW"

proxyServer = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

class MySession(AsyncClient):
    def __init__(self):
        super().__init__(proxies={
            "http://": proxyServer,
            "https://": proxyServer,
        })
        self.headers['Connection'] = 'close'