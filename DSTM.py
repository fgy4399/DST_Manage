import tkinter as tk
from tkinter import ttk, scrolledtext
import paramiko
import re
from item import item_dict



class SSHClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("饥荒管理工具 v0.0.5")
        self.root.geometry('670x475+100+100')
        self.IP = ["175.24.174.247", "47.103.61.217"]
        """"左边布局"""
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT,anchor=tk.N,padx=5,pady=5)

        # 物品名称和对应的值
        self.item_dict = item_dict

        #服务器连接布局
        self.net_frame = tk.LabelFrame(self.left_frame,text='服务器连接',padx=5,pady=5)
        self.net_frame.pack()
        self.label_host = ttk.Label(self.net_frame, text="地址:").pack(anchor=tk.W)
        self.host_var = tk.StringVar()
        self.combobox_host = ttk.Combobox(self.net_frame, textvariable=self.host_var, values=self.IP)
        self.combobox_host.set("175.24.174.247")  # 设置默认值
        self.combobox_host.bind("<FocusIn>", self.enable_editing)  # 绑定事件
        self.host_editable = False  # 判断是否可以编辑
        self.combobox_host.pack(anchor=tk.E)

        self.label_port = ttk.Label(self.net_frame, text="端口:").pack(anchor=tk.W)
        self.port_var = tk.StringVar()
        self.combobox_port = ttk.Combobox(self.net_frame, textvariable=self.port_var, values=["22","1080"])
        self.combobox_port.set("22")  # 设置默认值
        self.combobox_port.bind("<FocusIn>", self.enable_editing)  # 绑定事件
        self.port_editable = False  # 判断是否可以编辑
        self.combobox_port.pack(fill=tk.X)

        self.label_user = ttk.Label(self.net_frame, text="用户:").pack(anchor=tk.W)
        self.user_var = tk.StringVar()
        self.combobox_user = ttk.Combobox(self.net_frame, textvariable=self.user_var, values=["root","ubuntu"])
        self.combobox_user.set("root")  # 设置默认值
        self.combobox_user.bind("<FocusIn>", self.enable_editing)  # 绑定事件
        self.user_editable = False  # 判断是否可以编辑
        self.combobox_user.pack(fill=tk.X)

        self.label_password = ttk.Label(self.net_frame, text="密码:").pack(anchor=tk.W)
        self.entry_password = ttk.Entry(self.net_frame, show="*")
        self.entry_password.pack(fill=tk.X)

        #信息发送布局
        self.wup_frame = tk.LabelFrame(self.left_frame, text='信息发送', padx=5, pady=5)
        self.wup_frame.pack()

        self.label_quantity = ttk.Label(self.wup_frame, text="数量:").pack(anchor=tk.W)
        self.entry_quantity = ttk.Entry(self.wup_frame)
        self.entry_quantity.pack(fill=tk.X)

        self.label_character = ttk.Label(self.wup_frame, text="人物:").pack(anchor=tk.W)
        self.character_var = tk.StringVar()
        self.combobox_character = ttk.Combobox(self.wup_frame, textvariable=self.character_var, values=["KU_dNLoogx4"])
        self.combobox_character.set("KU_dNLoogx4")  # 设置默认值,玩家id,KU打头
        self.combobox_character.bind("<FocusIn>", self.enable_editing)  # 绑定事件
        self.character_editable = False  # 判断是否可以编辑
        self.combobox_character.pack(fill=tk.X)

        self.label_item = ttk.Label(self.wup_frame, text="物品:").pack(anchor=tk.W)
        self.item_var = tk.StringVar()
        self.combobox_item = ttk.Combobox(self.wup_frame, textvariable=self.item_var, values=list(self.item_dict.keys()))
        self.combobox_item.set(list(self.item_dict.keys())[0])  # 设置默认值
        self.combobox_item.bind("<FocusIn>", self.enable_editing)  # 绑定事件
        self.item_editable = False  # 判断是否可以编辑
        self.combobox_item.pack(fill=tk.X)

        #服务器连接按钮
        self.button_connect = ttk.Button(self.net_frame, text="连接", command=self.connect_ssh).pack(anchor=tk.CENTER,padx=5,pady=5)
        #信息发送按钮
        self.button_execute = ttk.Button(self.wup_frame, text="发送", command=self.execute_command).pack(anchor=tk.CENTER,padx=5,pady=5)

        """右边布局"""
        # 创建数据日志文本框
        self.right_frame = tk.Frame(self.root, )
        self.right_frame.pack(anchor=tk.N,padx=5,pady=5)

        #self.info_frame = tk.Frame(self.right_frame)
        #self.info_frame.pack()
        self.info_frame = tk.LabelFrame(self.right_frame, text='数据日志', padx=5, pady=5)
        self.info_frame.pack()

        self.log_text = scrolledtext.ScrolledText(self.info_frame, wrap=tk.WORD, width=62,height=26)
        self.log_text.pack(side=tk.LEFT,fill=tk.X)

        #创建其他功能布局
        self.qit_frame = tk.LabelFrame(self.right_frame, text='其他功能')
        self.qit_frame.pack()

        # 添加按钮
        self.button_get_logs = ttk.Button(self.qit_frame, text="获取玩家列表", command=self.get_logs)
        self.button_get_logs.pack(side=tk.LEFT, padx=(13,2), pady=10)

        self.log_dir_var = tk.StringVar()
        self.label_log_dir = ttk.Label(self.qit_frame).pack(side=tk.LEFT, pady=10)
        self.combobox_log_dir = ttk.Combobox(self.qit_frame, textvariable=self.log_dir_var,values=["Master","Caves"], width=12)
        self.combobox_log_dir.set("Master")
        self.combobox_log_dir.pack(side=tk.LEFT, padx=(0,10), pady=(10,10))


        self.button_fuhuo = ttk.Button(self.qit_frame, text="复活玩家",command=self.resurrect_player)
        self.button_fuhuo.pack(side=tk.LEFT, padx=(25,0), pady=10)
        self.entry_player_id = ttk.Entry(self.qit_frame, width=15)
        self.entry_player_id.pack(side=tk.LEFT, padx=(5,13), pady=10)



    ###复活玩家
    def resurrect_player(self):
        player_id = self.entry_player_id.get()
        lua_command = f'UserToPlayer("{player_id}"):PushEvent("respawnfromghost")'
        lua_execution_command = f'screen -S dst -p 0 -X stuff \'{lua_command} \\n\''
        self.ssh_client.exec_command(lua_execution_command)

    ###查找server_log.txt文件路径
    def find_server_log_path(self):
        # 检查是否已经建立 SSH 连接
        if not hasattr(self, 'ssh_client') or self.ssh_client.get_transport() is None:
            return None

        # 文件名
        log_dir = self.combobox_log_dir.get()

        # 执行 find 命令
        find_command = f'find ~ -type f -wholename "*/{log_dir}/server_log.txt" 2>/dev/null || echo "File not found"'

        try:
            # 执行命令
            stdin, stdout, stderr = self.ssh_client.exec_command(find_command)

            # 获取命令执行结果
            result = stdout.read().decode('utf-8')
            print(result.strip())
            # 如果找到文件，返回文件路径，否则返回 None
            if result.strip():
                return result.strip()
            else:
                return None

        except Exception as e:
            # 处理异常
            log_message = ">>> " + "Failed to connect: {}".format(str(e))
            self.log_text.insert(tk.END, log_message + "\n")
            return None

    ###获取饥荒服务器日志，找出所有玩家
    def get_logs(self):
        try:
            # 检查是否已经建立 SSH 连接
            if not hasattr(self, 'ssh_client') or self.ssh_client.get_transport() is None:
                self.log_text.insert(tk.END, ">>> 请先建立 SSH 连接\n")
                return

            # 构建 Lua 命令
            lua_command = 'for i, v in ipairs(TheNet:GetClientTable()) do ' \
                          'print(string.format("%s %d %s %s %s %s ", "id", i-1, ' \
                          'string.format("%03d", v.playerage), v.userid, v.name, v.prefab)) end'

            # 将 Lua 命令嵌入到具体的命令字符串中
            lua_execution_command = f'screen -S dst -p 0 -X stuff \'{lua_command} \\n\''

            # 执行 Lua 命令
            stdin, stdout, stderr = self.ssh_client.exec_command(lua_execution_command)
            lua_result = stdout.read().decode('utf-8')

            # 获取日志的最后50行

            log_path = self.find_server_log_path()  # 替换为实际的日志路径
            tail_command = f'tail -n 30 {log_path}'


            # 执行获取日志的命令
            stdin, stdout, stderr = self.ssh_client.exec_command(tail_command)
            log_result = stdout.read().decode('utf-8')


            # 输出到数据日志框
            self.log_text.insert(tk.END, "\n")
            #print(log_result.splitlines())
            player_info_list = self.get_players(log_result.splitlines())

            # 输出结果
            if player_info_list:
                self.log_text.insert(tk.END, ">>> 找到的所有玩家信息：\n")
                for player_info in player_info_list:
                    self.log_text.insert(tk.END, f'--> {player_info}\n')
            else:
                self.log_text.insert(tk.END, ">>> 未找到任何玩家信息\n")

        except Exception as e:
            log_message = ">>> 执行 Lua 命令及获取玩家信息失败: {}".format(str(e))
            self.log_text.insert(tk.END, log_message + "\n")

    def connect_ssh(self):
        # 获取用户输入的信息
        host = self.host_var.get()

        port = int(self.combobox_port.get()) #if self.combobox_port.get() else 22  # 默认为22端口
        username = self.combobox_user.get()
        password = self.entry_password.get()
        #print(host,port,username,password)

        # 创建SSH客户端
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # 连接服务器
            self.ssh_client.connect(host, port=port, username=username, password=password)
            log_message = ">>> " + "Connected to {}@{}:{}".format(username, host, port) + "\n" + ">>> " + "连接服务器成功！！！"
            self.log_text.insert(tk.END, log_message + "\n")
        except Exception as e:
            log_message = ">>> " + "Failed to connect: {}".format(str(e))
            self.log_text.insert(tk.END, log_message + "\n")

    @staticmethod
    def get_players(dst_logs):
        player_info_list = []
        seen_player_ages = set()

        for line in dst_logs:
            match = re.match(r'\[(.+?)\]: id (\d+) (\d{3}) (\S+) (\S+) (\S+)', line)
            if match and "Host" not in match.group(5):

                Ku_Id = match.group(4)

                # 检查PlayerAge是否已经存在，如果不存在则添加到结果列表和集合中
                if Ku_Id not in seen_player_ages:
                    seen_player_ages.add(Ku_Id)

                    player_info = {

                        'Id': match.group(2),
                        'Days': match.group(3),
                        'KuId': Ku_Id,
                        'Name': match.group(5),
                        'Role': match.group(6)
                    }
                    player_info_list.append(player_info)

        return player_info_list

    def execute_command(self):
        # 获取用户输入的参数
        quantity = self.entry_quantity.get()
        character = self.combobox_character.get()
        item_name = self.combobox_item.get()
        item = self.item_dict.get(item_name, item_name)  # 如果不在下拉框中，直接使用输入的值

        # 构建命令字符串
        command = f'screen -S dst -p 0 -X stuff \'for i, v in pairs(AllPlayers) do for i=1,{quantity} do if v ~= nil then if (v.userid == "{character}") then v.components.inventory:GiveItem(SpawnPrefab("{item}")) end end end end \\n\''

        try:
            # 执行命令
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            result = stdout.read().decode('utf-8')
            log_message = ">>> " + quantity + "个" + item + " 发送成功！"
            self.log_text.insert(tk.END, log_message + "\n")
        except Exception as e:
            log_message = ">>> " + "Failed to execute command: {}".format(str(e))
            self.log_text.insert(tk.END, log_message + "\n")

    def enable_editing(self, event):
        # 允许手动输入
        if event.widget == self.combobox_host:
            self.host_editable = True
        elif event.widget == self.combobox_character:
            self.character_editable = True
        elif event.widget == self.combobox_item:
            self.item_editable = True
        elif event.widget == self.combobox_port:
            self.port_editable = True
        elif event.widget == self.combobox_user:
            self.user_editable = True


        event.widget.configure(state="normal")
        event.widget.unbind("<FocusIn>")  # 解除事件绑定

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHClientApp(root)
    root.mainloop()
