# db.py - Database Management Module

import sqlite3
import hashlib
import os
from datetime import datetime

class Database:
    """Database handler for user authentication and data storage"""
    
    def __init__(self, db_name='student_predictor.db'):
        """Initialize database connection"""
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create and return database connection"""
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                predicted_score REAL NOT NULL,
                grade TEXT,
                prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                feature_data TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password, full_name=''):
        """Create a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, email, password, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, hashed_password, full_name))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            return {'success': True, 'user_id': user_id, 'message': 'User created successfully'}
        
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return {'success': False, 'message': 'Username already exists'}
            elif 'email' in str(e):
                return {'success': False, 'message': 'Email already exists'}
            else:
                return {'success': False, 'message': 'User creation failed'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, username, email, full_name
                FROM users
                WHERE username = ? AND password = ?
            ''', (username, hashed_password))
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                cursor.execute('''
                    UPDATE users
                    SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user['id'],))
                conn.commit()
                
                conn.close()
                return {
                    'success': True,
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'full_name': user['full_name']
                    }
                }
            else:
                conn.close()
                return {'success': False, 'message': 'Invalid username or password'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, full_name, created_at, last_login
                FROM users
                WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'success': True,
                    'user': dict(user)
                }
            else:
                return {'success': False, 'message': 'User not found'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def save_prediction(self, user_id, predicted_score, grade, feature_data=''):
        """Save prediction to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO predictions (user_id, predicted_score, grade, feature_data)
                VALUES (?, ?, ?, ?)
            ''', (user_id, predicted_score, grade, feature_data))
            
            conn.commit()
            prediction_id = cursor.lastrowid
            conn.close()
            
            return {'success': True, 'prediction_id': prediction_id}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_user_predictions(self, user_id, limit=10):
        """Get user's prediction history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, predicted_score, grade, prediction_date
                FROM predictions
                WHERE user_id = ?
                ORDER BY prediction_date DESC
                LIMIT ?
            ''', (user_id, limit))
            
            predictions = cursor.fetchall()
            conn.close()
            
            return {
                'success': True,
                'predictions': [dict(p) for p in predictions]
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def update_user_profile(self, user_id, full_name=None, email=None):
        """Update user profile"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if full_name:
                cursor.execute('''
                    UPDATE users
                    SET full_name = ?
                    WHERE id = ?
                ''', (full_name, user_id))
            
            if email:
                cursor.execute('''
                    UPDATE users
                    SET email = ?
                    WHERE id = ?
                ''', (email, user_id))
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': 'Profile updated successfully'}
        
        except sqlite3.IntegrityError:
            return {'success': False, 'message': 'Email already exists'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verify old password
            old_hashed = self.hash_password(old_password)
            cursor.execute('''
                SELECT id FROM users
                WHERE id = ? AND password = ?
            ''', (user_id, old_hashed))
            
            if not cursor.fetchone():
                conn.close()
                return {'success': False, 'message': 'Old password is incorrect'}
            
            # Update to new password
            new_hashed = self.hash_password(new_password)
            cursor.execute('''
                UPDATE users
                SET password = ?
                WHERE id = ?
            ''', (new_hashed, user_id))
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': 'Password changed successfully'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Total predictions
            cursor.execute('''
                SELECT COUNT(*) as total FROM predictions WHERE user_id = ?
            ''', (user_id,))
            total = cursor.fetchone()['total']
            
            # Average score
            cursor.execute('''
                SELECT AVG(predicted_score) as avg_score FROM predictions WHERE user_id = ?
            ''', (user_id,))
            avg_score = cursor.fetchone()['avg_score'] or 0
            
            # Highest score
            cursor.execute('''
                SELECT MAX(predicted_score) as max_score FROM predictions WHERE user_id = ?
            ''', (user_id,))
            max_score = cursor.fetchone()['max_score'] or 0
            
            conn.close()
            
            return {
                'success': True,
                'stats': {
                    'total_predictions': total,
                    'average_score': round(avg_score, 2),
                    'highest_score': round(max_score, 2)
                }
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}