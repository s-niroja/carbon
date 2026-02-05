from fastapi import FastAPI,HTTPException
from classes.userclass import User
from classes.security import hash_password,verify_password,encode_response,decode_response
from classes.c02class import individual,application
from classes.database import users_collection as UserTable,history_collection as historyTable
from ai.prediction import predict_individual_co2,predict_app_co2
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#root 
@app.get("/")
def roor():
    return{"ststus":"carbon detector is working"}

#add user
@app.post("/createuser")
async def createuser(user:User):
    user_dict = User.dict(user)
    user_dict["phone"] = encode_response(user_dict["phone"])
    user_dict["password"] = hash_password(user_dict["password"])
    user_dict["role"] = "user"
    result = UserTable.insert_one(user_dict)

    if not result:
        raise HTTPException(status_code=400 , detail="try again")
    return({"message":"Account created"})

#login
@app.post("/login")
async def login(number,password):
    User = await UserTable.find_one({"phone":encode_response(number)})

    if not User:
        raise HTTPException(status_code=404, detail="user not found")
    
    if not verify_password(password,User['password']):
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    return({"message":"login sucessfull","user_id":encode_response(str(User["_id"])),"role":User["role"]})

    
#individual c02 prediction
@app.post("/calculateindividual")
async def individualc02(data: individual):

    co2_value, category, suggestion, details = predict_individual_co2(
        data.pvkm,
        data.puvkm,
        data.pjc,
        data.tkm,
        data.ekwh,
        data.wul,
        data.wk,
        data.dt
    )

    userid = decode_response(data.userid)

    history_dict = {
        "user_id": userid,
        "data": {
            "predicted_co2": float(co2_value),
            "impact_category": category,
            "suggestion": suggestion,
            "details": details
        }
    }

    insert_result = await historyTable.insert_one(history_dict)  

    if not insert_result.inserted_id:
        raise HTTPException(status_code=400, detail="Cannot store history")

    return {
        "status": "success",
        "co2_value": co2_value,
        "category": category,
        "suggestion": suggestion,
        "details": details
    }



#application c02
@app.post("/appc02")
async def application_co2(app:application):
   prediction, result= predict_app_co2(app.cpu,app.ram,app.duriation,app.app_name)
   
   user_id = decode_response(app.user_id)

   history_dict = {
        "user_id": user_id,
        "data": {
            "predicted_co2": float(prediction),
            "Tips": result
        }
    }
   insert_result = await historyTable.insert_one(history_dict)  
   if not insert_result.inserted_id:
        raise HTTPException(status_code=400, detail="Cannot store history")

   return{
       "co2":prediction,
       "tips":result
   }


#history
@app.get("/history/{user_id}")
async def history(user_id: str):

    decoded_user_id = decode_response(user_id)

    if not decoded_user_id or not ObjectId.is_valid(decoded_user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")

    cursor = historyTable.find({
        "user_id": decoded_user_id
    })

    history_list = await cursor.to_list(length=100)

    if not history_list:
        raise HTTPException(status_code=404, detail="No history found")

    for item in history_list:
        item["_id"] = str(item["_id"])
        item["user_id"] = str(item["user_id"])

    return {
        "count": len(history_list),
        "history": history_list
    }

@app.get("/allusers")
async def allusers():
    # Get cursor
    cursor = UserTable.find()

    # Convert cursor to list (limit to 100 for safety)
    users_list = await cursor.to_list(length=100)

    # Convert ObjectId to string
    for user in users_list:
        user["_id"] = encode_response(str(user["_id"]))

    return {"count": len(users_list), "users": users_list}


#delete user
@app.delete("/deleteuser/{user_id}")
async def delete_user(user_id: str):
    # Decode or validate user_id if using tokens
    decoded_user_id = decode_response(user_id)

    if not decoded_user_id or not ObjectId.is_valid(decoded_user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")

    # Perform deletion
    delete_result = await UserTable.delete_one({"_id": ObjectId(decoded_user_id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully", "user_id": encode_response(decoded_user_id)}