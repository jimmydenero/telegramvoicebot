import sqlite3
import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class AIKnowledgeDatabase:
    def __init__(self, db_path: str = "./ai_knowledge.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create knowledge table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create conversation history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_knowledge(self, title: str, content: str, category: str = None, tags: List[str] = None):
        """Add new AI knowledge to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tags_json = json.dumps(tags) if tags else None
        
        cursor.execute('''
            INSERT INTO ai_knowledge (title, content, category, tags)
            VALUES (?, ?, ?, ?)
        ''', (title, content, category, tags_json))
        
        conn.commit()
        conn.close()
    
    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for relevant AI knowledge based on query."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Search in title and content
        cursor.execute('''
            SELECT id, title, content, category, tags
            FROM ai_knowledge
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY updated_at DESC
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        
        results = []
        for row in cursor.fetchall():
            tags = json.loads(row[4]) if row[4] else []
            results.append({
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'category': row[3],
                'tags': tags
            })
        
        conn.close()
        return results
    
    def get_all_knowledge(self) -> List[Dict]:
        """Get all AI knowledge from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, category, tags, created_at, updated_at
            FROM ai_knowledge
            ORDER BY updated_at DESC
        ''')
        
        results = []
        for row in cursor.fetchall():
            tags = json.loads(row[4]) if row[4] else []
            results.append({
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'category': row[3],
                'tags': tags,
                'created_at': row[5],
                'updated_at': row[6]
            })
        
        conn.close()
        return results
    
    def save_conversation(self, user_id: int, message: str, response: str):
        """Save conversation history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversation_history (user_id, message, response)
            VALUES (?, ?, ?)
        ''', (user_id, message, response))
        
        conn.commit()
        conn.close()
    
    def get_user_conversation_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get conversation history for a specific user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT message, response, timestamp
            FROM conversation_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'message': row[0],
                'response': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return results
