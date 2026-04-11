import services


@router.post("/login")
async def login( form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return services.login(db, form_data.username, form_data.password)

@router.get("/me")
async def me(user=Depends(get_current_user)):
    return user