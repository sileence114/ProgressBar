# ProgressBar

> 灵感来源于Bukkit端插件CMI

通过封装[`/bossbar`](https://minecraft-zh.gamepedia.com/%E5%91%BD%E4%BB%A4/bossbar)实现的进度条。

## 所需模块
|名称|安装|
|----|----|
|uuid|`pip install uuid`|

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
|text|str|条的文本|'请等待§c§l{wait_left_time}§r秒... §c§l{wait_passed_time}§r/§c§l{waite_time}'|
|color|BarColor|条的颜色|BarColor.WHITE|
|style|BarStyle|条的样式|BarStyle.NOTCHED_10|
|update_interval|int,float|更新间隔（秒）|0.5|
|fall|bool|逐渐减少？|True|

> `wait_time`与`update_interval`会自动四舍五入地转为1GameTick(0.05s)的整数倍。
>
> `player`用于命令`/bossbar set <id> players <players>`中<players>的值。
> 
> `text`为字符串，可用`§`样式代码。因为要使用`str.replace()`将占位符替换为相应的值，故不可用`RText`和`RTextList`。
> 
> |占位符|替换值|
> |----|----|
> |`{wait_left_time}`|等待时间（即`wait_time`）|
> |`{wait_passed_time}`|已等待时间|
> |`{wait_left_time}`|剩余时间|
> 
> `color`与`style`分别输入`BarColor`与`BarStyle`枚举类，请参考下文“枚举类 - BarColor/BarStyle”。
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

### 构造 \_\_init\_\_(self, text, id_=None)

|参数|类型|描述|默认值|
|----|----|----|----|
|text|str,RText,RTextList|bossbar的标题|必须项|
|id_|str|Bar对象的ID|uuid.uuid4()|

在Bar对象创建时，会通过`bossbar`命令创建id为`pb:{id_}`的bossbar，所以请不要手动通过命令修改命名空间为`pb`的bossbar！
当Bar成功创建，会以`id_`作为key将自己添加到全局字典`Bars`。

> `text`可用使用带有样式代码`§`的字符串，也可以是`RText`和`RTextList`的实例，但最终会处理为[`原始JSON文本格式`](https://minecraft-zh.gamepedia.com/%E5%8E%9F%E5%A7%8BJSON%E6%96%87%E6%9C%AC%E6%A0%BC%E5%BC%8F)到成员变量`_text`上。
> `id_`作为寻找Bar对象的键，不可重复，若与现有的重复，则会与没有指定一样分配一个随机的UUID。

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
> 请注意：bossbar在minecraft中的ID为：`pb:{ID}`。

### 设置/获取标题 text(self, text=None)
当参数`text`的值为字符串或RText,RTextList实例时，设置标题，返回self；
参数`text`的值为None时，返回标题。

|参数|类型|描述|默认值|
|----|----|----|----|
|text|str,RText,RTextList|标题|None|
> 与构造函数中的`text`参数类似，`text`也可以使用带有样式代码`§`的字符串和`RText`、`RTextList`的实例，最终也会处理为[`原始JSON文本格式`](https://minecraft-zh.gamepedia.com/%E5%8E%9F%E5%A7%8BJSON%E6%96%87%E6%9C%AC%E6%A0%BC%E5%BC%8F)到成员变量`_text`上。

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

## 命令交互
命令前缀可以自行配置，子命令所需权限也可以自行更改，请参考下文“可配置字典变量”；
### !!pb timer \<time\> \[user\]
就像前面“快速上手”那样启动一个计时器。
`\<time\>`：计时器时间（秒）；
`\[user\]`：显示计时器的用户，可以使用@选择器，@a需要相应权限；选填，默认自己（在控制台必填）。

### !!pb list
通过列表的形式展示所有的Bar对象的实例。

## 可配置字典变量
### 注意事项
1. 使用文本编辑器打开ProgressBar.py，推荐使用`Sublime`、`VSCode`等编辑器打开；
2. 除非你知道自己操作的后果，否则请不要增减`缩进`、修改`键`和`括号`、以及`PB_CONFIG`变量以外的其他内容；
3. 打开后找到如下代码修改：
```python
PB_CONFIG = {
    'user_interface': {
        'enable': True,
        'prefix': '!!pb',
        'help_message_container': (
            '------ §aMCDR ProgressBar插件帮助信息 §r------',
            '--------------------------------'
        ),
        'sub_command': {
            'help': {
                'use_permission_limit': (0, 1, 2, 3, 4),
                'help_msg': '§b{prefix} [help] §f- §c显示此帮助信息'
            },
            'timer': {
                'use_permission_limit': (1, 2, 3, 4),
                '@a_permission_limit': (2, 3, 4),  # 在[user]参数中填入@a的权限限制
                'help_msg': '§b{prefix} timer <time> [user] §f- §c显示一个简易计时器\n§7<time>:时间(秒) [user]:显示的玩家(默认自己)'
            },
            'list': {
                'use_permission_limit': (2, 3, 4),
                'delete_permission_limit': (3, 4),  # 删除权限限制，还没有实现，咕咕咕。
                'help_msg': '§b{prefix} list §f- §c通过列表的形式展示所有的Bar对象的实例'
            }
        }
    }
}
```
### user_interface节点
这个节点配置用户交互相关事项。

|键|描述|默认|
|----|----|----|
|`enable`|是否启用用户交互，为False甚至不会在帮助列表中出现|True|
|`prefix`|命令前缀|'!!pb'|
|`help_message_container`|帮助命令显示容器，为两个元素的元组<br>子命令的帮助信息会加载中间|('------ §aMCDR ProgressBar插件帮助信息 §r------',<br>'--------------------------------')|
|`sub_command`|子命令配置节点|{'help': {...},'timer': {...},'list': {...}}|

#### sub_command节点
这个节点用于设置子命令的使用权限、帮助信息等。

|键|描述|默认|
|----|----|----|
|`help`|帮助命令的相关|{'use_permission_limit': (0, 1, 2, 3, 4),<br>'help_msg': '§b{prefix} [help] §f- §c显示此帮助信息'}|
|`timer`|计时器相关|{'use_permission_limit': (1, 2, 3, 4),<br>'@a_permission_limit': (2, 3, 4),<br>'help_msg': '§b{prefix} timer <time> [user] §f- §c显示一个简易计时器\n§7<time>:时间(秒) [user]:显示的玩家(默认自己)'}|
|`list`|Bar实例列表相关|{'use_permission_limit': (2, 3, 4),<br>'delete_permission_limit': (3, 4),<br>'help_msg': '§b{prefix} list §f- §c通过列表的形式展示所有的Bar对象的实例'}|

#### sub_command子节点
子节点较多，但主要设置一下两类，在此不一一列举。

|键|描述|举栗|
|----|----|----|
|`use_permission_limit`|子命令使用权限等级限制<br>仅元组内列举的权限等级才能被运行使用该命令|(2, 3, 4)|
|`*_permission_limit`|子命令的具体功能限制|(3, 4)|
|`help_msg`|用于在帮助列表显示的描述|'§b{prefix} [help] §f- §c显示此帮助信息'|

> `help_msg`中使用`{prefix}`作为前缀的占位符。
>> 因使用了`str.format()`，所以若想显示大括号则需要转义（`{`->`{{`，`}`->`}}`）。
