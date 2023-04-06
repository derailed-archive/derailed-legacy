"""
Run the API in a development environment.

Part of the Derailed Project.
Copyright 2021-2023 Derailed
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api:derailed", host="0.0.0.0", port=8080, reload=True, reload_dirs=["api"]
    )
