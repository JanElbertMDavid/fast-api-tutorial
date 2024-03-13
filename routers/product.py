from typing import Optional, List
from fastapi import APIRouter, BackgroundTasks, Cookie, Form, Header, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
from custom_log import log
import time

router = APIRouter(prefix="/product", tags=["product"])

products = ["Watch", "Camera", "Phone"]

async def time_consuming_function():
    time.sleep(5)
    return 'okay'

@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get("/all")
async def get_all_products(bt: BackgroundTasks):
    bt.add_task(log_router,'Test log using BG')
    await time_consuming_function()
    # log('MyAPI', 'Call to get all products')
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="Test_cookie", value="test_cookie_value")
    return response

def log_router(message: str):
    log('Test BG task', message)


@router.get("/withheader")
def get_products_with_header(
    response: Response,
    custom_header: List[Optional[str]] = Header(None),
    Test_cookie: Optional[str] = Cookie(None),
):
    if custom_header:
        response.headers["custom_response_header"] = "and ".join(custom_header)
    return {"data": products, "custom_header": custom_header, "my_cookie": Test_cookie}


@router.get(
    "/{id}",
    responses={
        200: {
            "content": {"text/html": {"example": "<div>product</div>"}},
            "description": "Returns the HTML for an object.",
        },
        400: {
            "content": {"text/plain": {"example": "Product not available"}},
            "description": "A clear text error message.",
        },
    },
)
def get_products_by_id(id: int):
    if id >= len(products):
        out = "Product not available"
        return PlainTextResponse(status_code=404, content=out, media_type="text/plain")
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;
            }}
            </style>
        </head>
        <div class="product>{product}</div>
        """
        return HTMLResponse(content=out, media_type="text/html")
