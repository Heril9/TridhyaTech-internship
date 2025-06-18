#!/bin/bash

# Your GitHub username
GITHUB_USER="Heril9"  # <-- Replace this

# Repo name on GitHub
REPO_NAME="TridhyaTech-internship"

# Set to 'private' or 'public'
REPO_VISIBILITY="private"

# ===============================

echo "Creating top-level GitHub repo: $REPO_NAME"

# Create the repo on GitHub
gh repo create "$GITHUB_USER/$REPO_NAME" --$REPO_VISIBILITY --description "All my projects from internship in one repo" --confirm

# Initialize git in the current folder
git init
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"

# Add all files/folders
git add .
git commit -m "Initial commit: All internship projects pushed into one repo"

# Push to GitHub
git branch -M main
git push -u origin main

echo "✅ All projects have been pushed into https://github.com/$GITHUB_USER/$REPO_NAME"
