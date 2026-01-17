from fastapi import FastAPI
from fastapi.responses import HTMLResponse

'''
This app object will be used to define the routes.
FastAPI uses decorators to define routes.
'''
app = FastAPI(
#     docs_url=None, # Keep Swagger UI accessible
#     redoc_url=None, # Disable ReDoc
#     openapi_url=None # Enable OpenAPI schema for docs to work
)

# Sample posts data
posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the first blog post",
        "author": "John Doe"
    },
    {
        "id": 2,
        "title": "Learning FastAPI",
        "content": "FastAPI is a modern Python web framework",
        "author": "Jane Smith"
    },
    {
        "id": 3,
        "title": "Python Tips",
        "content": "Some useful Python programming tips",
        "author": "Mike Johnson"
    },
    {
        "id": 4,
        "title": "Web Development",
        "content": "Building scalable web applications",
        "author": "Sarah Williams"
    },
    {
        "id": 5,
        "title": "API Design Best Practices",
        "content": "How to design clean and effective APIs",
        "author": "Tom Brown"
    }
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