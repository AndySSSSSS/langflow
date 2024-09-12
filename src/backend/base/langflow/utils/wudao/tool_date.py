from dateutil import parser


def normalize_date(date_str):
    try:
        # 解析日期字符串为 datetime 对象
        date_obj = parser.parse(date_str)
        # 格式化为 YYYY-MM-DD
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None

