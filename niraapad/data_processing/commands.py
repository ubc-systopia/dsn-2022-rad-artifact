magnetic_stirrer = [{
    "command_name": "IN_NAME",
    "method_name": "read_the_device_name",
    "resp": "device_name"
}, {
    "command_name": "IN_PV_1",
    "method_name": "read_actual_external_sensor_value",
    "resp": "external_sensor_value"
}, {
    "command_name": "IN_PV_2",
    "method_name": "read_actual_hotplate_sensor_value",
    "resp": "hotplate_sensor_value"
}, {
    "command_name": "IN_PV_4",
    "method_name": "read_stirring_speed_value",
    "resp": "stirring_speed_value"
}, {
    "command_name": "IN_PV_5",
    "method_name": "read_velocity_trend_value",
    "resp": "velocity_trend_value"
}, {
    "command_name": "IN_SP_1",
    "method_name": "read_rated_temperature_value",
    "resp": "rated_temperature_value"
}, {
    "command_name": "IN_SP_3",
    "method_name": "read_rated_set_safety_temperature_value",
    "resp": "set_safety_temperature_value"
}, {
    "command_name": "IN_SP_4",
    "method_name": "read_rated_speed_value",
    "resp": "speed_value"
}, {
    "command_name": "OUT_SP_1",
    "method_name": "adjust_the_set_temperature_value",
    "resp": "adjust_the_set_temperature_value"
}, {
    "command_name": "OUT_SP_1 ",
    "method_name": "set_temperature_value",
    "resp": "set_temperature_value"
}, {
    "command_name": "OUT_SP_4",
    "method_name": "adjust_the_set_speed_value",
    "resp": "adjust_the_set_speed_value"
}, {
    "command_name": "OUT_SP_4 ",
    "method_name": "set_speed_value",
    "resp": "set_speed_value"
}, {
    "command_name": "START_1",
    "method_name": "start_the_heater",
    "resp": "start_the_heater"
}, {
    "command_name": "STOP_1",
    "method_name": "stop_the_heater",
    "resp": "stop_the_heater"
}, {
    "command_name": "START_4",
    "method_name": "start_the_motor",
    "resp": "start_the_motor"
}, {
    "command_name": "STOP_4",
    "method_name": "stop_the_motor",
    "resp": "stop_the_motor"
}, {
    "command_name": "RESET",
    "method_name": "switch_to_normal_operating_mode",
    "resp": "switch_to_normal_operating_mode"
}, {
    "command_name": "SET_MODE_A",
    "method_name": "set_operating_mode_a",
    "resp": "set_operating_mode_a"
}, {
    "command_name": "SET_MODE_B",
    "method_name": "set_operating_mode_b",
    "resp": "set_operating_mode_b"
}, {
    "command_name": "SET_MODE_D",
    "method_name": "set_operating_mode_d",
    "resp": "set_operating_mode_d"
}, {
    "command_name": "OUT_SP_12@",
    "method_name": "set_wd_saftey_limit_temperature",
    "resp": "set_wd_saftey_limit_temperature"
}, {
    "command_name": "OUT_SP_42@",
    "method_name": "set_wd_saftey_limit_speed",
    "resp": "set_wd_saftey_limit_speed"
}, {
    "command_name": "OUT_WD1@",
    "method_name": "watchdog_mode_1",
    "resp": "watchdog_mode_1"
}, {
    "command_name": "OUT_WD2@",
    "method_name": "watchdog_mode_2",
    "resp": "watchdog_mode_2"
}]

tecan_cavro = [{
    "command_name": "?",
    "args": None,
    "resp": "position_counts"
}, {
    "command_name": "?2",
    "args": None,
    "resp": "velocity_counts"
}, {
    "command_name": "?6",
    "args": None,
    "resp": "valve_position"
}, {
    "command_name": "?1",
    "args": None,
    "resp": "start_speed"
}, {
    "command_name": "?3",
    "args": None,
    "resp": "cutoff_speed"
}, {
    "command_name": "?76",
    "args": None,
    "resp": "pump_configuration"
}, {
    "command_name": "K",
    "args": "dead_volume",
    "resp": None
}, {
    "command_name": "k",
    "args": "dead_volume",
    "resp": None
}, {
    "command_name": "V",
    "args": "velocity_counts",
    "resp": None
}, {
    "command_name": "L",
    "args": "slope_code",
    "resp": None
}, {
    "command_name": "R",
    "args": None,
    "resp": None
}, {
    "command_name": "U",
    "args": "pump_configuration_value",
    "resp": None
}, {
    "command_name": "Z",
    "args": "plunger_home_speed",
    "resp": None
}, {
    "command_name": "Y",
    "args": "plunger_home_speed",
    "resp": None
}, {
    "command_name": "W",
    "args": None,
    "resp": None
}, {
    "command_name": "w",
    "args": None,
    "resp": None
}, {
    "command_name": "T",
    "args": None,
    "resp": None
}, {
    "command_name": "Q",
    "args": None,
    "resp": None
}, {
    "command_name": "g",
    "args": None,
    "resp": None
}, {
    "command_name": "G",
    "args": "iteration_count",
    "resp": None
}, {
    "command_name": "A",
    "args": "position_counts",
    "resp": None
}, {
    "command_name": "P",
    "args": "delta_counts",
    "resp": None
}, {
    "command_name": "D",
    "args": "delta_counts",
    "resp": None
}, {
    "command_name": "I",
    "args": "position",
    "resp": None
}, {
    "command_name": "O",
    "args": None,
    "resp": None
}]

controller = [{
    "command_name": "PING",
    "flags": None,
    "args": None,
    "resp": "ping"
}, {
    "command_name": "HOME",
    "flags": {
        "C": "if_needed",
        "K": "skip"
    },
    "args": "axes",
    "resp": "home"
}, {
    "command_name": "HALT",
    "flags": None,
    "args": "axes",
    "resp": "halt"
}, {
    "command_name": "BIAS",
    "flags": None,
    "args": "bias",
    "resp": "elbow_bias"
}, {
    "command_name": "CURR",
    "flags": {
        "M": "max"
    },
    "args": "axis, max_current",
    "resp": "axis_current"
}, {
    "command_name": "POS",
    "flags": {
        "C": "C",
        "U": "units",
        "M": "motor"
    },
    "args": "axes",
    "resp": "axis_positions"
}, {
    "command_name": "MVNG",
    "flags": None,
    "args": "axes",
    "resp": "axes_moving"
}, {
    "command_name": "OUTP",
    "flags": None,
    "args": "output, value",
    "resp": "output_state"
}, {
    "command_name": "OUTP",
    "flags": {
        "A": "all"
    },
    "args": "pins",
    "resp": "output_pins_state"
}, {
    "command_name": "JLEN",
    "flags": None,
    "args": "length_offset",
    "resp": "length_offset"
}, {
    "command_name": "SPED",
    "flags": None,
    "args": "velocity, acceleration",
    "resp": "velocity_acceleration"
}, {
    "command_name": "ARM",
    "flags": {
        "V": "velocity",
        "A": "acceleration",
        "R": "relative",
        "X": "X",
        "Y": "Y",
        "Z": "Z",
        "G": "gripper",
        "B": "elbow_bias"
    },
    "args": None,
    "resp": "move_arm_axes_positions"
}, {
    "command_name": "COM",
    "flags": {
        "I": "initialize"
    },
    "args": "port, baudrate",
    "resp": "com_init"
}, {
    "command_name": "COM",
    "flags": {
        "F": "flush"
    },
    "args": "port",
    "resp": "com_flush"
}, {
    "command_name": "COM",
    "flags": {
        "S": "size"
    },
    "args": "port",
    "resp": "no_of_char_input_buffer"
}, {
    "command_name": "COM",
    "flags": {
        "R": "read"
    },
    "args": "port, timeout, num_bytes",
    "resp": "bytes_of_data_read"
}, {
    "command_name": "COM",
    "flags": {
        "W": "write"
    },
    "args": "port, data_length",
    "resp": "com_write"
}]


class magneticstirrer_commands:

    def get_ika_cmd(self, command_name):
        list_of_cmd = magnetic_stirrer
        m_cmd = ""
        resp = ""

        for cmd in list_of_cmd:
            if cmd['command_name'] == command_name:
                resp = cmd['resp']

        return resp

    def write_ika(self, value, commands):
        command_str = value.decode()
        request_cmd = command_str.strip('\r\n')
        global write_ika_cmd

        if "OUT_SP_1" in request_cmd or "OUT_SP_4" in request_cmd:
            if ' ' in request_cmd:
                request_cmd = request_cmd.split(' ')
                commands['command_name'] = request_cmd[0]
                write_ika_cmd = self.get_ika_cmd(commands['command_name'] + ' ')
                commands['value'] = request_cmd[1]
            elif '@' in request_cmd:
                request_cmd = request_cmd.split('@')
                commands['command_name'] = request_cmd[0]
                commands['value'] = request_cmd[1]
                write_ika_cmd = self.get_ika_cmd(commands['command_name'] + '@')
        else:
            commands['command_name'] = request_cmd
            write_ika_cmd = self.get_ika_cmd(commands['command_name'])
            commands['value'] = None

        return commands

    def read_ika(self, value, commands):
        command_str = value.decode()
        if command_str == 'RCT digital' or command_str == 'C-MAG HS7':
            commands[write_ika_cmd] = command_str
        else:
            commands[write_ika_cmd] = command_str.split()[0]
        return commands


class tecancavro_commands:

    def get_cavro_cmd(self, command_name):
        list_of_cmd = tecan_cavro
        m_cmd = ""
        resp = ""
        args = ""

        for cmd in list_of_cmd:
            if cmd['command_name'] == command_name:
                args = cmd['args']
                resp = cmd['resp']

        return args, resp

    def write_cavro(self, value, commands):
        command_str = value
        status_data = command_str[command_str.index(b"\x02"):]
        try:
            end_line = command_str.index(b"R\x03")
        except:
            end_line = command_str.index(b"\x03")

        data = status_data[3:end_line].decode()

        iter = 0
        if '?' not in data:
            for i in range(0, len(data)):
                if iter < len(data):
                    command_name = data[iter]
                    write_cavro_args, write_cavro_resp = self.get_cavro_cmd(
                        command_name)
                    commands["command_name_" + str(i)] = command_name
                    nums = []

                    for j in range(iter, len(data)):
                        try:
                            if write_cavro_args != None and data[j +
                                                                 1].isnumeric():
                                nums.append(data[j + 1])
                                iter = j + 2
                            else:
                                iter = j + 1
                                break
                        except:
                            break

                    if write_cavro_args != None:
                        if len(nums) == 0:
                            commands[write_cavro_args + "_" + str(i)] = None
                        else:
                            commands[write_cavro_args + "_" +
                                     str(i)] = "".join(nums)
                else:
                    break
        else:
            write_cavro_args, write_cavro_resp = self.get_cavro_cmd(data)

        return commands

    def read_ika(self, value, commands):
        command_str = value.decode()
        commands['resp'] = None

        return commands


class controller_commands:

    def get_n9_cmd(self, name, flags, args):
        list_of_cmd = controller
        check = 0
        counter = 2
        com_counter = 4
        m_cmd = ""
        m_flags = {}
        m_args = {}

        for cmd in list_of_cmd:
            #Iterate the commands that are repetitive to get thecorrect one
            if cmd['command_name'] == name:
                if name == "OUTP":
                    if len(flags) == 1:
                        check = 2
                    else:
                        check = 1

                    if check == 2 and counter == 2:
                        counter = counter - 1
                        continue

                elif name == "COM":
                    if list(flags[0].keys())[0] == "W":
                        check = 5
                    elif list(flags[0].keys())[0] == "R":
                        check = 4
                    elif list(flags[0].keys())[0] == "S":
                        check = 3
                    elif list(flags[0].keys())[0] == "F":
                        check = 2
                    elif list(flags[0].keys())[0] == "I":
                        check = 1

                    if check == 5 and (com_counter == 4 or com_counter == 3 or
                                       com_counter == 2 or com_counter == 1):
                        com_counter = com_counter - 1
                        continue
                    elif check == 4 and (com_counter == 4 or com_counter == 3 or
                                         com_counter == 2):
                        com_counter = com_counter - 1
                        continue
                    elif check == 3 and (com_counter == 4 or com_counter == 3):
                        com_counter = com_counter - 1
                        continue
                    elif check == 2 and com_counter == 4:
                        com_counter = com_counter - 1
                        continue

                if cmd['flags'] is not None:
                    cmd_flags = cmd["flags"]
                    for i in range(0, len(flags)):
                        m_flags[cmd_flags[list(flags[i].keys())[0]]] = list(
                            flags[i].values())[0]

                if cmd['args'] is not None:
                    cmd_args = cmd['args'].split(", ")
                    if (len(args) != 0):
                        m_args[cmd_args[0]] = args[0]
                    for i in range(1, len(args)):
                        if len(cmd_args) < len(args):
                            m_args[cmd_args[0]] = m_args[
                                cmd_args[0]] + "," + args[i]
                        else:
                            m_args[cmd_args[i]] = args[i]

                break

        return m_cmd, m_flags, m_args

    def write_n9(self, value, commands):
        command_str = value.decode()
        request_cmd = command_str.strip('\r').split(' ')

        if (request_cmd[0] == "PING"):
            commands['command_name'] = 'PING'
            return commands

        commands['network_address'] = request_cmd[0]
        commands['99'] = request_cmd[1]
        commands['crc'] = request_cmd[2]
        commands['sequence_no'] = request_cmd[3]
        commands['command_name'] = request_cmd[4]
        global write_centrifuge_cmd
        write_centrifuge_cmd = commands['command_name']

        i = 5
        commands['flags'] = []
        if (len(request_cmd) > 5):
            while ('/' in request_cmd[i]):
                flags = {}
                flags[request_cmd[i][1]] = request_cmd[i + 1]
                commands['flags'].append(flags)
                i = i + 2
                if (i == len(request_cmd)):
                    break

        commands['args'] = []
        while (len(request_cmd) - 1 >= i):
            commands['args'].append(request_cmd[i])
            i = i + 1

        m_com, m_flags, m_args = self.get_n9_cmd(commands['command_name'],
                                                 commands['flags'],
                                                 commands['args'])

        commands['command'] = m_com
        commands['flags'] = m_flags
        commands['args'] = m_args

        return commands

    def read_n9(value, commands):
        list_of_cmd = controller
        resp = ""
        for cmd in list_of_cmd:
            if write_centrifuge_cmd == cmd['command_name']:
                resp = cmd['resp']
        response, crc = value.rsplit(b'\r')
        response = response.strip(b'\r\x00')
        crc = crc.decode()
        commands[resp] = response.decode().strip(' ')
        commands['crc'] = crc

        return commands
