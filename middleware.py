import time

async def logging_middleware(request,call_next):

    start=time.time()
    response=await call_next(request)
    end=time.time()

    print(
        f"{request.method} | "
        f"{request.url.path} | "
        f"{response.status_code} | "
        f"{round(end-start,3)} sec"
    )

    return response