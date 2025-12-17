"""
字符串生成器核心模块
支持多种格式的随机字符串生成
"""

import uuid
import secrets
import base64


class StringGenerator:
    """随机字符串生成器"""

    def __init__(self, prefix="custom-"):
        self.prefix = prefix

    def generate(self, format_type="uuid_hex", length=32):
        """
        生成随机字符串

        Args:
            format_type: 格式类型 (uuid, uuid_hex, hex, base64url, alnum, jwt)
            length: 主体部分长度（不包含前缀）

        Returns:
            生成的字符串
        """
        if format_type == "uuid":
            return self._generate_uuid()
        elif format_type == "uuid_hex":
            return self._generate_uuid_hex()
        elif format_type == "hex":
            return self._generate_hex(length)
        elif format_type == "base64url":
            return self._generate_base64url(length)
        elif format_type == "alnum":
            return self._generate_alnum(length)
        elif format_type == "jwt":
            return self._generate_jwt_like(length)
        else:
            raise ValueError(f"不支持的格式类型: {format_type}")

    def _generate_uuid(self):
        """生成标准 UUID 格式（带连字符）"""
        return f"{self.prefix}{uuid.uuid4()}"

    def _generate_uuid_hex(self):
        """生成 UUID 十六进制格式（32位，无连字符）"""
        return f"{self.prefix}{uuid.uuid4().hex}"

    def _generate_hex(self, length):
        """生成纯十六进制字符串"""
        # 每个字节生成2个十六进制字符
        num_bytes = (length + 1) // 2
        random_bytes = secrets.token_bytes(num_bytes)
        hex_string = random_bytes.hex()[:length]
        return f"{self.prefix}{hex_string}"

    def _generate_base64url(self, length):
        """生成 URL 安全的 base64 字符串"""
        # base64 编码后每3字节变成4字符，所以需要 length * 3 / 4 字节
        num_bytes = (length * 3 + 3) // 4
        random_bytes = secrets.token_bytes(num_bytes)
        # 使用 URL 安全的 base64 编码（替换 +/ 为 -_，去除 padding）
        b64_string = base64.urlsafe_b64encode(random_bytes).decode('ascii').rstrip('=')
        return f"{self.prefix}{b64_string[:length]}"

    def _generate_alnum(self, length):
        """生成字母+数字混合字符串"""
        # 使用 secrets.choice 从字母数字字符集中随机选择
        import string
        alphabet = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(alphabet) for _ in range(length))
        return f"{self.prefix}{random_string}"

    def _generate_jwt_like(self, payload_length=32):
        """
        生成 JWT 风格的三段式字符串
        格式: prefix-header.payload.signature

        Args:
            payload_length: 中间段（payload）的长度
        """
        # JWT 的 header 通常较短（约20-30字符）
        header_bytes = secrets.token_bytes(12)
        header = base64.urlsafe_b64encode(header_bytes).decode('ascii').rstrip('=')

        # payload 部分使用指定长度
        payload_bytes = secrets.token_bytes((payload_length * 3 + 3) // 4)
        payload = base64.urlsafe_b64encode(payload_bytes).decode('ascii').rstrip('=')[:payload_length]

        # signature 部分固定长度（约40-50字符）
        signature_bytes = secrets.token_bytes(32)
        signature = base64.urlsafe_b64encode(signature_bytes).decode('ascii').rstrip('=')

        return f"{self.prefix}{header}.{payload}.{signature}"

    @staticmethod
    def get_supported_formats():
        """获取支持的所有格式"""
        return {
            "uuid": {
                "name": "UUID 标准格式",
                "description": "带连字符的标准 UUID v4",
                "example": "prefix-550e8400-e29b-41d4-a716-446655440000",
                "supports_length": False
            },
            "uuid_hex": {
                "name": "UUID 十六进制",
                "description": "32位十六进制 UUID（无连字符）",
                "example": "prefix-550e8400e29b41d4a716446655440000",
                "supports_length": False
            },
            "hex": {
                "name": "十六进制",
                "description": "纯十六进制字符串",
                "example": "prefix-a1b2c3d4e5f6...",
                "supports_length": True
            },
            "base64url": {
                "name": "Base64 URL安全",
                "description": "URL 安全的 base64 编码",
                "example": "prefix-A1b2C3d4E5f6...",
                "supports_length": True
            },
            "alnum": {
                "name": "字母数字",
                "description": "大小写字母和数字混合",
                "example": "prefix-aB1cD2eF3gH4...",
                "supports_length": True
            },
            "jwt": {
                "name": "JWT 风格",
                "description": "三段式 JWT 格式（header.payload.signature）",
                "example": "prefix-xxxxx.yyyyy.zzzzz",
                "supports_length": True,
                "length_note": "长度仅控制中间段（payload）"
            }
        }


if __name__ == "__main__":
    # 测试代码
    gen = StringGenerator()

    print("=== 字符串生成器测试 ===\n")

    for format_type in ["uuid", "uuid_hex", "hex", "base64url", "alnum", "jwt"]:
        result = gen.generate(format_type, length=32)
        print(f"{format_type:12} : {result}")
