import yaml


# 返回配置信息
def get_config():
    with open("config/config.yaml", "r", encoding="utf8") as fp:
        content = yaml.safe_load(fp)
    return content
