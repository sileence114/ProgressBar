import uuid

from enum import Enum
import time

from utils.rtext import *

# ---------- 下方PB_CONFIG变量为可配置变量 请不要修改key 不要增加/减少缩进 ----------
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
# ---------- 可配置变量到此结束 下为插件正文 请不要修改 ----------

for key in PB_CONFIG['user_interface']['sub_command'].keys():
    PB_CONFIG['user_interface']['sub_command'][key]['help_msg'] = \
        PB_CONFIG['user_interface']['sub_command'][key]['help_msg'].format(prefix=PB_CONFIG['user_interface']['prefix'])

server_instance = None
if_server_alive = False
Bars = {}


class BarColor(Enum):
    BLUE = 0
    GREEN = 1
    PINK = 2
    PURPLE = 3
    RED = 4
    WHITE = 5
    YELLOW = 6


class BarStyle(Enum):
    NOTCHED_6 = 0
    NOTCHED_10 = 1
    NOTCHED_12 = 2
    NOTCHED_20 = 3
    PROGRESS = 4


BarColor_to_RText = {
    BarColor.BLUE: RColor.blue,
    BarColor.GREEN: RColor.green,
    BarColor.PINK: RColor.light_purple,
    BarColor.PURPLE: RColor.dark_purple,
    BarColor.RED: RColor.red,
    BarColor.WHITE: RColor.white,
    BarColor.YELLOW: RColor.yellow
}


class Bar(object):
    def __init__(self, text, id_=None):
        """
        :param text: 标题，将双引号转义，富文本请用RText
        :type text: str, RText, RTextList
        :param id_:
        """
        self._color = BarColor.WHITE
        self._style = BarStyle.PROGRESS
        self._value = 0
        self._max = 100
        self._visible = True
        self.__del_count = 0
        self.__deleted = False
        if server_instance is not None and if_server_alive:
            if id_ is None or id_ in Bars.keys():
                id_ = uuid.uuid4()
            if isinstance(text, RTextBase):
                self._text = text.to_json_str()
            else:
                self._text = '"%s"' % str(text).replace('"', '\\"')
            self._id = id_
            self._time = time.time()
            server_instance.execute(f'bossbar add pb:{id_} {self._text}')
            Bars[id_] = self
        else:
            server_instance.logger.info(
                'Bar创建失败！原因：' +
                ("[插件未加载]" if server_instance is None else "") +
                ("[服务端未就绪]" if not if_server_alive else "")
            )
            server_instance.logger.debug('未准备就绪时的Bar创建失败：')
            server_instance.logger.debug(f' - text: "{text}" id: "{id_}"')

    def __del__(self):
        if self.__del_count < 2:
            self.__del_count += 1
            if not self.__deleted:
                server_instance.logger.debug(f'delete_bar:')
                server_instance.execute(f'bossbar remove pb:{self._id}')
                self.__deleted = True
            if self._id in Bars.keys():
                del Bars[self._id]

    def get_time(self):
        """
        获取Bar创建的时间
        创建时，使用的time.time()获取的时间
        :return: 创建时间
        """
        return self._time

    def delete(self):
        """
        从Bars中删除Bar，并将bossbar从minecraft中删除
        """
        del Bars[self._id]
        del self

    def show(self, player):
        """
        设置玩家该玩家能看到这个Bar
        :param player: 玩家名称 或@选择器
        :type player: str
        :return: self
        """
        server_instance.execute(f'bossbar set pb:{self._id} players {player}')
        return self

    def get_id(self):
        """
        获取Bar的ID
        :return: ID
        """
        return self._id

    def text(self, text=None):
        """
        str 设置/获取Bar的标题，双引号会被转义，富文本请用RText
        :param text: 输入设置值 留空则返回标题
        :type text: None, str, RText, RTextList
        :return: 若输入值则返回self 否则返回标题
        """
        if text is not None:
            if text != self._text:
                if isinstance(text, RTextBase):
                    self._text = text.to_json_str()
                else:
                    self._text = '"%s"' % str(text).replace('"', '\\"')
                server_instance.execute(f'bossbar set pb:{self._id} name {self._text}')
            return self
        else:
            return self._text

    def color(self, color=None):
        """
        BarColor 设置/获取Bar的颜色
        :param color: 输入设置值 留空则返回颜色 请务必使用枚举类BarColor
        :type color: None, BarColor
        :return: 若输入值则返回self 否则返回颜色
        """
        if type(color) is BarColor:
            if color != self._color:
                self._color = color
                server_instance.execute(f'bossbar set pb:{self._id} color {color.name.lower()}')
            return self
        else:
            return self._color

    def style(self, style=None):
        """
        BarStyle 设置/获取Bar的样式
        :param style: 输入设置值 留空则返回样式 请务必使用枚举类BarStyle
        :type style: None, BarStyle
        :return: 若输入值则返回self 否则返回样式
        """
        if type(style) is BarStyle:
            if style != self._style:
                self._style = style
                server_instance.execute(f'bossbar set pb:{self._id} style {style.name.lower()}')
            return self
        else:
            return self._style

    def max(self, max_=None):
        """
        int 设置/获取Bar的最大值
        :param max_: 输入设置值 留空则返回最大值 0< max < 2147483647
        :type max_: None, int
        :return: 若输入值则返回self 否则返回最大值
        """
        if type(max_) is int and 2147483647 >= max_ > 0:
            if max_ != self._max:
                self._max = max_
                server_instance.execute(f'bossbar set pb:{self._id} max {max_}')
            return self
        else:
            return self._max

    def value(self, value=None):
        """
        int 设置/获取Bar的值
        :param value: 输入设置值 留空则返回值 0< value < max
        :type value: None, int
        :return: 若输入值则返回self 否则返回值
        """
        if type(value) is int and self._max >= value >= 0:
            if value != self._value:
                self._value = value
                server_instance.execute(f'bossbar set pb:{self._id} value {value}')
            return self
        else:
            return self._value

    def visible(self, visible=None):
        """
        bool 设置/获取Bar的可见性
        :param visible: 输入设置值 留空则返回可见性
        :type visible: None, bool
        :return: 若输入值则返回self 否则返回可见性
        """
        if type(visible) is bool:
            if visible != self._visible:
                self._visible = visible
                server_instance.execute(f'bossbar set pb:{self._id} visible {str(visible).lower()}')
            return self
        else:
            return self._visible


def on_load(server, old_module):
    global server_instance, if_server_alive
    server_instance = server
    if old_module is not None:
        server_instance.logger.debug('检测到重载，检查服务器是否就绪……')
        if server_instance.is_server_running():
            if_server_alive = True
            server_instance.logger.debug('服务器已就绪，更改if_server_alive标志为True')
        else:
            server_instance.logger.debug('服务器未就绪')
        for key in old_module.Bars.keys():
            server.execute(f'bossbar remove pb:{key}')
            server_instance.logger.debug(f'重新向minecraft中加载[progressbar:{key}]')
    if PB_CONFIG['user_interface']['enable']:
        server.add_help_message(PB_CONFIG['user_interface']['prefix'], '进度条')
        server.logger.info('已启动交互界面。')
    server.logger.info('启动完成。')


def on_server_startup(server):
    global if_server_alive,  server_instance
    if_server_alive = True
    server_instance.logger.info(f'服务器端已启动。{"ProgressBar已经启动，Bar创建已解锁。" if server_instance is not None else "ProgressBar未启动，Bar创建暂时锁定。"}')


def on_info(server, info):
    if PB_CONFIG['user_interface']['enable'] and info.is_user:
        args = info.content.split(' ')
        if args[0] == PB_CONFIG['user_interface']['prefix']:
            if len(args) == 1 or args[1] == 'help':
                permission_level = server_instance.get_permission_level(info)
                msg = ''
                for key in PB_CONFIG['user_interface']['sub_command'].keys():
                    if permission_level in PB_CONFIG['user_interface']['sub_command'][key]['use_permission_limit']:
                        msg += '\n%s' % PB_CONFIG['user_interface']['sub_command'][key]['help_msg']
                server_instance.reply(info, '%s%s\n%s' % (
                    PB_CONFIG['user_interface']['help_message_container'][0],
                    msg,
                    PB_CONFIG['user_interface']['help_message_container'][1]
                ))
            elif len(args) in (3, 4) and args[1] == 'timer' and server_instance.get_permission_level(info) in PB_CONFIG['user_interface']['sub_command']['timer']['use_permission_limit']:
                try:
                    t = float(args[2])
                except ValueError as e:
                    server_instance.reply(str(e))
                    return
                if len(args) == 3:
                    p = info.player
                    if not info.is_player:
                        server_instance.reply(info, '在控制台操作时请指定玩家！')
                        return
                else:
                    p = args[3]
                    if p[0] == '@' and server_instance.get_permission_level(info) not in PB_CONFIG['user_interface']['sub_command']['timer']['@a_permission_limit']:
                        server_instance.reply(info, "你没有权限这样做！")
                        return
                wait_bar(wait_time=t, player=p)
            elif len(args) == 2 and args[1] == 'list':
                msg = RTextList(
                    '------ ',
                    RText('当前Bar类有', color=RColor.dark_red),
                    RText(len(Bars), color=RColor.red),
                    RText('个实例', color=RColor.dark_red),
                    ' ------\n',
                )
                for key in Bars.keys():
                    msg = RTextList(
                        msg,
                        RText(
                            Bars[key].text() + ' ',
                            color=BarColor_to_RText[Bars[key].color()]
                        ).set_hover_text(f'pb:{Bars[key].get_id()}'),
                        '创建于：',
                        RText(
                            time.strftime("%X", time.localtime(Bars[key].get_time())),
                            color=RColor.gray,
                            styles=RStyle.italic
                        ).set_hover_text(time.strftime("%Y-%m-%d %X", time.localtime(Bars[key].get_time()))),
                        '\n'
                    )
                server_instance.reply(info, msg)
            else:
                server_instance.reply(info, '未知命令')


def on_server_stop(server, return_code):
    global if_server_alive, server_instance
    if_server_alive = False
    server_instance.logger.info(
        f'服务器端已关闭。{"ProgressBar尽管已经启动，但是Bar创建已被暂时锁定。" if server_instance is not None else "ProgressBar未启动，Bar创建仍将继续锁定。"}')


def on_unload(server):
    global server_instance, Bars
    for key in Bars.keys():
        server_instance.execute(f'bossbar remove pb:{key}')
        server_instance.logger.debug(f'已从minecraft中卸载[pb:{key}]')
    server_instance.logger.info(f'已卸载。')
    server_instance = None


def wait_bar(wait_time, player, text="", color=BarColor.WHITE, style=BarStyle.NOTCHED_10, update_interval=0.5, fall=True):
    """
    设置一个倒计时 函数将在此阻塞至倒计时结束 可替代time.sleep()
    :param wait_time: 等待时间 最小时间单位为1GameTick(0.05s)
    :type wait_time: float, int
    :param player: 显示给指定玩家 输入玩家ID或@选择器
    :type player: str
    :param text: 倒计时文字 可使用占位符：{waite_time}-等待总时间 {wait_left_time}-剩余时间 {wait_passed_time}-已等待时间 如:'请等待§c§l{wait_left_time}§r秒... §c§l{wait_passed_time}§r/§c§l{waite_time}'
    :type text: str
    :param color: 设置Bar的颜色
    :type color: BarColor
    :param style: 设置Bar的样式
    :type style: BarStyle
    :param update_interval: 更新周期 最小时间单位为1GameTick(0.05s)
    :type update_interval: float, int
    :param fall: 计时过程中进度条减少(100%->0%) False:设置增加(0%->100%)
    :type fall: bool
    """
    # 校验参数
    if type(wait_time) not in (int, float):
        try:
            wait_time = float(wait_time)
        except ValueError as e:
            server_instance.logger.debug(f'参数wait_time={wait_time}异常。')
            raise e
    wait_time = round(int((wait_time + 0.025) / 0.05) * 0.05, 2)
    if text in ("", None):
        text = '请等待§c§l{wait_left_time}§r秒... §c§l{wait_passed_time}§r/§c§l{waite_time}'
    if color is not None and type(color) is BarColor:
        color = BarColor.WHITE
    if style is not None and type(style) is BarStyle:
        style = BarStyle.NOTCHED_10
    if type(update_interval) not in (int, float):
        try:
            update_interval = float(update_interval)
        except ValueError as e:
            server_instance.logger.debug(f'参数update_frequency={update_interval}异常。设为默认值0.1。')
            update_interval = 0.1
    update_interval = round(int((update_interval + 0.025) / 0.05) * 0.05, 2)
    if type(fall) is not bool:
        try:
            fall = bool(fall)
        except ValueError as e:
            server_instance.logger.debug(f'参数drop={fall}异常。设为默认值True。')
            fall = True
    # 创建Bar
    waited = 0
    progress_bar = Bar(
        text.replace('{waite_time}', '%.1f' % wait_time)
            .replace('{wait_passed_time}', '%.1f' % waited)
            .replace('{wait_left_time}', '%.1f' % (wait_time - waited))
    )  # text为JSON字符串，要用str.format()需要把输入字符串里JSON的括号给转义了
    progress_bar.value(100).color(color).style(style).show(player)
    # 循环
    while True:
        if waited > wait_time:
            progress_bar.delete()
            break
        val = int(((wait_time-waited)/wait_time if fall else waited/wait_time)*100)
        progress_bar.value(val if val > 0 else 0)
        progress_bar.text(
            text.replace('{waite_time}', '%.1f' % wait_time)
                .replace('{wait_passed_time}', '%.1f' % waited)
                .replace('{wait_left_time}', '%.1f' % (wait_time - waited))
        )
        time.sleep(update_interval)
        waited += update_interval


