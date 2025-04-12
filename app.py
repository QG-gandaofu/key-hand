from flask import Flask, render_template, jsonify, request
import random
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# 编程关键词列表
PROGRAMMING_KEYWORDS = [
    'if', 'else', 'for', 'while', 'def', 'class', 'import', 'from',
    'return', 'try', 'except', 'finally', 'with', 'as', 'in', 'is',
    'not', 'and', 'or', 'True', 'False', 'None', 'break', 'continue',
    'pass', 'raise', 'yield', 'async', 'await', 'lambda', 'global',
    'nonlocal', 'del', 'assert', 'print', 'input', 'len', 'range',
    'type', 'str', 'int', 'float', 'bool', 'list', 'dict', 'set',
    'tuple', 'enumerate', 'zip', 'map', 'filter', 'reduce', 'sorted',
    'reversed', 'min', 'max', 'sum', 'abs', 'round', 'divmod', 'pow',
    'bin', 'hex', 'oct', 'chr', 'ord', 'format', 'join', 'split',
    'strip', 'replace', 'find', 'index', 'count', 'startswith',
    'endswith', 'lower', 'upper', 'title', 'capitalize', 'swapcase',
    'isalpha', 'isdigit', 'isalnum', 'isspace', 'islower', 'isupper',
    'istitle', 'append', 'extend', 'insert', 'remove', 'pop', 'clear',
    'index', 'count', 'sort', 'reverse', 'copy', 'update', 'get',
    'keys', 'values', 'items', 'popitem', 'setdefault', 'clear',
    'add', 'remove', 'discard', 'pop', 'clear', 'union', 'intersection',
    'difference', 'symmetric_difference', 'update', 'intersection_update',
    'difference_update', 'symmetric_difference_update', 'issubset',
    'issuperset', 'isdisjoint', 'copy', 'frozenset', 'bytearray',
    'bytes', 'memoryview', 'complex', 'frozenset', 'property', 'staticmethod',
    'classmethod', 'super', 'object', 'type', 'isinstance', 'issubclass',
    'getattr', 'setattr', 'hasattr', 'delattr', 'callable', 'dir', 'vars',
    'locals', 'globals', 'help', 'id', 'hash', 'repr', 'ascii', 'compile',
    'eval', 'exec', 'open', 'close', 'read', 'write', 'seek', 'tell',
    'flush', 'truncate', 'fileno', 'isatty', 'readable', 'writable',
    'closed', 'mode', 'name', 'newlines', 'encoding', 'errors', 'buffer',
    'raw', 'line_buffering', 'closefd', 'opener', 'mode', 'buffering',
    'encoding', 'errors', 'newlines', 'closefd', 'opener', 'mode',
    'buffering', 'encoding', 'errors', 'newlines', 'closefd', 'opener'
]

def load_wordlist():
    """从文件加载词库"""
    try:
        with open('words.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return PROGRAMMING_KEYWORDS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_word')
def get_word():
    words = load_wordlist()
    if not words:
        return jsonify({'error': '词库为空'}), 500
    return jsonify({'word': random.choice(words)})

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
    
    # 创建字母统计表
    c.execute('''
        CREATE TABLE IF NOT EXISTS letter_stats (
            user_id TEXT,
            letter TEXT,
            total INTEGER DEFAULT 0,
            errors INTEGER DEFAULT 0,
            last_practiced TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            average_speed REAL DEFAULT 0,
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