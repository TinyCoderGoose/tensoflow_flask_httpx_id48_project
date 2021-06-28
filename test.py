import asyncio
from searchTB import spiderTaoBao
from searchSN import spiderSuNing
from searchJD import spiderJingDong
def spiderRun(keyword='显卡'):
    t = spiderTaoBao(keyword)
    s = spiderSuNing(keyword)
    j = spiderJingDong(keyword)
    loop = asyncio.new_event_loop()
    tasks = asyncio.wait([s.run(), t.run(),j.run()])
    loop.run_until_complete(tasks)