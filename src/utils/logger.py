def log_to_file(content, file="logs.txt"):
    import datetime
    try:
        with open(file, "a", encoding="utf-8") as f:
            f.write(f"==\n{datetime.datetime.utcnow()}\n")
            f.write(content)
            f.write("==\n")
    except:
        pass