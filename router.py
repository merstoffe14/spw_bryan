from fastapi import APIRouter
from serialBridge import SerialBridge
from serialBridge import SerialBridge
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import matlab.engine

class JointAngles(BaseModel):
    theta_1: float
    theta_2: float
    theta_3: float

class Position(BaseModel):
    pos_x: float
    pos_y: float
    pos_z: float

bridge = SerialBridge()
router = APIRouter()

# Start MATLAB engine
eng = matlab.engine.start_matlab()

@router.get("/example")
async def example():
    return "Hello world!"

# This function currently uses G0 for the moves, which is a quick move(?), G1 is a linear move for cutting. Not sure what is best for this application, yet to test.

@router.get("/goto")
async def goto(x: float, y: float, z: float, sys: int):
    await bridge.goto(x, y, z, sys)


@router.get("/sendcommand")
async def sendcommand(command):
    print(f"sending command: {command}")
    await bridge.send_command(command)


@router.post("/forward_kinematics/")
def forward_kinematics(joint_angles: JointAngles):
    try:
        theta_1 = joint_angles.theta_1
        theta_2 = joint_angles.theta_2
        theta_3 = joint_angles.theta_3

        result = eng.forward_kinematics(theta_1, theta_2, theta_3, nargout=3)  # Adjust this according to your MATLAB function signature
        return {"pos_x": result[0], "pos_y": result[1], "pos_z": result[2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/inverse_kinematics/")
def inverse_kinematics(position: Position):
    try:
        print("inverse_kinematics")
        pos_x = position.pos_x
        pos_y = position.pos_y
        pos_z = position.pos_z

        result = eng.inverse_kinematics(pos_x, pos_y, pos_z, nargout=3)  # Adjust this according to your MATLAB function signature
        return {"theta_1": result[0], "theta_2": result[1], "theta_3": result[2]}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))