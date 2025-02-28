# One-api/new-api 倍率 比较与合并工具

一个用于比较和合并 JSON 文件的工具，特别适用于 API 定价模型的管理和更新通知。

## 功能特点

- 比较两个文件夹中的 JSON 文件，识别新增、缺失和值不同的键
- 可选择性地将新数据合并到基准文件中
- 生成详细的 Markdown 格式比较报告

  ![Markdown格式比较报告](https://ourzhishi.top:7602/apps/sharingpath/nextcloud/public/tu-zi/api-tuzi/github-readme/02.png)

- 生成用于社交媒体的简洁更新通知

  ![社交媒体简介更新日志](https://ourzhishi.top:7602/apps/sharingpath/nextcloud/public/tu-zi/api-tuzi/github-readme/03.png)

- 生成美观的 HTML 格式更新通知，适合网站弹窗显示

  ![HTML通知图片](https://ourzhishi.top:7602/apps/sharingpath/nextcloud/public/tu-zi/api-tuzi/github-readme/01.png)

- 全面的日志记录



## 安装

1. 克隆仓库：

```bash
git clone https://github.com/wangjueszu/api-tuzi.git
cd api-tuzi
```

2. 无需特殊依赖，使用标准 Python 库

3. 如果要使用示例数据进行测试，可以将示例数据复制到工作目录：

```bash
# 复制示例基准数据（如果工作目录中没有 tuzi 文件夹）
cp -r examples/tuzi .

# 复制示例比较数据
cp -r examples/20250101 .
```

## 使用方法

基本用法：

```bash
python json_compare.py --other <比较文件夹>
```

其中：
- 默认基准文件夹为 `tuzi`
- `<比较文件夹>` 是包含要比较的 JSON 文件的文件夹路径

### 命令行参数

```
--tuzi        基准文件夹路径（默认为 "tuzi"）
--other       要比较的另一个文件夹路径（必需）
--no-add      不添加缺失的数据（默认会添加）
--update      更新两个文件夹中都有但值不同的键（默认不更新）
```

### 示例

```bash
# 比较 tuzi 和 20250101 文件夹，并将新数据添加到 tuzi 中
python json_compare.py --other 20250101

# 比较文件夹但不合并任何数据（仅生成报告）
python json_compare.py --other 20250101 --no-add

# 比较并更新已有键的值
python json_compare.py --other 20250101 --update
```

## 输出文件

程序运行后将生成以下输出：

1. **日志文件**：`logs/json_compare_[时间戳].log`
2. **Markdown 报告**：`reports/json_compare_report_[时间戳].md`
3. **社交媒体更新日志**：`updates/social_update_log_[版本号].txt`
4. **HTML 更新日志**：`updates/html_update_log_[版本号].html`

其中的[版本号]取自比较文件夹的名称。

## 项目结构

```
.
├── examples/             # 示例数据
│   ├── tuzi/             # 基准数据示例
│   └── 20250101/         # 比较数据示例
├── logs/                 # 日志文件目录
├── reports/              # 生成的报告目录
├── updates/              # 更新日志目录
├── json_compare.py       # 主程序
├── LICENSE               # 许可证
└── README.md             # 说明文档
```

## 数据格式

该工具设计用于比较具有类似结构的 JSON 文件。示例数据格式：

```json
{
    "model-name-1": 1.0,
    "model-name-2": 2.5
}
```

其中键是模型名称，值是相关的数值（如定价）。

## 许可证

MIT

## 贡献

欢迎通过提交 issue 或 pull request 来贡献代码。请确保在提交前测试您的代码。 