

@router.post("/login")
async def login(response: Response, username: str, password: str):
    user = await user_service.verify_user(username, password)
    await auth_service.login_web(user, response)
    return {"msg": "ok"}

@router.get("/me")
async def me(user=Depends(get_current_user)):
    return user