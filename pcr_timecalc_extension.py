import hoshino
import math
from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('补时', manage_priv=priv.SUPERUSER, help_='请输入：补时 刀1伤害 剩余血量 所需补时 [击杀刀剩余时间]\n如：补时 500 600 44')



class time_calc():
    def __init__(self,dmg1:float,rest:float,time:int,left_time:int):
        self.dmg_A = min(rest,dmg1)
        self.rest = rest
        self.time = time-1+0.0001
        self.left_time = left_time
    def _range(num):
        return round(max(min(num,90.0),21.0),2)
    def A_first(self)->str:
        dmg = round(max(0,1/(110.0-self.time)*90*(self.rest-self.dmg_A)),2)
        if dmg>=self.rest:
            needed_time = math.ceil(90-(110-self.time)*self.rest/(self.rest-self.dmg_A))
            return "刀A先出，刀B需要"+str(needed_time)+"s前击杀才能使刀B获得"+str(math.ceil(self.time))+"秒补时\n"
        return "刀A先出，刀B需要造成"+str(dmg)+"伤害才能使刀B获得"+str(math.ceil(self.time))+"秒补时\n"
    def A_second(self)->str:
        dmg = max(round(self.rest-(110-self.time)/(90.99-self.left_time)*self.dmg_A,2),0)
        return "刀A收尾，刀B需要造成"+str(dmg)+"伤害才能使刀A获得"+str(math.ceil(self.time))+"秒补时"
@sv.on_prefix('补时')
async def feedback(bot, ev: CQEvent):
    cmd = ev.raw_message
    content=cmd.split()
    if(len(content)!=4 and len(content)!= 5):
        reply="请输入：补时 刀A伤害 剩余血量 所需补时 [击杀刀剩余时间]\n如：补时 500 600 44"
        await bot.send(ev, reply)
        return
    d1=float(content[1])
    rest=float(content[2])
    time=int(content[3])
    try:
        left_time = int(content[4])
        flag=0
    except:
        left_time = 1
        flag = 1 if d1>rest else 0
    result = time_calc(d1,rest,time,left_time)
    reply=f"刀A伤害：{d1}    Boss血量：{rest}    所需补时：{time}秒"
    reply+="\n" if flag else f"    击杀时间：{left_time}\n"
    if flag:
        reply+="刀A可以直接击杀boss，请填写击杀剩余时间\n如：补时 610 600 90 11"
        await bot.send(ev, reply)
        return 
    # dmg2 = round(max(0,1/(110.0-t)*90*(rest-dmg1)),2)
    
    # dmg2 = round(max(0,rest-(110.0-t)/90*dmg1),2)
    reply+=result.A_second()
    if(d1>=rest):
        await bot.send(ev, reply)
        return
    reply+=result.A_first()
    await bot.send(ev, reply)
