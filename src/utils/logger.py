def log_to_file(content, file="logs.txt"):
    """
    Logs the content to a specified file, by default logs.txt
    :param content, string content to be logged to the file
    :param file, path to save the log file.
    """
    import datetime
    try:
        with open(file, "a", encoding="utf-8") as f:
            f.write(f"==\n{datetime.datetime.utcnow()}\n")
            f.write(content)
            f.write("==\n")
    except:
        pass
    