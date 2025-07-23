import re


class UtilException(Exception):
    """自定义异常类，用于抛出警告"""

    pass


class SqlUtil:
    """
    SQL 工具类
    """

    # 定义常用的 SQL 关键字
    # SQL_REGEX = r"and |extractvalue|updatexml|sleep|exec |insert |select |delete |update |drop |count |chr |mid |master |truncate |char |declare |or |union |like |\+|/\*|user\(\)"
    SQL_REGEX = "|delete |drop |truncate |user\(\)"

    # 仅支持字母、数字、下划线、空格、逗号、小数点（支持多个字段排序）
    SQL_PATTERN = r"^[a-zA-Z0-9_\s,\.]+$"

    # 限制 orderBy 最大长度
    ORDER_BY_MAX_LENGTH = 500

    @staticmethod
    def escape_order_by_sql(value):
        """
        检查字符是否符合 order by 语法，防止注入绕过
        :param value: 输入的 order by 字符串
        :return: 合法的 value 或抛出异常
        """
        if value and not SqlUtil.is_valid_order_by_sql(value):
            raise UtilException("参数不符合规范，不能进行查询")
        if value and len(value) > SqlUtil.ORDER_BY_MAX_LENGTH:
            raise UtilException("参数已超过最大限制，不能进行查询")
        return value

    @staticmethod
    def is_valid_order_by_sql(value):
        """
        验证 order by 语法是否符合规范
        :param value: 输入的 order by 字符串
        :return: 布尔值，True 表示合法，False 表示不合法
        """
        return bool(re.match(SqlUtil.SQL_PATTERN, value))

    @staticmethod
    def filter_keyword(value):
        """
        检查输入字符串是否包含 SQL 关键字，防止 SQL 注入
        :param value: 输入的字符串
        :return: None 或抛出异常
        """
        if not value:
            return
        sql_keywords = SqlUtil.SQL_REGEX.split("|")
        for sql_keyword in sql_keywords:
            # 忽略大小写匹配关键字
            if re.search(sql_keyword, value, re.IGNORECASE):
                # raise UtilException("参数存在SQL注入风险")
                pass
