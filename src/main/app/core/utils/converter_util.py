import re
import inflect
from typing import Optional


class ClassNameConverter:
    def __init__(self):
        self.p = inflect.engine()

    def to_singular(self, word: str) -> str:
        """将复数形式转为单数形式 (使用inflect包)"""
        singular = self.p.singular_noun(word)
        return singular if singular else word

    def to_plural(self, word: str) -> str:
        """将单数形式转为复数形式 (使用inflect包)"""
        return self.p.plural(word)

    def to_camel(self, s: str) -> str:
        """转换为小驼峰命名 (camelCase)"""
        s = self._clean_string(s)
        if not s:
            return s
        words = s.split("_")
        return words[0].lower() + "".join(
            word.capitalize() for word in words[1:]
        )

    def to_pascal(self, s: str) -> str:
        """转换为大驼峰命名 (PascalCase)"""
        s = self._clean_string(s)
        if not s:
            return s
        words = s.split("_")
        return "".join(word.capitalize() for word in words)

    def to_snake(self, s: str) -> str:
        """转换为蛇形命名 (snake_case)"""
        s = self._clean_string(s)
        if not s:
            return s
        s = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
        s = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s)
        return s.lower()

    def to_kebab(self, s: str) -> str:
        """转换为烤肉串命名 (kebab-case)"""
        return self.to_snake(s).replace("_", "-")

    def to_upper(self, s: str) -> str:
        """转换为全大写"""
        return s.upper()

    def to_lower(self, s: str) -> str:
        """转换为全小写"""
        return s.lower()

    def convert(self, s: str, style: str) -> Optional[str]:
        """通用转换方法"""
        if not s:
            return s

        style = style.lower()
        if style in ("singular", "sing"):
            return self.to_singular(s)
        elif style in ("plural", "plur"):
            return self.to_plural(s)
        elif style in ("camel", "camelcase"):
            return self.to_camel(s)
        elif style in ("pascal", "pascalcase", "pascal_case"):
            return self.to_pascal(s)
        elif style in ("snake", "snakecase", "snake_case"):
            return self.to_snake(s)
        elif style in ("kebab", "kebabcase", "kebab-case"):
            return self.to_kebab(s)
        elif style in ("upper", "uppercase"):
            return self.to_upper(s)
        elif style in ("lower", "lowercase"):
            return self.to_lower(s)
        else:
            raise ValueError(f"Unknown style: {style}")

    def _clean_string(self, s: str) -> str:
        """清理字符串，去除特殊字符"""
        # 替换连字符和空格为下划线
        s = re.sub(r"[-\s]", "_", s)
        # 移除非字母数字和下划线
        s = re.sub(r"[^a-zA-Z0-9_]", "", s)
        return s


# 示例使用
if __name__ == "__main__":
    converter = ClassNameConverter()

    # 测试单复数转换
    words = [
        "child",
        "person",
        "ox",
        "mouse",
        "matrix",
        "index",
        "user",
        "data",
    ]
    print("=== Singular/Plural Conversion ===")
    for word in words:
        plural = converter.to_plural(word)
        singular = converter.to_singular(plural)
        print(f"{word} -> plural: {plural} -> singular: {singular}")

    # 测试命名风格转换
    examples = [
        "userAccount",
        "UserAccount",
        "user_account",
        "user-account",
        "USER_ACCOUNT",
        "user",
        "users",
        "child",
    ]

    print("\n=== Naming Style Conversion ===")
    for example in examples:
        print(f"\nOriginal: {example}")
        print(f"Singular: {converter.convert(example, 'singular')}")
        print(f"Plural: {converter.convert(example, 'plural')}")
        print(f"CamelCase: {converter.convert(example, 'camel')}")
        print(f"PascalCase: {converter.convert(example, 'pascal')}")
        print(f"snake_case: {converter.convert(example, 'snake')}")
        print(f"kebab-case: {converter.convert(example, 'kebab')}")
        print(f"UPPERCASE: {converter.convert(example, 'upper')}")
        print(f"lowercase: {converter.convert(example, 'lower')}")
