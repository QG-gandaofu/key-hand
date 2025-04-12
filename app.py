from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import os
import sqlite3

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

@app.route('/update_letter_stats', methods=['POST'])
def update_letter_stats():
    try:
        data = request.json
        user_id = data.get('user_id')
        letter = data.get('letter')
        is_correct = data.get('is_correct')
        
        if not all([user_id, letter, is_correct is not None]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        conn = sqlite3.connect('typing.db')
        c = conn.cursor()
        
        # 更新字母统计
        c.execute('''
            INSERT INTO letter_stats (user_id, letter, total, errors)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(user_id, letter) DO UPDATE SET
            total = total + 1,
            errors = errors + ?
        ''', (user_id, letter, 0 if is_correct else 1, 0 if is_correct else 1))
        
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_letter_stats', methods=['GET'])
def get_letter_stats():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'Missing user_id parameter'}), 400
        
        conn = sqlite3.connect('typing.db')
        c = conn.cursor()
        
        # 获取错误率最高的前5个字母
        c.execute('''
            SELECT letter, 
                   ROUND(errors * 100.0 / total, 2) as error_rate,
                   total as total_typed,
                   errors
            FROM letter_stats
            WHERE user_id = ? AND total > 0
            ORDER BY error_rate DESC, total DESC
            LIMIT 5
        ''', (user_id,))
        
        stats = [{'letter': row[0], 'error_rate': row[1], 'total_typed': row[2], 'errors': row[3]} 
                for row in c.fetchall()]
        
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def init_db():
    conn = sqlite3.connect('typing.db')
    c = conn.cursor()
    
    # 创建用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            best_speed REAL,
            total_practice_time INTEGER,
            total_words INTEGER,
            correct_words INTEGER
        )
    ''')
    
    # 创建字母统计表
    c.execute('''
        CREATE TABLE IF NOT EXISTS letter_stats (
            user_id TEXT,
            letter TEXT,
            total INTEGER DEFAULT 0,
            errors INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, letter)
        )
    ''')
    
    conn.commit()
    conn.close()

# 确保数据库表存在
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True) 