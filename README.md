# ProgressBar
通过封装/bossbar实现的进度条。

> 灵感来源于Bukkit端插件CMI

## 快速上手
安装至MCDR后登陆服务器，输入：
```
!!pb timer 10
```
即可获得一个10秒的倒计时条（确保权限等级>1）。

## 静态方法

|名称|参数|描述|
|----|----|----|
|wait_bar|wait_time, player, text="", color=BarColor.WHITE, style=BarStyle.NOTCHED_10, update_interval=0.5, fall=True|召唤一个等待条并阻塞，结束后消失并返回None，可代替time.sleep()|

### wait_bar

|参数|类型|描述|默认值|
|----|----|----|----|
|wait_time|int,float|等待时间（秒）|必须项|
|player|str|玩家名称或@选择器|必须项|
|text|str|条的文本|'"请等待{wait_left_time}秒... {wait_passed_time}/{waite_time}"'|
|color|BarColor|条的颜色|BarColor.WHITE|
|style|BarStyle|条的样式|BarStyle.NOTCHED_10|
|update_interval|int,float|更新间隔（秒）|0.5|
|fall|bool|逐渐减少？|True|

> `wait_time`与`update_interval`会自动四舍五入地转为1GameTick(0.05s)的整数倍。
>
> `player`用于命令`/bossbar set <id> players <players>`中<players>的值。
> 
> `text`为[`原始JSON文本格式`](https://minecraft-zh.gamepedia.com/%E5%8E%9F%E5%A7%8BJSON%E6%96%87%E6%9C%AC%E6%A0%BC%E5%BC%8F)，需要自行验证格式，暂不支持直接输入RText（Fallen_Breath.lazy）。可使用如下占位符：
> 
> |占位符|替换值|
> |----|----|
> |`{wait_left_time}`|等待时间（即`wait_time`）|
> |`{wait_passed_time}`|已等待时间|
> |`{wait_left_time}`|剩余时间|
> 
> `color`与`style`分别输入`BarColor`与`BarStyle`枚举类，请参考下文“类-BarColor/BarStyle”。
> 
> `fall`值为True则倒计时过程中条的值递减（0%->100%），False递增（100%->0%）。

## 枚举类
### BarColor
这是一个描述Bar颜色的枚举类，用于`bossbar set <id> color <color>`命令中的`<color>`

|枚举项|意义|
|----|----|
|BLUE|蓝色|
|GREEN|绿色|
|PINK|粉色|
|PURPLE|紫色|
|RED|红色|
|WHITE|白色|
|YELLOW|黄色|

使用例：progress_bar=Bar('"Test"').color(**BarColor.BLUE**)

### BarStyle
这是一个描述Bar样式的枚举类，用于`bossbar set <id> style <style>`命令中的`<style>`

|枚举项|意义|
|----|----|
|NOTCHED_6|分6段|
|NOTCHED_10|分10段|
|NOTCHED_12|分12段|
|NOTCHED_20|分20段|
|PROGRESS|连续不分段|

使用例：progress_bar=Bar('"Test"').style(**BarStyle.NOTCHED_6**)

> 若不知道各个颜色和样式的区别，可以开一个能使用指令的存档，然后试着：
> 1. 创建bossbar：`/bossbar add bar:test "test"`；
> 2. 设置对自己可见：`/bossbar set bar:test players @s`；
> 3. 设置值为50：`/bossbar set bar:test value 50`；
> 4. 现在应该能看到一个白色的boss栏了，尝试下表的命令：
> 
> |命令|更改为颜色|命令|样式|
> |----|----|----|----|
> |`/bossbar set bar:test color blue`|蓝色|`/bossbar set bar:test style notched_6`|分6段|
> |`/bossbar set bar:test color green`|绿色|`/bossbar set bar:test style notched_10`|分10段|
> |`/bossbar set bar:test color pink`|粉色|`/bossbar set bar:test style notched_12`|分12段|
> |`/bossbar set bar:test color purple`|紫色|`/bossbar set bar:test style notched_20`|分20段|
> |`/bossbar set bar:test color red`|红色|`/bossbar set bar:test style progress`|连续不分段|
> |`/bossbar set bar:test color white`|白色|
> |`/bossbar set bar:test color yellow`|黄色|
> 5. 最后记得把刚刚创建的bossbar删掉：`/bossbar remove bar:test`。

## 还在施工，先commit一下吧……
