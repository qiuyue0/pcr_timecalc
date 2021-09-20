# pcr_timecalc

国服pcr合刀计算插件 for Hoshino。简单修改自https://github.com/bugaosuni59/my_Hoshinobot_plugins/tree/master/合刀

pcrtimecalc.py为原合刀计算器

pcr_timecalc_extension为任意时长补偿刀计算器

尾刀计算使用方法：

```
尾刀 刀A伤害 刀B伤害 boss血量 [击杀刀剩余时间]
```

任意时长补偿刀计算使用方法：

```
补时 刀A伤害 boss血量 所需补时 [击杀刀剩余时间]
```

因为用户输入的秒数为整型，所以对于计算.80s左右的尾刀会有精度误差，可能会出现实际秒数比计算秒数多的情况，这是因为计算中采用了相对保守的方法

~~总不能人眼判别秒数精确到0.1s吧~~
