from fastapi import APIRouter
from serialBridge import SerialBridge
from serialBridge import SerialBridge

bridge = SerialBridge()
router = APIRouter()


@router.get("/example")
async def example():
    return "Hello world!"

# This function currently uses G0 for the moves, which is a quick move(?), G1 is a linear move for cutting. Not sure what is best for this application, yet to test.

@router.get("/goto")
async def goto(x: float, y: float, z: float, sys: int):
    await bridge.goto(x, y, z, sys)


@router.get("/sendcommand")
async def sendcommand(command):
    await bridge.send_command(command)
