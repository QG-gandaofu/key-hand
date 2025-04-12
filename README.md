# Key-Hand 打字练习应用

一个现代化的英文打字练习应用，专注于编程关键词的练习，帮助用户提高打字速度和准确性。

## 功能特点

- 🎯 编程关键词练习
- ⌨️ 实时键盘可视化
- 👆 手指位置提示
- 📊 字母统计与分析
- 🌙 深色/浅色主题切换
- ⏱️ 打字速度统计
- 📈 错误率分析

## 技术栈

- Python 3.x
- Flask
- SQLite
- HTML5/CSS3/JavaScript

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Key-Hand.git
cd Key-Hand
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 初始化数据库：
```bash
python app.py
```

5. 运行应用：
```bash
python app.py
```

应用将在 http://localhost:5000 启动。

## 使用说明

1. 打开浏览器访问 http://localhost:5000
2. 开始打字练习：
   - 系统会随机显示编程关键词
   - 实时显示当前字母对应的手指位置
   - 错误输入会重置当前单词
3. 查看统计：
   - 实时显示打字速度（WPM）
   - 显示最佳速度
   - 显示练习时间
   - 分析错误率最高的字母

## 自定义词库

您可以通过编辑 `words.txt` 文件来自定义练习词库。每行一个单词，系统会自动加载。

## 主题切换

- 点击右上角的"切换主题"按钮可以手动切换深色/浅色主题
- 勾选"自动切换"可以根据系统时间自动切换主题

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License 