from flask import request, session, jsonify
import requests
import json
from config import CLERK_SECRET_KEY, CLERK_JWKS_URL
from jose import jwt, jwk
import logging

logger = logging.getLogger(__name__)

class ClerkAuth:
    def __init__(self):
        self.clerk_secret_key = CLERK_SECRET_KEY
        self.jwks_url = CLERK_JWKS_URL
        self.jwks = None
        
    def get_jwks(self):
        """Fetch JWKS from Clerk"""
        if not self.jwks:
            try:
                response = requests.get(self.jwks_url)
                self.jwks = response.json()
            except Exception as e:
                logger.error(f"Failed to fetch JWKS: {e}")
                return None
        return self.jwks
    
    def verify_jwt(self, token):
        """Verify JWT token using Clerk's JWKS"""
        try:
            # Get JWKS
            jwks = self.get_jwks()
            if not jwks:
                return None
            
            # Decode token header to get kid
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')
            
            if not kid:
                return None
            
            # Find the key in JWKS
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == kid:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
                    break
            
            if not rsa_key:
                return None
            
            # Verify and decode token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=['RS256'],
                audience='https://your-clerk-instance.clerk.accounts.dev',
                issuer='https://clerk.your-instance.clerk.accounts.dev'
            )
            
            return payload
            
        except Exception as e:
            logger.error(f"JWT verification error: {e}")
            return None
    
    def verify_user(self):
        """Verify user authentication"""
        try:
            # Check if user is already logged in
            if 'user_id' in session and session.get('authenticated'):
                return session['user_id']
            
            # Get JWT from Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return None
            
            token = auth_header.replace('Bearer ', '')
            
            # Verify JWT
            payload = self.verify_jwt(token)
            if not payload:
                return None
            
            user_id = payload.get('sub')  # User ID from JWT
            if user_id:
                # Store in session
                session['user_id'] = user_id
                session['authenticated'] = True
                session['user_email'] = payload.get('email', '')
                return user_id
            
            return None
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
    
    def login_required(self, func):
        """Decorator to require authentication"""
        def wrapper(*args, **kwargs):
            user_id = self.verify_user()
            if not user_id:
                # Return JSON response for API endpoints
                if request.path.startswith('/api/') or request.is_json:
                    return jsonify({'error': 'Authentication required'}), 401
                # Redirect for web pages
                return redirect('/login')
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__  # Important for Flask
        return wrapper
    
    def get_user_info(self, user_id):
        """Get user information from Clerk API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.clerk_secret_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"https://api.clerk.dev/v1/users/{user_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None
    
    def logout(self):
        """Clear session data"""
        session.clear()