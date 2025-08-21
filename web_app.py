# #!/usr/bin/env python3
# """
# Web Application for Secret Manager
# Flask-based web interface for managing secrets
# """
#
# from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# import json
# from datetime import datetime, timedelta
# from secret_manager import SecretManager
# import secrets
#
# app = Flask(__name__)
# app.secret_key = secrets.token_hex(16)
#
# # Global secret manager instance
# secret_manager = None
#
# # Simple user authentication (for demo purposes)
# DEMO_USERS = {
#     "admin": generate_password_hash("admin123"),
#     "user": generate_password_hash("user123")
# }
#
# def init_secret_manager():
#     """Initialize the secret manager"""
#     global secret_manager
#     if not secret_manager:
#         secret_manager = SecretManager("web_secrets.dat