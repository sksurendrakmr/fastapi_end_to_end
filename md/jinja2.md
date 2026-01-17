# Jinja2 Templating in FastAPI

## 1. Configure Jinja2 Template in FastAPI App

### Basic Setup

```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Mount static files (CSS, JS, images)
# Arguments:
# - "/static": URL path where static files will be accessible (e.g., /static/css/style.css)
# - StaticFiles(directory="static"): Serves files from the "static" directory in your project root
# - name="static": Name for the route, used with url_for() in templates
app.mount("/static", StaticFiles(directory="static"), name="static")



# Configure Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request):
    return templates.TemplateResponse("home.html", {"request": request})
```

### Important Points:

- Always include `request` object in the context dictionary
- The `request` object is required for URL generation with `url_for()`
- Template directory path should be relative to your project root
- Use absolute path for production: `directory=os.path.join(os.path.dirname(__file__), "templates")`

### Using url_for() in Templates

The `url_for()` function is used in Jinja2 templates to generate URLs dynamically. It requires the `request` object to be passed in the context.

#### Generating URLs for Routes

```jinja2
{# Link to a named route #}
<a href="{{ url_for('home') }}">Home</a>
<a href="{{ url_for('about') }}">About Page</a>

{# Link to a route with path parameters #}
<a href="{{ url_for('get_user', user_id=123) }}">View User 123</a>
<a href="{{ url_for('get_post', user_id=5, post_id=42) }}">View Post</a>

{# Link with query parameters #}
<a href="{{ url_for('search', q='python') }}">Search for Python</a>

{# Link with query parameters and path parameters #}
<a href="{{ url_for('get_user', user_id=123, include_posts=true) }}">User with Posts</a>
```

#### Accessing Files from Static Folder

```jinja2
{# Link to CSS files #}
<link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
<link rel="stylesheet" href="{{ url_for('static', path='/css/responsive.css') }}">

{# Link to JavaScript files #}
<script src="{{ url_for('static', path='/js/main.js') }}"></script>
<script src="{{ url_for('static', path='/js/app.js') }}"></script>

{# Link to images #}
<img src="{{ url_for('static', path='/images/logo.png') }}" alt="Logo">
<img src="{{ url_for('static', path='/images/header/banner.jpg') }}" alt="Banner">

{# Link to font files #}
<link href="{{ url_for('static', path='/fonts/roboto.woff2') }}" rel="preload" as="font">

{# Link to favicon #}
<link rel="icon" href="{{ url_for('static', path='/images/favicon.ico') }}">

{# Background image in CSS #}
<div style="background-image: url('{{ url_for('static', path='/images/bg.jpg') }}')">
    Background content
</div>
```

#### Complete Example with Routes and Static Files

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    return templates.TemplateResponse("user.html", {
        "request": request,
        "user_id": user_id
    })

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
```

```jinja2
{# Template example with url_for usage #}
<!DOCTYPE html>
<html>
<head>
    <title>My Site</title>

    {# CSS files using url_for #}
    <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', path='/css/theme.css') }}">

    {# Favicon using url_for #}
    <link rel="icon" href="{{ url_for('static', path='/images/favicon.ico') }}">
</head>
<body>
    <header>
        {# Logo image using url_for #}
        <img src="{{ url_for('static', path='/images/logo.png') }}" alt="Logo" class="logo">

        {# Navigation links using url_for for routes #}
        <nav>
            <a href="{{ url_for('home') }}">Home</a>
            <a href="{{ url_for('about') }}">About</a>
            <a href="{{ url_for('get_user', user_id=1) }}">Profile</a>
        </nav>
    </header>

    <main>
        <h1>Welcome</h1>

        {# Images with url_for #}
        <img src="{{ url_for('static', path='/images/banner.jpg') }}" alt="Banner">

        {# Links with url_for for routes #}
        <a href="{{ url_for('get_user', user_id=123) }}">View User Profile</a>
    </main>

    <footer>
        <p>&copy; 2024 My Site</p>
    </footer>

    {# JavaScript files using url_for #}
    <script src="{{ url_for('static', path='/js/main.js') }}"></script>
    <script src="{{ url_for('static', path='/js/app.js') }}"></script>
</body>
</html>
```

#### Key Points about url_for():

- `url_for('name')` - where `name` is the route function name or the mount name (`'static'`)
- `path='/...'` - required parameter when accessing static files, specifies the file path relative to static directory
- Path parameters must be passed as keyword arguments: `user_id=123`
- Query parameters are automatically added to the URL
- Always pass the `request` object in context for `url_for()` to work
- Static files should use `path='/...'` parameter with the `'static'` mount name

### Complete Example with Multiple Routes

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Static files setup
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates setup
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "title": "Home Page"
    })

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int, name: str = "Guest"):
    return templates.TemplateResponse("user.html", {
        "request": request,
        "user_id": user_id,
        "name": name
    })
```

---

## 2. Essential Jinja2 Concepts

### Variables

```jinja2
{# Display variable #}
{{ variable_name }}

{# Display nested object #}
{{ user.name }}
{{ items[0] }}

{# Default value if variable is undefined #}
{{ name | default("Unknown") }}
```

### If/Elif/Else Blocks

```jinja2
{# Basic if statement #}
{% if user %}
    <p>Welcome, {{ user.name }}!</p>
{% endif %}

{# If-else #}
{% if age >= 18 %}
    <p>Adult</p>
{% else %}
    <p>Minor</p>
{% endif %}

{# If-elif-else #}
{% if score >= 90 %}
    <p>Grade: A</p>
{% elif score >= 80 %}
    <p>Grade: B</p>
{% elif score >= 70 %}
    <p>Grade: C</p>
{% else %}
    <p>Grade: F</p>
{% endif %}

{# Comparison operators #}
{% if user.is_active == true %}
{% if count > 0 %}
{% if name in allowed_names %}
{% if user.role is not none %}
```

### For Loops

```jinja2
{# Basic loop #}
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}

{# Loop with condition #}
{% for user in users if user.is_active %}
    <p>{{ user.name }}</p>
{% endfor %}

{# Nested loops #}
{% for category in categories %}
    <h3>{{ category.name }}</h3>
    {% for product in category.products %}
        <p>{{ product }}</p>
    {% endfor %}
{% endfor %}

{# Using loop variable (special) #}
{% for item in items %}
    <li>{{ loop.index }}: {{ item }}</li>
    {# loop.index: Current iteration (1-indexed) #}
    {# loop.index0: Current iteration (0-indexed) #}
    {# loop.first: True if first iteration #}
    {# loop.last: True if last iteration #}
    {# loop.length: Total length of sequence #}
    {# loop.revindex: Reverse iteration index #}
    {# loop.depth: Nesting depth #}
{% endfor %}

{# Loop with else (no items) #}
{% for item in items %}
    <li>{{ item }}</li>
{% else %}
    <p>No items found</p>
{% endfor %}
```

### Filters

```jinja2
{# String filters #}
{{ text | upper }}              {# Uppercase #}
{{ text | lower }}              {# Lowercase #}
{{ text | capitalize }}         {# First letter uppercase #}
{{ text | title }}              {# Title case #}
{{ text | trim }}               {# Remove whitespace #}
{{ text | length }}             {# String length #}

{# Number filters #}
{{ price | round(2) }}          {# Round to 2 decimal places #}
{{ price | int }}               {# Convert to integer #}
{{ price | float }}             {# Convert to float #}

{# List filters #}
{{ items | length }}            {# Number of items #}
{{ items | first }}             {# First item #}
{{ items | last }}              {# Last item #}
{{ items | join(", ") }}        {# Join with separator #}
{{ items | sort }}              {# Sort list #}
{{ items | reverse }}           {# Reverse list #}
{{ items | unique }}            {# Remove duplicates #}

{# Other filters #}
{{ value | default("N/A") }}    {# Default value #}
{{ date | strftime("%Y-%m-%d") }}{# Date formatting #}
{{ html | safe }}               {# Mark as safe HTML #}
{{ dict_item | tojson }}        {# Convert to JSON #}

{# Chaining filters #}
{{ text | upper | trim }}
```

### Comments

```jinja2
{# This is a comment and won't appear in output #}

{# Multi-line comments also work
   across multiple lines
#}
```

---

## 3. Tips and Tricks

### 1. Using URL Generation

```jinja2
{# Generate URL for a route #}
<a href="{{ url_for('home') }}">Home</a>
<a href="{{ url_for('get_user', user_id=123) }}">User Profile</a>

{# Link to static files #}
<link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
<img src="{{ url_for('static', path='/images/logo.png') }}">
<script src="{{ url_for('static', path='/js/main.js') }}"></script>
```

### 2. Conditional CSS Classes

```jinja2
<div class="btn {% if is_active %}btn-active{% else %}btn-inactive{% endif %}">
    Button
</div>

{# More concise with ternary-like syntax #}
<div class="btn {{ 'btn-active' if is_active else 'btn-inactive' }}">
    Button
</div>
```

### 3. Using Whitespace Control

```jinja2
{# Remove extra whitespace #}
{% if condition -%}
    {# Content #}
{%- endif %}

{# Use '-' on left side to remove whitespace before #}
{# Use '-' on right side to remove whitespace after #}
```

### 4. Macros (Reusable Code Blocks)

```jinja2
{# Define macro #}
{% macro render_button(label, url, style='primary') %}
    <a href="{{ url }}" class="btn btn-{{ style }}">
        {{ label }}
    </a>
{% endmacro %}

{# Use macro #}
{{ render_button('Click Me', '/action', 'secondary') }}

{# Macro with variable arguments #}
{% macro render_list(items) %}
    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
{% endmacro %}

{{ render_list(my_items) }}
```

### 5. Set Variables in Template

```jinja2
{# Define variable in template #}
{% set full_name = user.first_name ~ " " ~ user.last_name %}
<p>{{ full_name }}</p>

{# Set with condition #}
{% set greeting = "Hello, " ~ (user.name if user else "Guest") %}
<p>{{ greeting }}</p>

{# Set with loop #}
{% set total = 0 %}
{% for item in items %}
    {% set total = total + item.price %}
{% endfor %}
<p>Total: ${{ total }}</p>
```

### 6. Logical Operators

```jinja2
{# AND operator #}
{% if user and user.is_active %}
    <p>Active user</p>
{% endif %}

{# OR operator #}
{% if user.role == 'admin' or user.role == 'moderator' %}
    <p>Admin or Moderator</p>
{% endif %}

{# NOT operator #}
{% if not user.deleted %}
    <p>User active</p>
{% endif %}
```

### 7. Dictionary and List Access

```jinja2
{# Dictionary access #}
{{ user['name'] }}
{{ config.get('api_key', 'default') }}

{# List slicing #}
{{ items[:5] }}          {# First 5 items #}
{{ items[-3:] }}         {# Last 3 items #}
{{ items[1:4] }}         {# Items 1-3 #}
```

### 8. Testing Values

```jinja2
{# is tests #}
{% if value is defined %}
{% if value is none %}
{% if value is sameas(true) %}
{% if items is iterable %}
{% if variable is odd %}
{% if variable is even %}
{% if value is divisibleby(3) %}

{# Negation #}
{% if value is not none %}
{% if item is not in items %}
```

---

## 4. Jinja2 Template Inheritance

### Base Template (base.html)

```jinja2
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Website{% endblock %}</title>
    {% block head %}
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
    {% endblock %}
</head>
<body>
    <header>
        <nav>
            {% block nav %}
                <a href="{{ url_for('home') }}">Home</a>
                <a href="{{ url_for('about') }}">About</a>
            {% endblock %}
        </nav>
    </header>

    <main>
        {% block content %}
            <p>Default content</p>
        {% endblock %}
    </main>

    <footer>
        {% block footer %}
            <p>&copy; 2024 My Website</p>
        {% endblock %}
    </footer>

    {% block scripts %}
        <script src="{{ url_for('static', path='/js/main.js') }}"></script>
    {% endblock %}
</body>
</html>
```

### Child Template (page.html)

```jinja2
{% extends "base.html" %}

{% block title %}Home Page - My Website{% endblock %}

{% block content %}
    <h1>Welcome to My Website</h1>
    <p>This is the home page content.</p>
{% endblock %}

{% block scripts %}
    {{ super() }}  {# Include parent block content #}
    <script src="{{ url_for('static', path='/js/home.js') }}"></script>
{% endblock %}
```

### Multi-level Inheritance

```jinja2
{# base.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

{# layout.html - extends base.html #}
{% extends "base.html" %}

{% block title %}{{ page_title }} - My Site{% endblock %}

{% block content %}
    <header>
        {% block header %}{% endblock %}
    </header>
    <main>
        {% block main_content %}{% endblock %}
    </main>
    <footer>
        {% block footer %}{% endblock %}
    </footer>
{% endblock %}

{# page.html - extends layout.html #}
{% extends "layout.html" %}

{% block main_content %}
    <h1>{{ title }}</h1>
    <p>{{ content }}</p>
{% endblock %}
```

### Important Notes on Inheritance:

- Child templates should extend parent with `{% extends "parent.html" %}`
- Use `{% block %}` to define overridable sections
- Use `{{ super() }}` to include parent block content
- `extends` must be the first statement in child template
- Multiple levels of inheritance are possible

---

## 5. Other Important Jinja2 Concepts

### Include (Reuse template fragments)

```jinja2
{# Include entire template #}
{% include "sidebar.html" %}

{# Include with context variables #}
{% include "user_card.html" with context %}

{# Include without context #}
{% include "isolated.html" without context %}

{# Include with specific variables #}
{% include "message.html" with context %}
    {% set message = "Hello" %}
{% endinclude %}

{# Include multiple templates #}
{% for template in templates %}
    {% include template %}
{% endfor %}
```

### Import (Use macros from another template)

```jinja2
{# Import macros from another template #}
{% import "macros.html" as macros %}
{{ macros.render_button('Click', '/url') }}

{# Import specific macro #}
{% from "macros.html" import render_button %}
{{ render_button('Click', '/url') }}

{# Import with alias #}
{% from "forms.html" import render_form as form %}
{{ form(data) }}
```

### Custom Filters

```python
# In your FastAPI app
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# Add custom filter
def format_currency(value):
    return f"${value:.2f}"

templates.env.filters["currency"] = format_currency

# Or add multiple filters
def pluralize(value, singular, plural):
    return singular if value == 1 else plural

templates.env.filters["pluralize"] = pluralize
```

```jinja2
{# Use custom filter in template #}
{{ price | currency }}
{{ count }} {{ count | pluralize("item", "items") }}
```

### Autoescape

```jinja2
{# By default, HTML is escaped #}
{{ user_input }}  {# <script>alert('xss')</script> becomes &lt;script&gt;...&lt;/script&gt; #}

{# Mark content as safe (use only for trusted content) #}
{{ html_content | safe }}

{# Turn off autoescape for a block #}
{% autoescape false %}
    {{ possibly_unsafe_html }}
{% endautoescape %}
```

### Context Variables in Filters

```jinja2
{# Some filters can access context #}
{{ items | join(separator, attribute='name') }}
```

---

## 6. Different Ways to Add JS and CSS in Jinja2 Templates

### 1. Direct Link in Template

```jinja2
{# Link to CSS #}
<link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">

{# Link to JavaScript #}
<script src="{{ url_for('static', path='/js/main.js') }}"></script>

{# External CDN #}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
```

### 2. Using Blocks for CSS and JS

```jinja2
{# base.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>

    {# Base CSS #}
    <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">

    {# CSS block for child templates #}
    {% block additional_css %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}

    {# Base JS #}
    <script src="{{ url_for('static', path='/js/main.js') }}"></script>

    {# JS block for child templates #}
    {% block additional_js %}{% endblock %}
</body>
</html>

{# child.html #}
{% extends "base.html" %}

{% block additional_css %}
    <link rel="stylesheet" href="{{ url_for('static', path='/css/page.css') }}">
{% endblock %}

{% block additional_js %}
    <script src="{{ url_for('static', path='/js/page.js') }}"></script>
{% endblock %}
```

### 3. Inline CSS

```jinja2
{% block head %}
    <style>
        body {
            background-color: {{ bg_color | default('#ffffff') }};
        }
        .title {
            color: {{ title_color | default('#000000') }};
        }
    </style>
{% endblock %}
```

### 4. Inline JavaScript

```jinja2
{% block additional_js %}
    <script>
        const userId = {{ user_id }};
        const userName = "{{ user_name }}";
        const items = {{ items_json }};

        document.addEventListener('DOMContentLoaded', function() {
            console.log('Page loaded for user:', userName);
        });
    </script>
{% endblock %}
```

### 5. Conditional CSS/JS

```jinja2
{# Load different CSS based on condition #}
{% if is_mobile %}
    <link rel="stylesheet" href="{{ url_for('static', path='/css/mobile.css') }}">
{% else %}
    <link rel="stylesheet" href="{{ url_for('static', path='/css/desktop.css') }}">
{% endif %}

{# Load JS only for specific pages #}
{% if page_type == 'dashboard' %}
    <script src="{{ url_for('static', path='/js/dashboard.js') }}"></script>
{% endif %}

{# Load CSS based on user role #}
{% if user.role == 'admin' %}
    <link rel="stylesheet" href="{{ url_for('static', path='/css/admin.css') }}">
{% endif %}
```

### 6. Using Macros for Repeated CSS/JS

```jinja2
{# macros.html #}
{% macro load_stylesheet(filename) %}
    <link rel="stylesheet" href="{{ url_for('static', path='/css/' ~ filename) }}">
{% endmacro %}

{% macro load_script(filename) %}
    <script src="{{ url_for('static', path='/js/' ~ filename) }}"></script>
{% endmacro %}

{% macro load_css_cdn(url) %}
    <link rel="stylesheet" href="{{ url }}">
{% endmacro %}

{% macro load_js_cdn(url) %}
    <script src="{{ url }}"></script>
{% endmacro %}

{# In your template #}
{% from "macros.html" import load_stylesheet, load_script, load_css_cdn, load_js_cdn %}

{{ load_stylesheet('style.css') }}
{{ load_script('main.js') }}
{{ load_css_cdn('https://cdn.example.com/bootstrap.css') }}
{{ load_js_cdn('https://cdn.example.com/jquery.js') }}
```

### 7. Asynchronous JS Loading

```jinja2
{# Async script loading #}
<script src="{{ url_for('static', path='/js/analytics.js') }}" async></script>

{# Deferred script loading #}
<script src="{{ url_for('static', path='/js/non-critical.js') }}" defer></script>

{# Module script #}
<script type="module" src="{{ url_for('static', path='/js/app.js') }}"></script>
```

### 8. Dynamic CSS Variables

```jinja2
<style>
    :root {
        --primary-color: {{ theme.primary_color }};
        --secondary-color: {{ theme.secondary_color }};
        --font-family: '{{ theme.font_family }}';
    }
</style>
<link rel="stylesheet" href="{{ url_for('static', path='/css/theme.css') }}">
```

### 9. CSS/JS with Query Parameters (Cache Busting)

```jinja2
{# Add version parameter for cache busting #}
<link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}?v={{ app_version }}">
<script src="{{ url_for('static', path='/js/main.js') }}?v={{ app_version }}"></script>

{# Or use timestamp #}
<link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}?t={{ now().timestamp() }}">
```

### 10. Best Practice Example

```jinja2
{# base.html #}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My App{% endblock %}</title>

    {# Core CSS #}
    <link rel="stylesheet" href="{{ url_for('static', path='/css/base.css') }}">

    {# Theme CSS #}
    <link rel="stylesheet" href="{{ url_for('static', path='/css/theme.css') }}?v=1.0.0">

    {# Page-specific CSS block #}
    {% block page_css %}{% endblock %}

    {# Inline critical CSS #}
    <style>
        {% block critical_css %}{% endblock %}
    </style>
</head>
<body>
    {% block content %}{% endblock %}

    {# Core JS (deferred) #}
    <script src="{{ url_for('static', path='/js/base.js') }}" defer></script>

    {# Page-specific JS #}
    {% block page_js %}{% endblock %}
</body>
</html>
```

---

## 7. Conditional HTML Rendering Based on Screen Size and Other Conditions

### 1. Show/Hide HTML Based on Screen Size (CSS Approach)

```jinja2
{# Show only on mobile (< 768px) #}
<div class="d-md-none">
    <p>This content only appears on mobile devices</p>
</div>

{# Show only on desktop (>= 768px) #}
<div class="d-none d-md-block">
    <p>This content only appears on desktop</p>
</div>

{# Using Tailwind CSS #}
<nav class="md:hidden">
    Mobile Navigation
</nav>

<nav class="hidden md:block">
    Desktop Navigation
</nav>

{# Show on small screens, hide on medium and up #}
<div class="block sm:hidden">
    Extra small screens
</div>

{# Show on medium screens and up #}
<div class="hidden md:block">
    Medium and larger screens
</div>
```

### 2. Show/Hide HTML Based on Screen Size (Server-side with Template Condition)

```python
# In your FastAPI app
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

@app.get("/page", response_class=HTMLResponse)
async def render_page(request: Request, device_type: str = None):
    # Detect device type from User-Agent header
    user_agent = request.headers.get('user-agent', '').lower()
    is_mobile = any(x in user_agent for x in ['mobile', 'iphone', 'android', 'ipad'])

    return templates.TemplateResponse("page.html", {
        "request": request,
        "is_mobile": is_mobile,
        "device_type": device_type or ("mobile" if is_mobile else "desktop")
    })
```

```jinja2
{# In your template #}
{% if is_mobile %}
    <nav class="mobile-nav">
        <a href="/">Home</a>
        <a href="/menu">Menu</a>
    </nav>
{% else %}
    <nav class="desktop-nav">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/services">Services</a></li>
        </ul>
    </nav>
{% endif %}

{# Show different layout based on device #}
{% if device_type == 'mobile' %}
    <div class="mobile-layout">
        {# Mobile layout #}
    </div>
{% elif device_type == 'tablet' %}
    <div class="tablet-layout">
        {# Tablet layout #}
    </div>
{% else %}
    <div class="desktop-layout">
        {# Desktop layout #}
    </div>
{% endif %}
```

### 3. Conditional HTML Based on User Role/Authentication

```jinja2
{# Show content only to authenticated users #}
{% if user and user.is_authenticated %}
    <div class="user-dashboard">
        <h2>Welcome, {{ user.name }}!</h2>
        <p>Your profile: <a href="/profile">View Profile</a></p>
    </div>
{% else %}
    <div class="login-prompt">
        <p>Please <a href="/login">login</a> to access this content</p>
    </div>
{% endif %}

{# Show content based on user role #}
{% if user.role == 'admin' %}
    <div class="admin-panel">
        <a href="/admin/users">Manage Users</a>
        <a href="/admin/settings">Settings</a>
    </div>
{% elif user.role == 'moderator' %}
    <div class="moderator-panel">
        <a href="/moderate">Moderate Content</a>
    </div>
{% else %}
    <div class="user-content">
        Regular user content
    </div>
{% endif %}
```

### 4. Conditional HTML Based on Feature Flags

```python
# In your FastAPI app
from typing import Dict

FEATURE_FLAGS: Dict[str, bool] = {
    "new_dashboard": True,
    "beta_features": False,
    "dark_mode": True,
}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "features": FEATURE_FLAGS
    })
```

```jinja2
{# In your template #}
{% if features.new_dashboard %}
    <div class="new-dashboard">
        {# New dashboard UI #}
    </div>
{% else %}
    <div class="old-dashboard">
        {# Old dashboard UI #}
    </div>
{% endif %}

{# Enable beta features only for specific users #}
{% if features.beta_features and user.is_beta_tester %}
    <div class="beta-feature">
        <p>Try our experimental features!</p>
    </div>
{% endif %}
```

### 5. Conditional HTML Based on Data/Content

```jinja2
{# Show/hide based on list content #}
{% if notifications %}
    <div class="notification-bell">
        <span class="badge">{{ notifications | length }}</span>
        {% for notification in notifications %}
            <div class="notification">{{ notification.message }}</div>
        {% endfor %}
    </div>
{% else %}
    <div class="no-notifications">
        You're all caught up!
    </div>
{% endif %}

{# Show/hide based on number of items #}
{% if items | length > 0 %}
    <div class="item-list">
        {% for item in items %}
            <div class="item">{{ item.name }}</div>
        {% endfor %}
    </div>
{% elif loading %}
    <div class="loading">
        Loading items...
    </div>
{% else %}
    <div class="empty-state">
        <p>No items found</p>
    </div>
{% endif %}

{# Show/hide based on date/time conditions #}
{% if current_time.hour < 12 %}
    <p>Good morning!</p>
{% elif current_time.hour < 18 %}
    <p>Good afternoon!</p>
{% else %}
    <p>Good evening!</p>
{% endif %}
```

### 6. Using JavaScript for Dynamic Conditional Rendering

```jinja2
{# Pass data to JavaScript for client-side conditional rendering #}
<script>
    const isMobile = window.innerWidth < 768;
    const theme = "{{ theme }}";
    const userRole = "{{ user.role }}";

    // Show/hide elements based on conditions
    if (isMobile) {
        document.getElementById('desktop-nav').style.display = 'none';
        document.getElementById('mobile-nav').style.display = 'block';
    } else {
        document.getElementById('desktop-nav').style.display = 'block';
        document.getElementById('mobile-nav').style.display = 'none';
    }

    // Apply theme
    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
    }
</script>

{# HTML elements to be controlled by JS #}
<nav id="desktop-nav" class="desktop-navigation">
    Desktop menu here
</nav>

<nav id="mobile-nav" class="mobile-navigation" style="display: none;">
    Mobile menu here
</nav>
```

### 7. Media Queries with Template Variables

```jinja2
<style>
    {# Dynamic media queries based on template variables #}
    {% if breakpoint_mobile %}
        @media (max-width: {{ breakpoint_mobile }}px) {
            .container {
                padding: 10px;
            }
        }
    {% endif %}

    {% if breakpoint_tablet %}
        @media (min-width: {{ breakpoint_tablet }}px) and (max-width: {{ breakpoint_desktop - 1 }}px) {
            .container {
                padding: 20px;
            }
        }
    {% endif %}
</style>
```

### 8. Conditional Elements with Macro

```jinja2
{# macros.html #}
{% macro render_conditional(content, condition, breakpoint='md') %}
    {# Desktop version (always rendered, hidden with CSS) #}
    <div class="d-none d-{{ breakpoint }}-block">
        {{ content }}
    </div>
{% endmacro %}

{% macro render_responsive_nav(mobile_items, desktop_items) %}
    {# Mobile nav #}
    <nav class="mobile-nav d-md-none">
        {% for item in mobile_items %}
            <a href="{{ item.url }}">{{ item.label }}</a>
        {% endfor %}
    </nav>

    {# Desktop nav #}
    <nav class="desktop-nav d-none d-md-block">
        {% for item in desktop_items %}
            <a href="{{ item.url }}">{{ item.label }}</a>
        {% endfor %}
    </nav>
{% endmacro %}

{# In your template #}
{% from "macros.html" import render_responsive_nav %}

{{ render_responsive_nav(mobile_menu, desktop_menu) }}
```

### 9. Practical Complete Example

```python
# FastAPI app
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    user_agent = request.headers.get('user-agent', '').lower()
    is_mobile = any(x in user_agent for x in ['mobile', 'iphone', 'android'])

    return templates.TemplateResponse("index.html", {
        "request": request,
        "is_mobile": is_mobile,
        "is_admin": True,  # Example
        "notifications_count": 3,
        "is_dark_mode": True,
        "current_hour": datetime.now().hour,
    })
```

```jinja2
{# index.html #}
<!DOCTYPE html>
<html>
<head>
    <style>
        @media (max-width: 767px) {
            .desktop-only { display: none; }
        }

        @media (min-width: 768px) {
            .mobile-only { display: none; }
        }

        {% if is_dark_mode %}
            body { background: #1a1a1a; color: #fff; }
        {% endif %}
    </style>
</head>
<body>
    {# Conditional header based on screen size #}
    <header>
        {% if is_mobile %}
            <div class="mobile-header">
                <button class="menu-toggle">☰</button>
                <h1>App</h1>
            </div>
        {% else %}
            <div class="desktop-header">
                <h1>My Application</h1>
                <nav>
                    <a href="/">Home</a>
                    <a href="/about">About</a>
                    {% if is_admin %}
                        <a href="/admin">Admin Panel</a>
                    {% endif %}
                </nav>
            </div>
        {% endif %}
    </header>

    {# Main content with conditional rendering #}
    <main>
        {% if current_hour < 12 %}
            <p>Good morning! Start your day right.</p>
        {% endif %}

        {% if notifications_count > 0 %}
            <div class="alert alert-info">
                You have {{ notifications_count }} new notifications
            </div>
        {% endif %}

        {# Admin-only content #}
        {% if is_admin %}
            <section class="admin-dashboard">
                <h2>Admin Controls</h2>
                <a href="/admin/users">Manage Users</a>
            </section>
        {% endif %}
    </main>

    {# Mobile-only footer navigation #}
    {% if is_mobile %}
        <nav class="mobile-footer-nav">
            <a href="/">Home</a>
            <a href="/search">Search</a>
            <a href="/menu">Menu</a>
        </nav>
    {% endif %}
</body>
</html>
```

### 10. Best Practices

```jinja2
{# ✅ DO: Use CSS for purely visual responsiveness #}
<div class="d-none d-md-block">Desktop content</div>

{# ✅ DO: Use Jinja2 for significant content/structure changes #}
{% if is_mobile %}
    {# Different HTML structure for mobile #}
{% endif %}

{# ✅ DO: Combine server-side and client-side approaches #}
<div id="content" class="responsive-content">
    {# Server renders the initial state #}
</div>

{# ❌ DON'T: Over-render duplicate content #}
{# Avoid rendering both versions if CSS can handle it #}

{# ✅ DO: Use feature flags for A/B testing #}
{% if features.new_feature and user.in_beta_group %}
    {# New feature #}
{% endif %}

{# ✅ DO: Minimize template logic, use CSS/JS when possible #}
{# For purely visual changes, use CSS media queries instead #}
```

---

## Summary

Jinja2 is a powerful templating engine that allows you to:

- Generate dynamic HTML content
- Reuse code with template inheritance and macros
- Organize CSS and JS assets efficiently
- Keep logic separate from presentation
- Build scalable template structures

Always remember to include the `request` object when rendering templates in FastAPI!
