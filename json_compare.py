import json
import os
import argparse
from datetime import datetime
import logging
from pathlib import Path


def setup_logging():
    """设置日志记录"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"json_compare_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(), timestamp


def generate_social_update_log(results, other_folder):
    """生成用于微信/QQ等社交媒体的更新日志"""
    update_dir = Path("updates")
    update_dir.mkdir(exist_ok=True)
    
    # 提取文件夹名作为版本号，假设格式为YYYYMMDD
    version = os.path.basename(other_folder)
    
    update_file = update_dir / f"social_update_log_{version}.txt"
    
    # 收集新增模型
    new_models = []
    for file_name, differences in results.items():
        if file_name == "model.json" and differences["only_in_other"]:
            new_models.extend(list(differences["only_in_other"].keys()))
    
    # 从completion.json中也收集新增模型
    for file_name, differences in results.items():
        if file_name == "completion.json" and differences["only_in_other"]:
            comp_models = list(differences["only_in_other"].keys())
            # 只添加不在model.json中的模型
            for model in comp_models:
                if model not in new_models:
                    new_models.append(model)
    
    # 收集价格变动
    price_changes = []
    if "model.json" in results and results["model.json"]["different_values"]:
        for key, values in results["model.json"]["different_values"].items():
            old_price = values["tuzi_value"]
            new_price = values["other_value"]
            change_pct = ((new_price - old_price) / old_price) * 100
            
            if abs(change_pct) >= 1:  # 仅显示变动超过1%的价格
                direction = "上升" if change_pct > 0 else "下降"
                price_changes.append({
                    "model": key,
                    "old_price": old_price,
                    "new_price": new_price,
                    "change_pct": abs(change_pct),
                    "direction": direction
                })
    
    # 生成更新日志文本
    with open(update_file, 'w', encoding='utf-8') as f:
        f.write(f"{version} API站更新说明\n")
        
        # 新增模型
        if new_models:
            f.write("1、新增模型\n")
            for model in sorted(new_models):
                f.write(f'  "{model}"\n')
        
        # 价格调整
        if price_changes:
            f.write("2、价格调整\n")
            for change in sorted(price_changes, key=lambda x: abs(x["change_pct"]), reverse=True):
                arrow = "↑" if change["direction"] == "上升" else "↓"
                f.write(f'  {change["model"]} {change["direction"]} {change["change_pct"]:.2f}% ({change["old_price"]} → {change["new_price"]})\n')
        
        # 如果没有新增模型和价格变动，显示一条友好的消息
        if not new_models and not price_changes:
            f.write("本次更新没有新增模型和价格变动\n")
    
    return update_file


def generate_html_update_log(results, other_folder):
    """生成用于网站弹窗的HTML格式更新日志"""
    update_dir = Path("updates")
    update_dir.mkdir(exist_ok=True)
    
    # 提取文件夹名作为版本号，假设格式为YYYYMMDD
    version = os.path.basename(other_folder)
    
    update_file = update_dir / f"html_update_log_{version}.html"
    
    # 收集新增模型
    new_models = []
    for file_name, differences in results.items():
        if file_name == "model.json" and differences["only_in_other"]:
            new_models.extend(list(differences["only_in_other"].keys()))
    
    # 从completion.json中也收集新增模型
    for file_name, differences in results.items():
        if file_name == "completion.json" and differences["only_in_other"]:
            comp_models = list(differences["only_in_other"].keys())
            # 只添加不在model.json中的模型
            for model in comp_models:
                if model not in new_models:
                    new_models.append(model)
    
    # 收集价格变动
    price_changes = []
    if "model.json" in results and results["model.json"]["different_values"]:
        for key, values in results["model.json"]["different_values"].items():
            old_price = values["tuzi_value"]
            new_price = values["other_value"]
            change_pct = ((new_price - old_price) / old_price) * 100
            
            if abs(change_pct) >= 1:  # 仅显示变动超过1%的价格
                direction = "上升" if change_pct > 0 else "下降"
                price_changes.append({
                    "model": key,
                    "old_price": old_price,
                    "new_price": new_price,
                    "change_pct": abs(change_pct),
                    "direction": direction
                })
    
    # 生成HTML
    with open(update_file, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* 重置样式 */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.5;
        }}
        /* 主容器 - 适应弹窗限制 */
        .update-container {{
            width: 100%;
            max-height: 80vh; /* 视窗高度的80% */
            overflow-y: auto; /* 添加垂直滚动条 */
            font-family: Arial, sans-serif;
            padding: 12px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        .update-title {{
            color: #333;
            border-bottom: 1px solid #ddd;
            padding-bottom: 8px;
            margin-bottom: 12px;
            font-size: 18px;
            text-align: center;
        }}
        .update-section {{
            margin-bottom: 15px;
        }}
        .update-section-title {{
            font-weight: bold;
            color: #444;
            margin-bottom: 8px;
            font-size: 16px;
        }}
        /* 模型列表样式 - 更紧凑的布局 */
        .model-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 8px;
        }}
        .model-item {{
            background-color: #e8f4f8;
            border-radius: 3px;
            padding: 4px 8px;
            font-family: monospace;
            font-size: 13px;
            white-space: nowrap;
        }}
        /* 表格样式 - 自适应宽度 */
        .price-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            table-layout: fixed;
        }}
        .price-table th, .price-table td {{
            padding: 6px;
            text-align: left;
            border-bottom: 1px solid #ddd;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
        .price-table th:first-child, .price-table td:first-child {{
            width: 40%;
        }}
        .price-table th:not(:first-child), .price-table td:not(:first-child) {{
            width: 20%;
            text-align: center;
        }}
        .price-table th {{
            background-color: #f2f2f2;
            position: sticky;
            top: 0;
        }}
        .price-up {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .price-down {{
            color: #2ecc71;
            font-weight: bold;
        }}
        /* 弹窗内部滚动样式优化 */
        .update-container::-webkit-scrollbar {{
            width: 6px;
        }}
        .update-container::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 3px;
        }}
        .update-container::-webkit-scrollbar-thumb {{
            background: #c1c1c1;
            border-radius: 3px;
        }}
        .update-container::-webkit-scrollbar-thumb:hover {{
            background: #a8a8a8;
        }}
    </style>
</head>
<body>
    <div class="update-container">
        <h2 class="update-title">{version} API站更新说明</h2>
""")
        
        # 新增模型
        if new_models:
            f.write("""        <div class="update-section">
            <div class="update-section-title">1. 新增模型</div>
            <div class="model-list">
""")
            for model in sorted(new_models):
                f.write(f'                <div class="model-item">{model}</div>\n')
            f.write("""            </div>
        </div>
""")
        
        # 价格调整
        if price_changes:
            f.write("""        <div class="update-section">
            <div class="update-section-title">2. 价格调整</div>
            <table class="price-table">
                <tr>
                    <th>模型</th>
                    <th>原价格</th>
                    <th>新价格</th>
                    <th>变动</th>
                </tr>
""")
            for change in sorted(price_changes, key=lambda x: abs(x["change_pct"]), reverse=True):
                css_class = "price-up" if change["direction"] == "上升" else "price-down"
                arrow = "↑" if change["direction"] == "上升" else "↓"
                f.write(f"""                <tr>
                    <td>{change["model"]}</td>
                    <td>{change["old_price"]}</td>
                    <td>{change["new_price"]}</td>
                    <td class="{css_class}">{arrow} {change["change_pct"]:.2f}%</td>
                </tr>
""")
            f.write("""            </table>
        </div>
""")
        
        # 如果没有新增模型和价格变动，显示一条友好的消息
        if not new_models and not price_changes:
            f.write("""        <div class="update-section">
            <div style="text-align:center; margin:20px 0; color:#666;">
                本次更新没有新增模型和价格变动
            </div>
        </div>
""")
        
        f.write("""    </div>
</body>
</html>""")
    
    return update_file


def generate_markdown_report(results, tuzi_folder, other_folder, add_missing_data, update_different_values, timestamp):
    """生成Markdown格式的报告"""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    
    report_file = report_dir / f"json_compare_report_{timestamp}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# JSON文件比较报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 比较参数\n\n")
        f.write(f"- 基准文件夹: `{tuzi_folder}`\n")
        f.write(f"- 比较文件夹: `{other_folder}`\n")
        f.write(f"- 添加缺失数据: {'是' if add_missing_data else '否'}\n")
        f.write(f"- 更新不同值: {'是' if update_different_values else '否'}\n\n")
        
        f.write(f"## 比较结果摘要\n\n")
        f.write("| 文件名 | 仅在基准文件夹中的键 | 仅在比较文件夹中的键 | 值不同的键 |\n")
        f.write("|--------|----------------------|----------------------|------------|\n")
        
        for file_name, differences in results.items():
            f.write(f"| {file_name} | {len(differences['only_in_tuzi'])} | {len(differences['only_in_other'])} | {len(differences['different_values'])} |\n")
        
        f.write("\n## 详细比较结果\n\n")
        
        for file_name, differences in results.items():
            f.write(f"### {file_name}\n\n")
            
            if differences['only_in_tuzi']:
                f.write("#### 仅在基准文件夹中的键\n\n")
                f.write("```json\n")
                json_str = json.dumps(differences['only_in_tuzi'], ensure_ascii=False, indent=2)
                f.write(json_str)
                f.write("\n```\n\n")
            
            if differences['only_in_other']:
                f.write("#### 仅在比较文件夹中的键\n\n")
                f.write("```json\n")
                json_str = json.dumps(differences['only_in_other'], ensure_ascii=False, indent=2)
                f.write(json_str)
                f.write("\n```\n\n")
            
            if differences['different_values']:
                f.write("#### 值不同的键\n\n")
                f.write("| 键 | 基准文件夹中的值 | 比较文件夹中的值 |\n")
                f.write("|----|-----------------|-----------------|\n")
                
                for key, values in differences['different_values'].items():
                    tuzi_value = str(values['tuzi_value']).replace('|', '\\|')
                    other_value = str(values['other_value']).replace('|', '\\|')
                    f.write(f"| {key} | {tuzi_value} | {other_value} |\n")
                
                f.write("\n")
    
    return report_file


def load_json_file(file_path):
    """加载JSON文件并返回数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"无法加载文件 {file_path}: {e}")
        return None


def compare_json_files(tuzi_data, other_data, file_name):
    """比较两个JSON文件并返回差异"""
    differences = {
        "only_in_tuzi": {},
        "only_in_other": {},
        "different_values": {}
    }
    
    # 检查tuzi中有但其他文件夹中没有的键
    for key in tuzi_data:
        if key not in other_data:
            differences["only_in_tuzi"][key] = tuzi_data[key]
    
    # 检查其他文件夹中有但tuzi中没有的键
    for key in other_data:
        if key not in tuzi_data:
            differences["only_in_other"][key] = other_data[key]
        elif tuzi_data[key] != other_data[key]:
            # 值不同的键
            differences["different_values"][key] = {
                "tuzi_value": tuzi_data[key],
                "other_value": other_data[key]
            }
    
    return differences


def merge_json_files(tuzi_data, differences, add_missing_data=True, update_different_values=False):
    """合并JSON数据，根据差异更新tuzi数据"""
    merged_data = tuzi_data.copy()
    
    # 添加其他文件夹中有但tuzi中没有的键
    if add_missing_data:
        for key, value in differences["only_in_other"].items():
            merged_data[key] = value
            logging.info(f"添加了新键: {key} = {value}")
    
    # 更新两个文件夹中都有但值不同的键
    if update_different_values:
        for key, values in differences["different_values"].items():
            merged_data[key] = values["other_value"]
            logging.info(f"更新了值: {key} = {values['other_value']} (原值: {values['tuzi_value']})")
    
    return merged_data


def save_json_file(data, file_path):
    """保存JSON数据到文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"已保存文件: {file_path}")
        return True
    except Exception as e:
        logging.error(f"保存文件 {file_path} 时出错: {e}")
        return False


def process_json_files(tuzi_folder, other_folder, json_files, add_missing_data=True, update_different_values=False):
    """处理多个JSON文件，比较和合并差异"""
    logger = logging.getLogger()
    results = {}
    
    for file_name in json_files:
        tuzi_file_path = os.path.join(tuzi_folder, file_name)
        other_file_path = os.path.join(other_folder, file_name)
        
        if not os.path.exists(tuzi_file_path):
            logger.warning(f"Tuzi文件夹中不存在文件: {file_name}")
            continue
            
        if not os.path.exists(other_file_path):
            logger.warning(f"指定文件夹中不存在文件: {file_name}")
            continue
        
        logger.info(f"正在处理文件: {file_name}")
        
        # 加载JSON数据
        tuzi_data = load_json_file(tuzi_file_path)
        other_data = load_json_file(other_file_path)
        
        if tuzi_data is None or other_data is None:
            continue
        
        # 比较文件
        differences = compare_json_files(tuzi_data, other_data, file_name)
        results[file_name] = differences
        
        # 输出差异
        logger.info(f"文件 {file_name} 的差异:")
        logger.info(f"  仅在Tuzi中的键数量: {len(differences['only_in_tuzi'])}")
        logger.info(f"  仅在其他文件夹中的键数量: {len(differences['only_in_other'])}")
        logger.info(f"  值不同的键数量: {len(differences['different_values'])}")
        
        # 详细记录差异
        if differences["only_in_tuzi"]:
            logger.info("仅在Tuzi中的键:")
            for key, value in differences["only_in_tuzi"].items():
                logger.info(f"  {key}: {value}")
        
        if differences["only_in_other"]:
            logger.info("仅在其他文件夹中的键:")
            for key, value in differences["only_in_other"].items():
                logger.info(f"  {key}: {value}")
        
        if differences["different_values"]:
            logger.info("值不同的键:")
            for key, values in differences["different_values"].items():
                logger.info(f"  {key}:")
                logger.info(f"    Tuzi中的值: {values['tuzi_value']}")
                logger.info(f"    其他文件夹中的值: {values['other_value']}")
        
        # 合并数据并保存（如果需要）
        should_update = (add_missing_data and differences["only_in_other"]) or (update_different_values and differences["different_values"])
        if should_update:
            merged_data = merge_json_files(tuzi_data, differences, add_missing_data, update_different_values)
            
            # 备份原始文件
            backup_path = f"{tuzi_file_path}.bak"
            try:
                with open(tuzi_file_path, 'r', encoding='utf-8') as src, open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                logger.info(f"已备份原始文件到: {backup_path}")
            except Exception as e:
                logger.error(f"备份文件时出错: {e}")
                continue
            
            # 保存更新后的文件
            save_json_file(merged_data, tuzi_file_path)
    
    return results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="比较两个文件夹中的JSON文件并合并差异")
    parser.add_argument("--tuzi", default="tuzi", help="Tuzi文件夹路径")
    parser.add_argument("--other", required=True, help="要比较的另一个文件夹路径")
    parser.add_argument("--no-add", action="store_true", help="不添加缺失的数据")
    parser.add_argument("--update", action="store_true", help="更新两个文件夹中都有但值不同的键")
    args = parser.parse_args()
    
    # 设置日志
    logger, timestamp = setup_logging()
    
    tuzi_folder = args.tuzi
    other_folder = args.other
    add_missing_data = not args.no_add
    update_different_values = args.update
    
    logger.info(f"开始比较文件夹: {tuzi_folder} 和 {other_folder}")
    logger.info(f"添加缺失数据: {add_missing_data}")
    logger.info(f"更新不同值: {update_different_values}")
    
    # 检查文件夹是否存在
    if not os.path.isdir(tuzi_folder):
        logger.error(f"Tuzi文件夹不存在: {tuzi_folder}")
        return
    
    if not os.path.isdir(other_folder):
        logger.error(f"指定的其他文件夹不存在: {other_folder}")
        return
    
    # 获取tuzi文件夹中的JSON文件
    json_files = [f for f in os.listdir(tuzi_folder) if f.endswith('.json')]
    
    if not json_files:
        logger.warning(f"Tuzi文件夹中没有找到JSON文件: {tuzi_folder}")
        return
    
    logger.info(f"找到以下JSON文件: {', '.join(json_files)}")
    
    # 处理JSON文件
    results = process_json_files(tuzi_folder, other_folder, json_files, add_missing_data, update_different_values)
    
    # 生成Markdown报告
    report_file = generate_markdown_report(results, tuzi_folder, other_folder, add_missing_data, update_different_values, timestamp)
    logger.info(f"已生成Markdown报告: {report_file}")
    
    # 生成微信/QQ更新日志
    social_update_file = generate_social_update_log(results, other_folder)
    logger.info(f"已生成社交媒体更新日志: {social_update_file}")
    
    # 生成HTML更新日志
    html_update_file = generate_html_update_log(results, other_folder)
    logger.info(f"已生成HTML更新日志: {html_update_file}")
    
    logger.info("处理完成")


if __name__ == "__main__":
    main() 