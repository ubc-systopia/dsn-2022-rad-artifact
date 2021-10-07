magnetic_stirrer = [
        {
            "command_name" : "IN_NAME",
            "method_name" : "read_the_device_name",
            "resp" : "device_name"
        },
        {
            "command_name" : "IN_PV_1",
            "method_name" : "read_actual_external_sensor_value",
            "resp" : "external_sensor_value"
        },
        {
            "command_name" : "IN_PV_2",
            "method_name" : "read_actual_hotplate_sensor_value",
            "resp" : "hotplate_sensor_value"
        },
        {
            "command_name" : "IN_PV_4",
            "method_name" : "read_stirring_speed_value",
            "resp" : "stirring_speed_value"
        },
        {
            "command_name" : "IN_PV_5",
            "method_name" : "read_velocity_trend_value",
            "resp" : "velocity_trend_value"
        },
        {
            "command_name" : "IN_SP_1",
            "method_name" : "read_rated_temperature_value",
            "resp" : "rated_temperature_value"
        },
        {
            "command_name" : "IN_SP_3",
            "method_name" : "read_rated_set_safety_temperature_value",
            "resp" : "set_safety_temperature_value"
        },
        {
            "command_name" : "IN_SP_4",
            "method_name" : "read_rated_speed_value",
            "resp" : "speed_value"
        },
        {
            "command_name" : "OUT_SP_1",
            "method_name" : "adjust_the_set_temperature_value",
            "resp" : "adjust_the_set_temperature_value"
        },
        {
            "command_name" : "OUT_SP_1 ",
            "method_name" : "set_temperature_value",
            "resp" : "set_temperature_value"
        },
        {
            "command_name" : "OUT_SP_4",
            "method_name" : "adjust_the_set_speed_value",
            "resp" : "adjust_the_set_speed_value"
        },
        {
            "command_name" : "OUT_SP_4 ",
            "method_name" : "set_speed_value",
            "resp" : "set_speed_value"
        },
        {
            "command_name" : "START_1",
            "method_name" : "start_the_heater",
            "resp" : "start_the_heater"
        },
        {
            "command_name" : "STOP_1",
            "method_name" : "stop_the_heater",
            "resp" : "stop_the_heater"
        },
        {
            "command_name" : "START_4",
            "method_name" : "start_the_motor",
            "resp" : "start_the_motor"
        },
        {
            "command_name" : "STOP_4",
            "method_name" : "stop_the_motor",
            "resp" : "stop_the_motor"
        },
        {
            "command_name" : "RESET",
            "method_name" : "switch_to_normal_operating_mode",
            "resp" : "switch_to_normal_operating_mode"
        },
        {
            "command_name" : "SET_MODE_A",
            "method_name" : "set_operating_mode_a",
            "resp" : "set_operating_mode_a"
        },
        {
            "command_name" : "SET_MODE_B",
            "method_name" : "set_operating_mode_b",
            "resp" : "set_operating_mode_b"
        },
        {
            "command_name" : "SET_MODE_D",
            "method_name" : "set_operating_mode_d",
            "resp" : "set_operating_mode_d"
        },
        {
            "command_name" : "OUT_SP_12@",
            "method_name" : "set_wd_saftey_limit_temperature",
            "resp" : "set_wd_saftey_limit_temperature"
        },
        {
            "command_name" : "OUT_SP_42@",
            "method_name" : "set_wd_saftey_limit_speed",
            "resp" : "set_wd_saftey_limit_speed"
        },
        {
            "command_name" : "OUT_WD1@",
            "method_name" : "watchdog_mode_1",
            "resp" : "watchdog_mode_1"
        },
        {
            "command_name" : "OUT_WD2@",
            "method_name" : "watchdog_mode_2",
            "resp" : "watchdog_mode_2"
        }
]


class magneticstirrer_commands:

    def get_ika_cmd(self, command_name):
        list_of_cmd = magnetic_stirrer
        m_cmd = ""
        resp = ""

        for cmd in list_of_cmd:
            if cmd["command_name"] == command_name:
                resp = cmd["resp"]

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


