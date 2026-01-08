from Alerting import sendAlert


if __name__ == "__main__":
    import time

    timestamp = time.strftime("%d.%m.%Y - %H:%M:%S", time.localtime(time.time()))
    status = sendAlert(f"POVIS-System start! 🚀 ( {timestamp} )")
    if status.value != 0:
        raise Exception(f"Test failed! Status: {status}")
    input()
