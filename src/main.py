from api import app
import uvicorn


def main():
    uvicorn.run("main:app", port=25565, log_level="info")


if __name__ == "__main__":
    main()
