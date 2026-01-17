from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

"""
This app object will be used to define the routes.
FastAPI uses decorators to define routes.
"""
app = FastAPI(
    #     docs_url=None, # Keep Swagger UI accessible
    #     redoc_url=None, # Disable ReDoc
    #     openapi_url=None # Enable OpenAPI schema for docs to work
)

# Jinja2Templates object for rendering HTML templates
# This object loads templates from the "templates" directory
# and provides the render() method to pass context data to templates
# templates object knows to look for HTML files in the "templates" folder
templates = Jinja2Templates(directory="templates")

# Sample posts data
posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the first blog post",
        "author": "John Doe",
    },
    {
        "id": 2,
        "title": "Learning FastAPI",
        "content": "FastAPI is a modern Python web framework",
        "author": "Jane Smith",
    },
    {
        "id": 3,
        "title": "Python Tips",
        "content": "Some useful Python programming tips",
        "author": "Mike Johnson",
    },
    {
        "id": 4,
        "title": "Web Development",
        "content": "Building scalable web applications",
        "author": "Sarah Williams",
    },
    {
        "id": 5,
        "title": "API Design Best Practices",
        "content": "How to design clean and effective APIs",
        "author": "Tom Brown",
    },
]


@app.get("/")
def get_root():
    return {"message": "Hello, World!"}


@app.get("/api/v1/posts")
def get_posts():
    return posts


# Stacked decorators allow the same function to handle multiple routes
# include_in_schema=False hides this endpoint from OpenAPI/Swagger documentation
@app.get("/about", response_class=HTMLResponse, include_in_schema=False)
@app.get("/page", response_class=HTMLResponse, include_in_schema=False)
def get_about():
    """
    Endpoint that returns HTML content for the about page.
    Uses HTMLResponse to properly render the HTML content.

    Returns an HTML response for the about page
    """

    html_content = """
    <html>
        <head>
            <title>About Page</title>
        </head>
        <body>
            <h1>About This Blog</h1>
            <p>This blog is created using FastAPI.</p>
        </body>
    </html>
    """
    # return html_content //M1 -> return as string
    return HTMLResponse(content=html_content)


@app.get("/home")
def get_home(request: Request):
    """
    Endpoint that renders the home page using a Jinja2 template.

    Args:
        request (Request): The HTTP request object from FastAPI.

    Why Request object is required with Jinja2TemplateResponse:
    - Jinja2TemplateResponse needs the request object to generate proper URL redirects and context
    - The request object contains session data, cookies, headers, and other HTTP context information
    - Jinja2 templates often need access to request properties (e.g., url_for(), request.url, etc.)
    - FastAPI uses the request to ensure CSRF protection and proper context binding

    Context Dictionary Significance:
    - The context dict is passed as the third argument to TemplateResponse
    - It contains all variables that will be available in the Jinja2 template
    - The "request" key MUST be included in context for Jinja2 to access request-related utilities
    - Additional keys (like "posts") are custom variables defined by the developer
    - Context values become accessible in templates using variable interpolation

    Jinja2 Dot Notation Access:
    - Jinja2 allows accessing dictionary values using dot notation in templates
    - In the template, you can access posts list as: {{ posts }} instead of {{ posts['posts'] }}
    - Dictionary items can be accessed as: {{ post.id }}, {{ post.title }} instead of post['id'], post['title']
    - This provides a cleaner, more Pythonic syntax in HTML templates
    - The dot notation also works with object attributes and dictionary keys interchangeably

    Template Rendering Process:
    - TemplateResponse takes the request, template filename, and context dictionary
    - Jinja2 engine processes the template file and substitutes variables from context
    - The rendered HTML is returned as an HTTP response with proper content-type headers

    Returns:
        TemplateResponse: Renders "home.html" with posts data available in the template context
    """
    return templates.TemplateResponse(
        request, "home.html", {"request": request, "posts": posts, "title": "Home Page"}
    )
    # return templates.TemplateResponse("home.html", {"request": request, "posts": posts})
