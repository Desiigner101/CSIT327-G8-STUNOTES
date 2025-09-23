# StuNotes: A Student Task & Notes Management System

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Team](#team)

## Overview

**StuNotes** is a web application designed to help students manage their academic tasks, deadlines, and notes in one centralized platform. It provides an easy way for students to stay organized and improve their academic productivity.

**Problem:** Students struggle with managing multiple subjects, assignments, and exam schedules across different platforms, leading to missed deadlines and poor organization.

**Solution:** StuNotes offers a single platform where students can manage tasks, take notes, and track deadlines all in one place.

## Features

### Core Features
- Create, edit, and delete academic tasks and assignments
- Organize notes by subject and date
- Set reminders for upcoming deadlines
- Dashboard showing pending tasks and recent notes
- Search and filter tasks by subject or date
- Calendar view of deadlines and events

### User Features
- User registration and login
- Profile management with picture upload
- Customizable themes and notification settings
- Admin panel for user management

## Technology Stack

- **Backend**: Django (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Version Control**: Git & GitHub

## Installation

### Requirements
- Python 3.8 or higher
- MySQL Server
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Desiigner101/STUNOTES-APP.git
   cd stunotes
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the application**
   ```bash
   python manage.py runserver
   ```
   
## Usage

### For Students
1. Register for a new account
2. Login to access your dashboard
3. Add tasks with subjects and deadlines
4. Create and organize notes
5. Set up reminders for important dates
6. Use search and filter to find specific tasks or notes

### For Administrators
1. Access admin panel with admin credentials
2. Manage user accounts (add, edit, delete users)
3. Monitor system usage and performance

## Team

### IT317-G3 Development Team

#### Project Leadership
- Tupas, Niña Isabelle Capilitan - Product Owner
- Unabia, Brent Jelson Dejos - Business Analyst
- Ybañez, Liezel Alvarado - Scrum Master

#### Developers
- Kervin Gino M. Sarsonas - Lead Developer
- Kirby Klent G. Sala - Developer
- Xavier John A. Sabornido - Developer

#### Academic Supervisors
- Joemarie Amparo - IT317 Instructor
- Frederick Revilleza - CSIT327 Instructor

## Support

For questions or issues:
- Create an issue on GitHub
- Contact the development team
- Email the project team

---

**Developed by CSIT-327 Team**
