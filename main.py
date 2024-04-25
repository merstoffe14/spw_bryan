from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import bridge, router
import threading

'''
For more structure, we use static files.
All the api calls get routed to the router.py file.
The commented lines are:
    - an example of how to use threading, can be useful.
    - an example of how to send a basic GRBL command.
'''


app = FastAPI()
api = FastAPI()
api.include_router(router)
app.mount('/api', api)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.on_event('startup')
async def app_startup():
    print("main startup")
    await bridge.open_bridge()
    
    # thread_threadname = threading.Thread(target=class.run_main)
    # thread_threadname.start()  

    # await bridge.send_command("$H")



