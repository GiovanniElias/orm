def get_postgresql_connection_info(*args, **kwargs) -> dict:
    if not kwargs.keys().isdisjoint({"host", "database", "user", "password"}):
        info = dict(
            host=kwargs.get("host"),
            database=kwargs.get("database"),
            user=kwargs.get("user"),
            password=kwargs.get("password"),
        )
        if "port" not in kwargs.keys():
            return info
        info["port"] = kwargs.get("port")
        return info

    raise AttributeError("Invalid connection properties.")
