import hoshino
import math
from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('补时', manage_priv=priv.SUPERUSER, help_='请输入：补时 刀1伤害 剩余血量 所需补时\n如：补时 500 600 44\n')


@sv.on_prefix('补时')
async def feedback(bot, ev: CQEvent):
    cmd = ev.raw_message
    content=cmd.split()
    if(len(content)!=4):
        reply="请输入：补时 刀1伤害 剩余血量 所需补时\n如：补时 500 600 44\n"
        await bot.send(ev, reply)
        return
    d1=float(content[1])
    rest=float(content[2])
    time=int(content[3])
    dmg1=d1
    t=float(time)-1+0.01
    reply=f"刀1伤害：{d1}    Boss血量：{rest}    所需补时：{time}秒\n"
    dmg2 = round(max(0,1/(109.01-t)*90*(rest-dmg1)),1)
    reply+="第一刀先出，第二刀需要造成"+str(dmg2)+"伤害才能使第二刀获得"+str(time)+"秒补时\n"
    dmg2 = round(max(0,rest-(109.01-t)/90*dmg1),1)
    reply+="第一刀后出，第二刀需要造成"+str(dmg2)+"伤害才能使第一刀获得"+str(time)+"秒补时"
    await bot.send(ev, reply)
