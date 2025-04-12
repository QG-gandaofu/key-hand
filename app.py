from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///typing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义用户进度模型
class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True)
    level = db.Column(db.Integer, default=1)
    words_typed = db.Column(db.Integer, default=0)
    accuracy = db.Column(db.Float, default=0.0)

# 编程关键词列表
PROGRAMMING_KEYWORDS = [
    'abstract', 'as', 'assert', 'async', 'await', 'auto', 'break', 'case', 'catch',
    'class', 'const', 'continue', 'debugger', 'default', 'delegate', 'delete', 'do',
    'dynamic', 'elif', 'else', 'enum', 'export', 'extends', 'extern', 'false',
    'final', 'finally', 'float', 'for', 'friend', 'from', 'func', 'global', 'goto',
    'if', 'implements', 'import', 'in', 'include', 'init', 'inline', 'instanceof',
    'interface', 'internal', 'is', 'let', 'loop', 'match', 'module', 'namespace',
    'new', 'nil', 'not', 'null', 'operator', 'override', 'package', 'pass', 'private',
    'protected', 'public', 'raise', 'readonly', 'ref', 'require', 'return', 'self',
    'static', 'struct', 'super', 'switch', 'this', 'throw', 'throws', 'true', 'try',
    'type', 'typeof', 'using', 'var', 'virtual', 'void', 'volatile', 'where', 'while',
    'with', 'yield'
]

# 用户进度数据
user_progress = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_word')
def get_word():
    # 随机选择一个关键词
    word = random.choice(PROGRAMMING_KEYWORDS)
    return jsonify({'word': word})

@app.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.json
    user_id = data.get('user_id')
    accuracy = data.get('accuracy', 0)
    
    if user_id not in user_progress:
        user_progress[user_id] = {
            'level': 1,
            'words_typed': 0,
            'accuracy': 0
        }
    
    user_progress[user_id]['words_typed'] += 1
    user_progress[user_id]['accuracy'] = accuracy
    
    # 根据准确率调整等级
    if accuracy >= 95:
        user_progress[user_id]['level'] = min(user_progress[user_id]['level'] + 1, 10)
    elif accuracy < 80:
        user_progress[user_id]['level'] = max(user_progress[user_id]['level'] - 1, 1)
    
    return jsonify({
        'success': True,
        'level': user_progress[user_id]['level']
    })

# 确保数据库表存在
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 