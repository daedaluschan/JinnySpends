
log_file_size_lmt = 10485760
log_file_count_lmt = 3

conv_time_out = 20

cat_list = ["Domestic", "Cook", "Drive", "Jinny", "Mortgage", "Bill", "Meal", "Misc", "Transport",
            "Leisure", "DanSan", "Clothes", "Apartment"]

log_i_dont_know_u = "唔識你（{}），唔同你講嘢。"
msg_i_dont_know_u = "唔識你，唔同你講嘢。"
msg_dont_understand = "唔明，請再試過啦。"

button_new_item = "記錄新洗費"
button_show_3D = "三天內洗費"
regex_show_3D = button_show_3D

keyboard_start=[[button_new_item],[button_show_3D]]

msg_greeting = "你好，這是可愛小 Jinny Telegram 機械人。"

il_button_clone = "Clone"
cb_data_clone = "clone_{}"
il_button_edit = "Edit"
cb_data_edit = "edit_{}"
il_button_delete = "Delete"
cb_data_delete = "del_{}"

msg_input_date = "請輸入日子（YYYYMMDD）。"

button_today = "今日"
button_ytd = "尋日"
button_previous_2d = "前日"
regex_date_options = "{}|{}|{}".format(button_today, button_ytd, button_previous_2d)
button_use_calendar = "用小日曆"

keyboard_date = [[button_today, button_ytd, button_previous_2d], [button_use_calendar]]

regex_date_input_pattern = ".*(\d{4}).*(\d{2}).*(\d{2}).*"

msg_picked_date = "日期係: {}"
msg_which_cat = "請選擇洗費類別。"
