# Simple GitHub Actions Setup

## What This Does
Runs your `battle.py` and `recruit.py` scripts every 2 hours automatically.

## Setup (3 steps)

### 1. Add Your Database Password
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `DATABASE_URL`
5. Value: Your Neon database connection string
6. Click **Add secret**

### 2. Commit the Workflow
```bash
git add .github/workflows/scheduler.yml
git commit -m "Add scheduler"
git push
```

### 3. Test It
1. Go to **Actions** tab in your repository
2. Click **Wargame Scheduler**
3. Click **Run workflow** button
4. Watch it run!

## That's It!
- Runs every 2 hours automatically
- Free forever
- Check **Actions** tab to see if it's working
- Green checkmark = success, red X = problem

## If Something Goes Wrong
1. Check the **Actions** tab for error messages
2. Make sure `DATABASE_URL` secret is set correctly
3. Make sure `recruit.py` and `battle.py` are in your repository
