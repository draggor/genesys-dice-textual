from textual_serve.server import Server


def main() -> None:
    server = Server("genesys-dice")
    server.serve()


if __name__ == "__main__":
    main()
