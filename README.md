# 🔐 字符串生成器

一个功能强大的随机字符串生成与管理工具，支持多种格式，提供美观的 Web 界面。

## ✨ 特性

- 🎲 **多种格式支持**：UUID、十六进制、Base64、字母数字、JWT 风格
- 💾 **持久化存储**：使用 SQLite 数据库安全存储
- 🔍 **搜索过滤**：快速查找已保存的字符串
- ✏️ **编辑管理**：重命名、编辑、删除条目
- 📤 **数据导出**：导出为 JSON 格式
- 📋 **一键复制**：快速复制到剪贴板
- ⚙️ **灵活配置**：支持自定义前缀、端口等配置
- 🎨 **Moemail 风格**：致敬 Moemail 的二次元像素风设计
- 🔒 **本地运行**：默认仅监听 127.0.0.1，安全可靠

## 🎨 设计风格

本项目前端设计复刻了 **Moemail** 的艺术风格，打造萌萌哒使用体验：

- **配色方案**：采用经典的 **魅惑紫 (#6200ea)** 作为主色调，搭配极简白/灰背景。
- **字体选择**：引入 **"ZCOOL KuaiLe" (站酷快乐体)**，圆润可爱的中文字体，完美契合二次元主题。
- **图标设计**：全站使用定制的 **SVG 矢量图标**，采用紫色填充/粗线条风格，替代了系统默认的 Emoji，视觉更加统一高级。
- **细节打磨**：圆角卡片、悬停动效、点阵背景纹理，处处体现精致感。

## 📦 支持的格式

| 格式 | 说明 | 示例 |
|------|------|------|
| **UUID 标准格式** | 带连字符的标准 UUID v4 | `prefix-550e8400-e29b-41d4-a716-446655440000` |
| **UUID 十六进制** | 32位十六进制 UUID（无连字符） | `prefix-550e8400e29b41d4a716446655440000` |
| **十六进制** | 纯十六进制字符串（可自定义长度） | `prefix-a1b2c3d4e5f6...` |
| **Base64 URL安全** | URL 安全的 base64 编码 | `prefix-A1b2C3d4E5f6...` |
| **字母数字** | 大小写字母和数字混合 | `prefix-aB1cD2eF3gH4...` |
| **JWT 风格** | 三段式格式（header.payload.signature） | `prefix-xxxxx.yyyyy.zzzzz` |

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 字符串前缀（默认值）
STRING_PREFIX=custom-

# 服务器配置
SERVER_HOST=127.0.0.1
SERVER_PORT=5000

# 调试模式（true/false）
FLASK_DEBUG=false
```

### 3. 启动服务

```bash
python app.py
```

或者使用 Flask 命令：

```bash
flask --app app run
```

### 4. 访问界面

打开浏览器访问：`http://127.0.0.1:5000`（端口根据配置而定）

## 📖 使用说明

### 配置管理

点击右上角的 **⚙️ 配置** 按钮可以修改：

- **字符串前缀**：生成字符串的固定前缀（建议以 `-` 结尾）
- **服务器地址**：监听地址（修改后需重启）
- **服务器端口**：监听端口（修改后需重启）

配置会保存到 `.env` 文件中。

### 生成随机字符串

1. 在左侧面板选择**格式类型**
2. 设置**长度**（如果格式支持）
3. 点击 **🎲 生成随机字符串** 按钮
4. 生成的字符串会显示在结果区域
5. 点击 **📋** 按钮可复制到剪贴板
6. 输入**自定义名称**后点击 **💾 保存** 按钮

### 手动输入字符串

1. 在左侧面板下方找到**手动输入**区域
2. 输入**名称**和**字符串值**
   - 可以包含或不包含前缀（会自动添加）
3. 选择**格式类型**
4. 点击 **💾 保存手动输入** 按钮

### 管理已保存的字符串

在右侧面板可以：

- 🔍 **搜索**：在搜索框输入关键词过滤
- 📋 **复制**：点击复制按钮快速复制值
- ✏️ **编辑**：修改名称或值
- 🗑️ **删除**：删除不需要的条目
- 📤 **导出**：导出所有数据为 JSON 文件
- 🔄 **刷新**：重新加载列表

## 🔧 API 接口

### 获取配置

```http
GET /api/config
```

### 更新配置

```http
POST /api/config
Content-Type: application/json

{
  "prefix": "new-prefix-",
  "host": "127.0.0.1",
  "port": 5000
}
```

### 获取支持的格式

```http
GET /api/formats
```

### 生成随机字符串

```http
POST /api/generate
Content-Type: application/json

{
  "format": "uuid_hex",
  "length": 32
}
```

### 保存字符串

```http
POST /api/entries
Content-Type: application/json

{
  "name": "my_key",
  "value": "custom-abc123",
  "format": "hex",
  "length": 32
}
```

### 获取所有条目

```http
GET /api/entries?search=keyword
```

### 更新条目

```http
PATCH /api/entries/{id}
Content-Type: application/json

{
  "name": "new_name",
  "value": "new_value"
}
```

### 删除条目

```http
DELETE /api/entries/{id}
```

### 导出数据

```http
GET /api/export
```

### 获取统计信息

```http
GET /api/statistics
```

## 📁 项目结构

```
string-generator/
├── app.py              # Flask 主程序
├── generator.py        # 字符串生成器核心逻辑
├── storage.py          # SQLite 数据存储层
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量示例
├── .env                # 环境变量配置（需自行创建）
├── README.md          # 使用文档
├── templates/
│   └── index.html     # Web 界面模板
├── static/
│   ├── app.js         # 前端交互逻辑
│   └── style.css      # 样式文件
└── data/
    └── strings.db     # SQLite 数据库（运行时自动创建）
```

## 🔒 安全说明

- 默认仅监听 `127.0.0.1`，不对外网开放
- 所有输出都经过 HTML 转义，防止 XSS 攻击
- 使用 Python `secrets` 模块生成高质量随机数
- SQLite 提供事务支持，保证数据一致性

## 💡 使用场景

- 🔑 生成 API 密钥
- 🎫 创建访问令牌
- 🆔 生成唯一标识符
- 🧪 测试数据准备
- 📝 密码/密钥管理
- 🔄 迁移其他系统的密钥

## 🛠️ 技术栈

- **后端**：Flask 3.0
- **数据库**：SQLite 3
- **前端**：原生 JavaScript + CSS
- **随机数生成**：Python secrets 模块
- **配置管理**：python-dotenv

## 📝 注意事项

1. **长度参数**：`length` 参数仅控制随机部分的长度，不包含前缀
2. **UUID 格式**：标准 UUID 格式不支持自定义长度，固定为 36 字符（含连字符）
3. **JWT 格式**：长度参数仅控制中间段（payload）的长度
4. **数据备份**：定期导出数据进行备份
5. **配置修改**：修改端口和地址后需要重启服务才能生效
6. **前缀建议**：建议前缀以 `-` 结尾，便于区分

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
