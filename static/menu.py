from asyncio import ensure_future
from pyweb import pydom
from pyodide.ffi import create_proxy
from js import document
from pyodide.http import pyfetch


container = pydom["#container"][0]



async def set_username(event):
    new_username = event.target.value    
    print(f"Using pyfetch to send new_username to server")
    result = await pyfetch(
        url=f"/set_username/{new_username}",
        method="GET",       
    )
    



username_field = document.getElementById("set_username")
change_proxy = create_proxy(set_username)
username_field.addEventListener("change", change_proxy)