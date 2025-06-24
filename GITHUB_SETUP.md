# GitHub 颜色编码文件设置指南

## 概述
为了让用户不需要手动上传颜色编码文件，我们将这些文件托管在GitHub上，应用会自动下载。

## 需要托管的文件
1. `color_en_cn_match.xlsx` - iPhone颜色对照表
2. `ipad_color_en_cn_match.xlsx` - iPad颜色对照表

## 设置步骤

### 1. 创建GitHub仓库
1. 在GitHub上创建一个新的公开仓库
2. 仓库名称建议：`market-scanner-assets` 或类似名称

### 2. 上传颜色编码文件
1. 将 `color_en_cn_match.xlsx` 和 `ipad_color_en_cn_match.xlsx` 上传到仓库的根目录
2. 确保文件在 `main` 分支上

### 3. 获取Raw URL
对于每个文件，获取其raw URL：
- 格式：`https://raw.githubusercontent.com/用户名/仓库名/main/文件名.xlsx`
- 例如：`https://raw.githubusercontent.com/your-username/market-scanner-assets/main/color_en_cn_match.xlsx`

### 4. 更新应用中的URL
在 `streamlit_app.py` 文件中，更新以下URL：

```python
# 将这些URL替换为你的实际GitHub仓库URL
IPHONE_COLOR_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/color_en_cn_match.xlsx"
IPAD_COLOR_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/ipad_color_en_cn_match.xlsx"
```

### 5. 测试
1. 运行应用
2. 检查iPhone和iPad标签页是否显示"✅ 颜色对照表已自动下载"
3. 测试完整的识别流程

## 注意事项
- 确保GitHub仓库是公开的，这样应用才能访问文件
- 如果文件较大，考虑使用Git LFS
- 定期更新颜色编码文件时，只需要在GitHub上更新文件即可，用户无需重新下载应用

## 故障排除
如果下载失败：
1. 检查网络连接
2. 验证GitHub URL是否正确
3. 确认仓库是公开的
4. 检查文件是否存在于指定路径 