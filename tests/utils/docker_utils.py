import os
import time

import docker


def is_container_ready(container):
    container.reload()
    return container.status == "running"


def wait_for_stable_status(container, stable_duration=3, interval=1):
    start_time = time.time()
    stable_count = 0

    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count += 1
            if stable_count >= 3:
                return True
        else:
            stable_count = 0

        if stable_count >= stable_duration / interval:
            return True

        time.sleep(interval)

    return False


def start_database_container():
    client = docker.from_env()
    scripts_dir = os.path.abspath("./scripts")
    container_name = "test-db"

    try:
        existing_container = client.containers.get(container_name)
        print(f"container {container_name} already exists")
        existing_container.stop()
        existing_container.remove()
        print(f"container {container_name} removed")
    except docker.errors.NotFound:
        print(f"container {container_name} does not exist")

    container_config = {
        "name": container_name,
        "image": "postgres:16.3-alpine3.20",
        "detach": True,
        "ports": {"5432": "5434"},
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
        },
        "volumes": [f"{scripts_dir}:/docker-entrypoint-initdb.d"],
        "network_mode": "fastapi-development_dev-network",
    }

    # Start the container
    container = client.containers.run(**container_config)

    while not is_container_ready(container):
        time.sleep(4)

    if not wait_for_stable_status(container):
        raise RuntimeError("Database container failed to become stable")

    return container
