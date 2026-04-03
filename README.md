---
title: Email Triage OpenEnv
emoji: 📧
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# Email Triage OpenEnv (Final Boss Version)

## Overview
A realistic email inbox simulation where an AI agent must classify, prioritize, and respond.

## Features
- Multi-email inbox
- Priority-aware decision making
- Time-sensitive penalties
- Multi-step reasoning

## Run
uvicorn app:app --reload

## Docker
docker build -t email-env .
docker run -p 7860:7860 email-env

## Inference
python inference.py