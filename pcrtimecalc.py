import hoshino
import math
from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('合刀', manage_priv=priv.SUPERUSER, help_='请输入：合刀 刀A伤害 刀B伤害 剩余血量 [刀A剩余时间]\n如：合刀 500 600 700\n')
class time_calc():
    def __init__(self,dmg1:float,dmg2:float,rest:float,left_time:int):
        self.dmg_A = min(rest,dmg1)
        self.dmg_B = min(rest,dmg2)
        self.rest=rest
        self.left_time=left_time
    def _range(self,num):
        return round(max(min(num,90.0),21.0),2)
    def A_first(self)->str:
        ret = self._range(110-(self.rest-self.dmg_A)/self.dmg_B*(90.95-self.left_time))
        return str(ret)
    def B_first(self)->str:
        ret = self._range(110-(self.rest-self.dmg_B)/self.dmg_A*(90.95-self.left_time))
        return str(ret)
@sv.on_prefix('合刀')
async def feedback(bot, ev: CQEvent):
    cmd = ev.raw_message
    content=cmd.split()
    if(len(content)!=4 and len(content)!=5):
        reply="请输入：合刀 刀A伤害 刀B伤害 剩余血量 [刀A剩余时间]，如：合刀 500 600 700\n"
        await bot.send(ev, reply)
        return
    try:
        left_time = float(content[4])
    except:
        left_time = 1.0
    d1=float(content[1])
    d2=float(content[2])
    rest=float(content[3])
    if(d1+d2<rest):
        reply="醒醒！这两刀是打不死boss的\n"
        await bot.send(ev, reply)
        return
    result = time_calc(d1,d2,rest,left_time)
    
    reply=f"刀A伤害：{d1}\t刀B伤害：{d2}\tBOSS血量：{rest}\n"
    if(d1>=rest or d2>=rest):
        if(len(content)==4):
            reply=reply+"第一刀可直接秒杀boss，请输入：合刀 刀A伤害 刀B伤害 剩余血量 击杀刀剩余时间\n如：合刀 620 450 600 8\n"
            await bot.send(ev, reply)
            return
        elif(d2>=rest):
            reply=reply+"刀A先出，另一刀可获得 "+result.A_first()+" 秒补偿刀\n"
            await bot.send(ev, reply)
            return
        elif(d1>=rest):
            reply=reply+"刀B先出，另一刀可获得 "+result.B_first()+" 秒补偿刀\n"
            await bot.send(ev, reply)
            return
    reply=reply+"刀A先出，另一刀可获得 "+result.A_first()+" 秒补偿刀\n"
    reply=reply+"刀B先出，另一刀可获得 "+result.B_first()+" 秒补偿刀\n"
    await bot.send(ev, reply)
