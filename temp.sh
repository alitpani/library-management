#!/bin/bash

# Set up Git (first-time setup)
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"

# Initialize a new Git repository (if you are starting a new project)
git init

# OR clone an existing repository (do not use git init if you're cloning)
# git clone https://github.com/your-username/your-repository.git

# Navigate into your repository if you cloned it
# cd your-repository

# Add files to staging
git add .

# Commit the changes
git commit -m "Initial commit or a meaningful message describing your changes"

# Log in to GitHub from the CLI (as of Git version 2.29)
# Note: As of my last update, GitHub recommends using a personal access token (PAT) instead of a password.
# You can generate a PAT in your GitHub settings under Developer settings > Personal access tokens.
# When prompted for a username and password, use your GitHub username and your PAT as the password.
# For GitHub CLI users:
# gh auth login

# Set your remote repository URL
git remote add origin https://github.com/your-username/your-repository.git

# Push your commits to the remote repository
git push -u origin master
# If you're using main as the default branch (GitHub's default since Oct 2020), use:
# git push -u origin main

# Future pushes after the first one do not require the -u option:
# git push
