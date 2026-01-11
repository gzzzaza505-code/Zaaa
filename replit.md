# Replit.md

## Overview

This is a Discord bot built with Python that provides server management (destructive) capabilities. The bot uses discord.py for Discord API integration and includes a command-line interface with colorama for styled terminal output. It features a premium user system backed by SQLite for gating certain functionality.

**Note:** This bot is designed for destructive actions on Discord servers (deleting channels, banning members, etc.). Such actions violate Discord's Terms of Service and can result in account bans.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Technology Stack
- **Language:** Python 3.6 - 3.8
- **Discord Library:** discord.py with commands extension and app_commands (slash commands)
- **Terminal Styling:** colorama for cross-platform colored output
- **Database:** SQLite for local data persistence

### Application Structure
The project has a simple single-file architecture:
- `nuke-bot.py` - Main bot file containing all logic
- `requirements.txt` - Python dependencies
- `bot_data.db` - SQLite database file (created at runtime)

### Bot Features Architecture
1. **Channel Management** - Delete all channels, create new channels
2. **Role Management** - Delete all roles
3. **Member Management** - Ban all members
4. **Premium System** - SQLite-backed user gating system

### Database Schema
Single table design using SQLite:
- **premium_users** table with `user_id` (INTEGER PRIMARY KEY)
- Functions: `setup_db()`, `is_premium()`, `add_premium()`

### Design Patterns
- Uses discord.py's commands extension for bot command handling
- Async/await pattern for Discord API operations
- Environment-aware clear screen function (Windows vs Unix)
- Lambda functions for utility operations

## External Dependencies

### Python Packages
- **discord.py** (>=1.5.1) - Discord API wrapper for bot functionality
- **colorama** (>=0.4.4) - Cross-platform terminal color support

### External Services
- **Discord API** - Requires a bot token to authenticate and operate
- Bot token should be provided via environment variable or user input at runtime

### Data Storage
- **SQLite** - Local file-based database (`bot_data.db`) for premium user tracking
- No external database service required