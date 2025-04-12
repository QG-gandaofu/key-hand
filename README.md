# 打字练习应用

这是一个简单的网页打字练习应用，帮助用户练习标准英文打字指法。

## 功能特点

- 显示标准键盘指法图（左手和右手按键用不同颜色标注）
- 随机单词练习
- 自动记录练习进度
- 显示准确率和等级

## 安装步骤

1. 确保已安装Python 3.6或更高版本
2. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```
3. 运行应用：
   ```
   python app.py
   ```
4. 在浏览器中访问：`http://localhost:5000`

## 使用方法

1. 打开网页后，你会看到一个键盘布局图，其中：
   - 粉色按键表示左手操作
   - 绿色按键表示右手操作
2. 在练习区域，系统会随机显示一个单词
3. 在输入框中输入显示的单词
4. 输入正确后，系统会自动显示下一个单词
5. 你的进度（等级、已输入单词数、准确率）会实时显示在页面上

## 数据存储

应用使用SQLite数据库存储用户进度，数据文件名为`typing.db`。 