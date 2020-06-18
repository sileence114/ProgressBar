# ProgressBar

> 灵感来源于Bukkit端插件CMI

通过封装/bossbar实现的进度条。



## 所需模块
- `uuid`
### 安装
- `pip install uuid`

## 快速上手
安装至MCDR后登陆服务器，输入：
```
!!pb timer 10
```
即可获得一个10秒的倒计时条（确保权限等级>1）。

## 静态方法

|名称|参数|描述|
|----|----|----|
|wait_bar|wait_time, player, text="", color=BarColor.WHITE, style=BarStyle.NOTCHED_10, update_interval=0.5, fall=True|召唤一个等待条并阻塞，计时结束后消失并返回None，可代替time.sleep()|

### wait_bar(wait_bar|wait_time, player, text="", color=BarColor.WHITE, style=BarStyle.NOTCHED_10, update_interval=0.5, fall=True)

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
> `color`与`style`分别输入`BarColor`与`BarStyle`枚举类，请参考下文“枚举类-BarColor/BarStyle”。
> 
> `fall`值为True则倒计时过程中条的值递减（0%->100%），False递增（100%->0%）。

## Bar类
通过Bar类可以通过创建对象的方式创建bossbar，很方便的修改、获取bossbar的参数。
关于Bar类的具体使用实例请阅读静态方法`wait_bar()`相关的源码。

### 成员变量
**请通过Getter/Setter方法访问成员变量！**
Setter会更改配置到minecraft，直接更改变量会导致很多问题！
|名称|默认值|用途|Getter()|Setter(val)|
|----|----|----|----|----|
|**\_id**|无|用于关联Bar对象与bossbar|get_id()|无|
|**\_text**|无|用于设置bossbar标题|text()|text(val)|
|**\_time**|time.time()|记录创建时间|get_time()|无|
|**\_color**|BarColor.WHITE|设置bossbar颜色|color()|color(val)|
|**\_style**|BarStyle.PROGRESS|设置bossbar样式|style()|style(val)|
|**\_value**|0|bossbar的值|value()|value(val)|
|**\_max**|100|bossbar的最大值|max()|max(val)|
|**\_visible**|True|bossbar的可见性|visible()|visible(val)|
|\_\_del\_count|0|析构执行计数 避免无尽套娃|无|无|
|\_\_deleted|False|记录是否从minecraft中删除|无|无|

### 构造 \_\_init\_\_(self, text, id=None)

|参数|类型|描述|默认值|
|----|----|----|----|
|text|str|bossbar的标题|必须项|
|id|str|Bar对象的ID|uuid.uuid4()|

在构造时，会通过`bossbar`命令创建id为`pb:{id}`的bossbar，所以请不要手动通过命令修改命名空间为`pb`的bossbar！
当Bar成功创建时，会自动将自己添加到全局的字典变量Bars，key为`id`。

> `text`为[`原始JSON文本格式`](https://minecraft-zh.gamepedia.com/%E5%8E%9F%E5%A7%8BJSON%E6%96%87%E6%9C%AC%E6%A0%BC%E5%BC%8F)，需要自行验证格式，暂不支持直接输入RText（Fallen_Breath.lazy）。
> `id`作为寻找Bar对象的键，不可重复，若与现有的重复，则会与没有指定一样分配一个随机的UUID。

### 获取创建时间 get_time(self)
返回创建时的time.time()

### 删除 delete(self)
删除Bar，并从Bars中删除自己，从minecraft中删除bossbar。

### 显示给玩家 show(self, player)
将bossbar显示给玩家。

|参数|类型|描述|默认值|
|----|----|----|----|
|player|str|玩家名称 或@选择器|必须项|

### 获取ID get_id(self)
返回Bar的ID。
> 请注意：bossbar在minecraft中的id为：`pb:{ID}`。

### 设置/获取标题 text(self, text=None)
当参数`text`的值为字符串时，设置标题，返回self；
参数`text`的值为None时，返回标题。

|参数|类型|描述|默认值|
|----|----|----|----|
|text|str|标题|None|
> `text`必须为"原始JSON文本格式"(暂时不支持RText，Fallen_Breath.lazy) 请自行校验 如：'{"text": "BarBar"}'。

### 设置/获取颜色 color(self, color=None)
当参数`color`的值为枚举类`BarColor`的实例时，设置颜色，返回self；
否则，返回颜色。

|参数|类型|描述|默认值|
|----|----|----|----|
|color|BarColor|颜色|None|

### 设置/获取样式 style(self, style=None)
当参数`style`的值为枚举类`BarStyle`的实例时，设置样式，返回self；
否则，返回样式。

|参数|类型|描述|默认值|
|----|----|----|----|
|style|BarStyle|样式|None|

### 设置/获取最大值 max(self, max_=None)
当参数`max_`的类型为int，且大于0、小于等于2147483647时，设置最大值，并返回self；
否则，返回当前的最大值。

|参数|类型|描述|默认值|
|----|----|----|----|
|max_|int|最大值|None|

### 设置/获取值 value(self, value=None)
当参数`value`的类型为int，且大于等于0、小于等于`max()`时，设置值，并返回self；
否则，返回当前的值。

|参数|类型|描述|默认值|
|----|----|----|----|
|value|int|值|None|

### 设置/获取可见性 visible(self, visible=None)
当参数`visible`的类型为bool，设置可见性，并返回self；
否则，返回当前的可见性。

|参数|类型|描述|默认值|
|----|----|----|----|
|value|int|最大值|None|

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
