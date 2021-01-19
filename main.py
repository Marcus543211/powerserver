import asyncio


values = {}


def get_rank(addr):
    return sorted(values, key=values.get, reverse=True).index(addr)


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode().strip()
    power_used = int(message)
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    values[addr] = power_used
    rank = get_rank(addr)

    print(f"Send: {rank!r}")
    writer.write(str(rank))
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 15231)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
