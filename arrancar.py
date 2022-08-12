#!/usr/bin/env python3
"""
Arrancar gunicorn para que se ejecute el servicio de la API
"""
import argparse
import os
import sys

APP = "plataforma_web.app:app"
PORT = 8002


def uvicorn_run():
    """Run uvicorn"""

    # Parsear argumentos
    parser = argparse.ArgumentParser(description="Arrancar uvicorn")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host default 127.0.0.1")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port default {PORT}")
    parser.add_argument("--reload", type=bool, default=True, help="Reload default True")
    args = parser.parse_args()

    # Definir comando a ejecutar
    reload_str = "--reload" if args.reload else ""
    cmd = f"uvicorn --host={args.host} --port {args.port} {reload_str} {APP}"
    print(cmd)

    # Ejecutar comando
    os.system(cmd)


def gunicorn_run():
    """Run gunicorn"""

    # Parsear argumentos
    parser = argparse.ArgumentParser(description="Arrancar gunicorn")
    parser.add_argument("-r", "--reload", type=bool, default=True)
    parser.add_argument("-w", "--workers", type=int, default=4)
    parser.add_argument("-b", "--bind", type=str, default=f"0.0.0.0:{PORT}")
    parser.add_argument("-k", "--worker-class", type=str, default="uvicorn.workers.UvicornWorker")
    args = parser.parse_args()

    # Definir comando a ejecutar
    reload_str = "--reload" if args.reload else ""
    cmd = f"gunicorn {reload_str} -w {args.workers} -b {args.bind} -k {args.worker_class} {APP}"
    print(cmd)

    # Ejecutar comando
    os.system(cmd)


def main():
    """Main"""

    # Arrancar uvicorn o gunicorn
    if "ARRANCAR" in os.environ:
        if os.environ["ARRANCAR"] == "uvicorn":
            uvicorn_run()
        elif os.environ["ARRANCAR"] == "gunicorn":
            gunicorn_run()
        else:
            print("No se puede arrancar nada")
            sys.exit(1)
    else:
        print("No se puede arrancar nada")
        sys.exit(1)


if __name__ == "__main__":
    main()
    sys.exit(0)
